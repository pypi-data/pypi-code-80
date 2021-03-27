"""Utility functions for converting to TextEdit.

This module is a bridge between `jedi.Refactoring` and
`pygls.types.TextEdit` types
"""


import ast
import difflib
from bisect import bisect_right
from typing import Iterator, List, NamedTuple, Union

from jedi.api.refactoring import ChangedFile, Refactoring
from pygls.lsp.types import (
    Position,
    Range,
    RenameFile,
    RenameFileOptions,
    TextDocumentEdit,
    TextEdit,
    VersionedTextDocumentIdentifier,
)
from pygls.workspace import Document, Workspace


def is_valid_python(code: str) -> bool:
    """Check whether Python code is syntactically valid."""
    try:
        ast.parse(code)
    except SyntaxError:
        return False
    return True


def lsp_document_changes(
    workspace: Workspace,
    refactoring: Refactoring,
) -> List[Union[TextDocumentEdit, RenameFile]]:
    """Get lsp text document edits from Jedi refactoring.

    This is the main public function that you probably want
    """
    converter = RefactoringConverter(workspace, refactoring)
    return [
        *converter.lsp_text_document_edits(),
        *converter.lsp_renames(),
    ]


class RefactoringConverter:
    """Convert jedi Refactoring objects into renaming machines."""

    def __init__(self, workspace: Workspace, refactoring: Refactoring) -> None:
        self.workspace = workspace
        self.refactoring = refactoring

    def lsp_renames(self) -> Iterator[RenameFile]:
        """Get all File rename operations."""
        for old_name, new_name in self.refactoring.get_renames():
            yield RenameFile(
                old_uri=old_name.as_uri(),
                new_uri=new_name.as_uri(),
                options=RenameFileOptions(
                    ignore_if_exists=True, overwrite=True
                ),
            )

    def lsp_text_document_edits(self) -> Iterator[TextDocumentEdit]:
        """Get all text document edits."""
        changed_files = self.refactoring.get_changed_files()
        for path, changed_file in changed_files.items():
            uri = path.as_uri()
            document = self.workspace.get_document(uri)
            version = 0 if document.version is None else document.version
            text_edits = lsp_text_edits(document, changed_file)
            if text_edits:
                yield TextDocumentEdit(
                    text_document=VersionedTextDocumentIdentifier(
                        uri=uri,
                        version=version,
                    ),
                    edits=text_edits,
                )


_OPCODES_CHANGE = {"replace", "delete", "insert"}


def lsp_text_edits(
    document: Document, changed_file: ChangedFile
) -> List[TextEdit]:
    """Take a jedi `ChangedFile` and convert to list of text edits.

    Handles inserts, replaces, and deletions within a text file.

    Additionally, makes sure returned code is syntactically valid Python.
    """
    new_code = changed_file.get_new_code()
    if not is_valid_python(new_code):
        return []

    old_code = document.source
    position_lookup = PositionLookup(old_code)
    text_edits = []
    for opcode in get_opcodes(old_code, new_code):
        if opcode.op in _OPCODES_CHANGE:
            start = position_lookup.get(opcode.old_start)
            end = position_lookup.get(opcode.old_end)
            new_text = new_code[opcode.new_start : opcode.new_end]
            text_edits.append(
                TextEdit(
                    range=Range(start=start, end=end),
                    new_text=new_text,
                )
            )
    return text_edits


class Opcode(NamedTuple):
    """Typed opcode.

    Op can be one of the following values:
        'replace':  a[i1:i2] should be replaced by b[j1:j2]
        'delete':   a[i1:i2] should be deleted.
            Note that j1==j2 in this case.
        'insert':   b[j1:j2] should be inserted at a[i1:i1].
            Note that i1==i2 in this case.
        'equal':    a[i1:i2] == b[j1:j2]
    """

    op: str
    old_start: int
    old_end: int
    new_start: int
    new_end: int


def get_opcodes(old: str, new: str) -> List[Opcode]:
    """Obtain typed opcodes from two files (old and new)"""
    diff = difflib.SequenceMatcher(a=old, b=new)
    return [Opcode(*opcode) for opcode in diff.get_opcodes()]


# pylint: disable=too-few-public-methods
class PositionLookup:
    """Data structure to convert a byte offset in a file to a line number and
    character."""

    def __init__(self, code: str) -> None:
        # Create a list saying at what offset in the file each line starts.
        self.line_starts = []
        offset = 0
        for line in code.splitlines(keepends=True):
            self.line_starts.append(offset)
            offset += len(line)

    def get(self, offset: int) -> Position:
        """Get the position in the file that corresponds to the given
        offset."""
        line = bisect_right(self.line_starts, offset) - 1
        character = offset - self.line_starts[line]
        return Position(line=line, character=character)
