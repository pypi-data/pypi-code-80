import re
import typing as ty

from . import config
from . import misc


__all__: ty.Final[ty.Tuple[str, ...]] = ("Checker",)


class Checker:
	"""
	Checks indentation in blank lines to match the next line if there happens to be any
	"""
	name: str    = "flake8-tabs"
	version: str = misc.__version__
	
	
	REGEXP = re.compile(r"([ \t\v]*).*?([ \t\v]*)([\r\x0C]*\n?)$")
	
	
	def __new__(cls, physical_line: str, lines: ty.List[str], line_number: int, filename: str):
		# Look up per-file attributes from EditorConfig
		cfg = config.Config.with_filepath(filename, "blank-lines-indent", "indent-size")
		
		indent, trailing, crlf = cls.REGEXP.match(physical_line).groups()
		if len(physical_line) - len(crlf) < 1:  # Totally blank line
			if cfg["blank-lines-indent"] != "always":
				return  # Otherwise check whether the next non-blank line is also unindented
		elif len(indent) + len(crlf) == len(physical_line):
			if cfg["blank-lines-indent"] == "never":  # Cannot have indented blank line in this mode
				return (0, misc.format_warning(
					293,
					"blank line contains whitespace, but option "
					"blank-lines-indent=never does not permit this"
				))
		else:
			# Not a blank line with whitespace
			if len(trailing) > 0:
				return (len(physical_line) - len(trailing) - len(crlf), misc.format_warning(
					291,
					"trailing whitespace"
				))
			return
		
		# Confusingly using `lines[line_number]` does not yield the current line
		# but the line *after* that, so use the following variable to make it
		# more obvious what is happening in the following code
		line_idx = line_number - 1
		
		# Scan for previous non-blank line
		expected_indent_prev = 0
		for idx in range(line_idx - 1, -1, -1):
			line_indent, _, line_crlf = cls.REGEXP.match(lines[idx]).groups()
			if len(line_indent) + len(line_crlf) != len(lines[idx]):
				expected_indent_prev = line_indent
				break
		
		# Scan for next non-blank line
		expected_indent_next = ""
		for idx in range(line_idx + 1, len(lines), +1):
			line_indent, _, line_crlf = cls.REGEXP.match(lines[idx]).groups()
			if len(line_indent) + len(line_crlf) != len(lines[idx]):
				expected_indent_next = line_indent
				break
		
		# Choose the shorter indentation of the two
		if misc.parse_indent(expected_indent_prev).columns(cfg["indent-size"]) \
		   < misc.parse_indent(expected_indent_next).columns(cfg["indent-size"]):
			expected_indent = expected_indent_prev
		else:
			expected_indent = expected_indent_next
		
		# Compare the two indents
		if indent != expected_indent:
			return (0, misc.format_warning(
				293,
				"blank line contains unaligned whitespace"
			))
	
	def __init__(self, physical_line, lines, line_number, filename):
		pass