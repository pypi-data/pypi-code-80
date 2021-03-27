# -*- coding: utf-8 -*-
"""
Verbose and colourful traceback formatting.

**ColorTB**

I've always found it a bit hard to visually parse tracebacks in Python.  The
ColorTB class is a solution to that problem.  It colors the different parts of a
traceback in a manner similar to what you would expect from a syntax-highlighting
text editor.

Installation instructions for ColorTB::

    import sys,ultratb
    sys.excepthook = ultratb.ColorTB()

**VerboseTB**

I've also included a port of Ka-Ping Yee's "cgitb.py" that produces all kinds
of useful info when a traceback occurs.  Ping originally had it spit out HTML
and intended it for CGI programmers, but why should they have all the fun?  I
altered it to spit out colored text to the terminal.  It's a bit overwhelming,
but kind of neat, and maybe useful for long-running programs that you believe
are bug-free.  If a crash *does* occur in that type of program you want details.
Give it a shot--you'll love it or you'll hate it.

.. note::

  The Verbose mode prints the variables currently visible where the exception
  happened (shortening their strings if too long). This can potentially be
  very slow, if you happen to have a huge data structure whose string
  representation is complex to compute. Your computer may appear to freeze for
  a while with cpu usage at 100%. If this occurs, you can cancel the traceback
  with Ctrl-C (maybe hitting it more than once).

  If you encounter this kind of situation often, you may want to use the
  Verbose_novars mode instead of the regular Verbose, which avoids formatting
  variables (but otherwise includes the information and context given by
  Verbose).

.. note::

  The verbose mode print all variables in the stack, which means it can
  potentially leak sensitive information like access keys, or unencrypted
  password.

Installation instructions for VerboseTB::

    import sys,ultratb
    sys.excepthook = ultratb.VerboseTB()

Note:  Much of the code in this module was lifted verbatim from the standard
library module 'traceback.py' and Ka-Ping Yee's 'cgitb.py'.

Color schemes
-------------

The colors are defined in the class TBTools through the use of the
ColorSchemeTable class. Currently the following exist:

  - NoColor: allows all of this module to be used in any terminal (the color
    escapes are just dummy blank strings).

  - Linux: is meant to look good in a terminal like the Linux console (black
    or very dark background).

  - LightBG: similar to Linux but swaps dark/light colors to be more readable
    in light background terminals.

  - Neutral: a neutral color scheme that should be readable on both light and
    dark background

You can implement other color schemes easily, the syntax is fairly
self-explanatory. Please send back new schemes you develop to the author for
possible inclusion in future releases.

Inheritance diagram:

.. inheritance-diagram:: IPython.core.ultratb
   :parts: 3
"""

#*****************************************************************************
# Copyright (C) 2001 Nathaniel Gray <n8gray@caltech.edu>
# Copyright (C) 2001-2004 Fernando Perez <fperez@colorado.edu>
#
# Distributed under the terms of the BSD License.  The full license is in
# the file COPYING, distributed as part of this software.
#*****************************************************************************


import dis
import inspect
import keyword
import linecache
import os
import pydoc
import re
import sys
import time
import tokenize
import traceback

from tokenize import generate_tokens

# For purposes of monkeypatching inspect to fix a bug in it.
from inspect import getsourcefile, getfile, getmodule, \
    ismodule, isclass, ismethod, isfunction, istraceback, isframe, iscode

# IPython's own modules
from IPython import get_ipython
from IPython.core import debugger
from IPython.core.display_trap import DisplayTrap
from IPython.core.excolors import exception_colors
from IPython.utils import PyColorize
from IPython.utils import path as util_path
from IPython.utils import py3compat
from IPython.utils.data import uniq_stable
from IPython.utils.terminal import get_terminal_size

from logging import info, error, debug

from importlib.util import source_from_cache

import IPython.utils.colorable as colorable

# Globals
# amount of space to put line numbers before verbose tracebacks
INDENT_SIZE = 8

# Default color scheme.  This is used, for example, by the traceback
# formatter.  When running in an actual IPython instance, the user's rc.colors
# value is used, but having a module global makes this functionality available
# to users of ultratb who are NOT running inside ipython.
DEFAULT_SCHEME = 'NoColor'


# Number of frame above which we are likely to have a recursion and will
# **attempt** to detect it.  Made modifiable mostly to speedup test suite
# as detecting recursion is one of our slowest test
_FRAME_RECURSION_LIMIT = 500

# ---------------------------------------------------------------------------
# Code begins

# Utility functions
def inspect_error():
    """Print a message about internal inspect errors.

    These are unfortunately quite common."""

    error('Internal Python error in the inspect module.\n'
          'Below is the traceback from this internal error.\n')


# This function is a monkeypatch we apply to the Python inspect module. We have
# now found when it's needed (see discussion on issue gh-1456), and we have a
# test case (IPython.core.tests.test_ultratb.ChangedPyFileTest) that fails if
# the monkeypatch is not applied. TK, Aug 2012.
def findsource(object):
    """Return the entire source file and starting line number for an object.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a list of all the lines
    in the file and the line number indexes a line in that list.  An IOError
    is raised if the source code cannot be retrieved.

    FIXED version with which we monkeypatch the stdlib to work around a bug."""

    file = getsourcefile(object) or getfile(object)
    # If the object is a frame, then trying to get the globals dict from its
    # module won't work. Instead, the frame object itself has the globals
    # dictionary.
    globals_dict = None
    if inspect.isframe(object):
        # XXX: can this ever be false?
        globals_dict = object.f_globals
    else:
        module = getmodule(object, file)
        if module:
            globals_dict = module.__dict__
    lines = linecache.getlines(file, globals_dict)
    if not lines:
        raise IOError('could not get source code')

    if ismodule(object):
        return lines, 0

    if isclass(object):
        name = object.__name__
        pat = re.compile(r'^(\s*)class\s*' + name + r'\b')
        # make some effort to find the best matching class definition:
        # use the one with the least indentation, which is the one
        # that's most probably not inside a function definition.
        candidates = []
        for i, line in enumerate(lines):
            match = pat.match(line)
            if match:
                # if it's at toplevel, it's already the best one
                if line[0] == 'c':
                    return lines, i
                # else add whitespace to candidate list
                candidates.append((match.group(1), i))
        if candidates:
            # this will sort by whitespace, and by line number,
            # less whitespace first
            candidates.sort()
            return lines, candidates[0][1]
        else:
            raise IOError('could not find class definition')

    if ismethod(object):
        object = object.__func__
    if isfunction(object):
        object = object.__code__
    if istraceback(object):
        object = object.tb_frame
    if isframe(object):
        object = object.f_code
    if iscode(object):
        if not hasattr(object, 'co_firstlineno'):
            raise IOError('could not find function definition')
        pat = re.compile(r'^(\s*def\s)|(.*(?<!\w)lambda(:|\s))|^(\s*@)')
        pmatch = pat.match
        # fperez - fix: sometimes, co_firstlineno can give a number larger than
        # the length of lines, which causes an error.  Safeguard against that.
        lnum = min(object.co_firstlineno, len(lines)) - 1
        while lnum > 0:
            if pmatch(lines[lnum]):
                break
            lnum -= 1

        return lines, lnum
    raise IOError('could not find code object')


# Monkeypatch inspect to apply our bugfix.
def with_patch_inspect(f):
    """
    Deprecated since IPython 6.0
    decorator for monkeypatching inspect.findsource
    """

    def wrapped(*args, **kwargs):
        save_findsource = inspect.findsource
        inspect.findsource = findsource
        try:
            return f(*args, **kwargs)
        finally:
            inspect.findsource = save_findsource

    return wrapped


def fix_frame_records_filenames(records):
    """Try to fix the filenames in each record from inspect.getinnerframes().

    Particularly, modules loaded from within zip files have useless filenames
    attached to their code object, and inspect.getinnerframes() just uses it.
    """
    fixed_records = []
    for frame, filename, line_no, func_name, lines, index in records:
        # Look inside the frame's globals dictionary for __file__,
        # which should be better. However, keep Cython filenames since
        # we prefer the source filenames over the compiled .so file.
        if not filename.endswith(('.pyx', '.pxd', '.pxi')):
            better_fn = frame.f_globals.get('__file__', None)
            if isinstance(better_fn, str):
                # Check the type just in case someone did something weird with
                # __file__. It might also be None if the error occurred during
                # import.
                filename = better_fn
        fixed_records.append((frame, filename, line_no, func_name, lines, index))
    return fixed_records


@with_patch_inspect
def _fixed_getinnerframes(etb, context=1, tb_offset=0):
    LNUM_POS, LINES_POS, INDEX_POS = 2, 4, 5

    records = fix_frame_records_filenames(inspect.getinnerframes(etb, context))
    # If the error is at the console, don't build any context, since it would
    # otherwise produce 5 blank lines printed out (there is no file at the
    # console)
    rec_check = records[tb_offset:]
    try:
        rname = rec_check[0][1]
        if rname == '<ipython console>' or rname.endswith('<string>'):
            return rec_check
    except IndexError:
        pass

    aux = traceback.extract_tb(etb)
    assert len(records) == len(aux)
    for i, (file, lnum, _, _) in enumerate(aux):
        maybeStart = lnum - 1 - context // 2
        start = max(maybeStart, 0)
        end = start + context
        lines = linecache.getlines(file)[start:end]
        buf = list(records[i])
        buf[LNUM_POS] = lnum
        buf[INDEX_POS] = lnum - 1 - start
        buf[LINES_POS] = lines
        records[i] = tuple(buf)
    return records[tb_offset:]

# Helper function -- largely belongs to VerboseTB, but we need the same
# functionality to produce a pseudo verbose TB for SyntaxErrors, so that they
# can be recognized properly by ipython.el's py-traceback-line-re
# (SyntaxErrors have to be treated specially because they have no traceback)


def _format_traceback_lines(lnum, index, lines, Colors, lvals, _line_format):
    """
    Format tracebacks lines with pointing arrow, leading numbers...

    Parameters
    ==========

    lnum: int
    index: int
    lines: list[string]
    Colors:
        ColorScheme used.
    lvals: bytes
        Values of local variables, already colored, to inject just after the error line.
    _line_format: f (str) -> (str, bool)
        return (colorized version of str, failure to do so)
    """
    numbers_width = INDENT_SIZE - 1
    res = []

    for i,line in enumerate(lines, lnum-index):
        line = py3compat.cast_unicode(line)

        new_line, err = _line_format(line, 'str')
        if not err:
            line = new_line

        if i == lnum:
            # This is the line with the error
            pad = numbers_width - len(str(i))
            num = '%s%s' % (debugger.make_arrow(pad), str(lnum))
            line = '%s%s%s %s%s' % (Colors.linenoEm, num,
                                    Colors.line, line, Colors.Normal)
        else:
            num = '%*s' % (numbers_width, i)
            line = '%s%s%s %s' % (Colors.lineno, num,
                                  Colors.Normal, line)

        res.append(line)
        if lvals and i == lnum:
            res.append(lvals + '\n')
    return res

def is_recursion_error(etype, value, records):
    try:
        # RecursionError is new in Python 3.5
        recursion_error_type = RecursionError
    except NameError:
        recursion_error_type = RuntimeError

    # The default recursion limit is 1000, but some of that will be taken up
    # by stack frames in IPython itself. >500 frames probably indicates
    # a recursion error.
    return (etype is recursion_error_type) \
           and "recursion" in str(value).lower() \
           and len(records) > _FRAME_RECURSION_LIMIT

def find_recursion(etype, value, records):
    """Identify the repeating stack frames from a RecursionError traceback

    'records' is a list as returned by VerboseTB.get_records()

    Returns (last_unique, repeat_length)
    """
    # This involves a bit of guesswork - we want to show enough of the traceback
    # to indicate where the recursion is occurring. We guess that the innermost
    # quarter of the traceback (250 frames by default) is repeats, and find the
    # first frame (from in to out) that looks different.
    if not is_recursion_error(etype, value, records):
        return len(records), 0

    # Select filename, lineno, func_name to track frames with
    records = [r[1:4] for r in records]
    inner_frames = records[-(len(records)//4):]
    frames_repeated = set(inner_frames)

    last_seen_at = {}
    longest_repeat = 0
    i = len(records)
    for frame in reversed(records):
        i -= 1
        if frame not in frames_repeated:
            last_unique = i
            break

        if frame in last_seen_at:
            distance = last_seen_at[frame] - i
            longest_repeat = max(longest_repeat, distance)

        last_seen_at[frame] = i
    else:
        last_unique = 0 # The whole traceback was recursion

    return last_unique, longest_repeat

#---------------------------------------------------------------------------
# Module classes
class TBTools(colorable.Colorable):
    """Basic tools used by all traceback printer classes."""

    # Number of frames to skip when reporting tracebacks
    tb_offset = 0

    def __init__(self, color_scheme='NoColor', call_pdb=False, ostream=None, parent=None, config=None):
        # Whether to call the interactive pdb debugger after printing
        # tracebacks or not
        super(TBTools, self).__init__(parent=parent, config=config)
        self.call_pdb = call_pdb

        # Output stream to write to.  Note that we store the original value in
        # a private attribute and then make the public ostream a property, so
        # that we can delay accessing sys.stdout until runtime.  The way
        # things are written now, the sys.stdout object is dynamically managed
        # so a reference to it should NEVER be stored statically.  This
        # property approach confines this detail to a single location, and all
        # subclasses can simply access self.ostream for writing.
        self._ostream = ostream

        # Create color table
        self.color_scheme_table = exception_colors()

        self.set_colors(color_scheme)
        self.old_scheme = color_scheme  # save initial value for toggles

        if call_pdb:
            self.pdb = debugger.Pdb()
        else:
            self.pdb = None

    def _get_ostream(self):
        """Output stream that exceptions are written to.

        Valid values are:

        - None: the default, which means that IPython will dynamically resolve
          to sys.stdout.  This ensures compatibility with most tools, including
          Windows (where plain stdout doesn't recognize ANSI escapes).

        - Any object with 'write' and 'flush' attributes.
        """
        return sys.stdout if self._ostream is None else self._ostream

    def _set_ostream(self, val):
        assert val is None or (hasattr(val, 'write') and hasattr(val, 'flush'))
        self._ostream = val

    ostream = property(_get_ostream, _set_ostream)

    def get_parts_of_chained_exception(self, evalue):
        def get_chained_exception(exception_value):
            cause = getattr(exception_value, '__cause__', None)
            if cause:
                return cause
            if getattr(exception_value, '__suppress_context__', False):
                return None
            return getattr(exception_value, '__context__', None)

        chained_evalue = get_chained_exception(evalue)

        if chained_evalue:
            return chained_evalue.__class__, chained_evalue, chained_evalue.__traceback__

    def prepare_chained_exception_message(self, cause):
        direct_cause = "\nThe above exception was the direct cause of the following exception:\n"
        exception_during_handling = "\nDuring handling of the above exception, another exception occurred:\n"

        if cause:
            message = [[direct_cause]]
        else:
            message = [[exception_during_handling]]
        return message

    def set_colors(self, *args, **kw):
        """Shorthand access to the color table scheme selector method."""

        # Set own color table
        self.color_scheme_table.set_active_scheme(*args, **kw)
        # for convenience, set Colors to the active scheme
        self.Colors = self.color_scheme_table.active_colors
        # Also set colors of debugger
        if hasattr(self, 'pdb') and self.pdb is not None:
            self.pdb.set_colors(*args, **kw)

    def color_toggle(self):
        """Toggle between the currently active color scheme and NoColor."""

        if self.color_scheme_table.active_scheme_name == 'NoColor':
            self.color_scheme_table.set_active_scheme(self.old_scheme)
            self.Colors = self.color_scheme_table.active_colors
        else:
            self.old_scheme = self.color_scheme_table.active_scheme_name
            self.color_scheme_table.set_active_scheme('NoColor')
            self.Colors = self.color_scheme_table.active_colors

    def stb2text(self, stb):
        """Convert a structured traceback (a list) to a string."""
        return '\n'.join(stb)

    def text(self, etype, value, tb, tb_offset=None, context=5):
        """Return formatted traceback.

        Subclasses may override this if they add extra arguments.
        """
        tb_list = self.structured_traceback(etype, value, tb,
                                            tb_offset, context)
        return self.stb2text(tb_list)

    def structured_traceback(self, etype, evalue, tb, tb_offset=None,
                             context=5, mode=None):
        """Return a list of traceback frames.

        Must be implemented by each class.
        """
        raise NotImplementedError()


#---------------------------------------------------------------------------
class ListTB(TBTools):
    """Print traceback information from a traceback list, with optional color.

    Calling requires 3 arguments: (etype, evalue, elist)
    as would be obtained by::
    
      etype, evalue, tb = sys.exc_info()
      if tb:
        elist = traceback.extract_tb(tb)
      else:
        elist = None

    It can thus be used by programs which need to process the traceback before
    printing (such as console replacements based on the code module from the
    standard library).

    Because they are meant to be called without a full traceback (only a
    list), instances of this class can't call the interactive pdb debugger."""

    def __init__(self, color_scheme='NoColor', call_pdb=False, ostream=None, parent=None, config=None):
        TBTools.__init__(self, color_scheme=color_scheme, call_pdb=call_pdb,
                         ostream=ostream, parent=parent,config=config)

    def __call__(self, etype, value, elist):
        self.ostream.flush()
        self.ostream.write(self.text(etype, value, elist))
        self.ostream.write('\n')

    def _extract_tb(self, tb):
        if tb:
            return traceback.extract_tb(tb)
        else:
            return None

    def structured_traceback(self, etype, evalue, etb=None, tb_offset=None,
                             context=5):
        """Return a color formatted string with the traceback info.

        Parameters
        ----------
        etype : exception type
          Type of the exception raised.

        evalue : object
          Data stored in the exception

        etb : object
          If list: List of frames, see class docstring for details.
          If Traceback: Traceback of the exception.

        tb_offset : int, optional
          Number of frames in the traceback to skip.  If not given, the
          instance evalue is used (set in constructor).

        context : int, optional
          Number of lines of context information to print.

        Returns
        -------
        String with formatted exception.
        """
        # This is a workaround to get chained_exc_ids in recursive calls
        # etb should not be a tuple if structured_traceback is not recursive
        if isinstance(etb, tuple):
            etb, chained_exc_ids = etb
        else:
            chained_exc_ids = set()

        if isinstance(etb, list):
            elist = etb
        elif etb is not None:
            elist = self._extract_tb(etb)
        else:
            elist = []
        tb_offset = self.tb_offset if tb_offset is None else tb_offset
        Colors = self.Colors
        out_list = []
        if elist:

            if tb_offset and len(elist) > tb_offset:
                elist = elist[tb_offset:]

            out_list.append('Traceback %s(most recent call last)%s:' %
                            (Colors.normalEm, Colors.Normal) + '\n')
            out_list.extend(self._format_list(elist))
        # The exception info should be a single entry in the list.
        lines = ''.join(self._format_exception_only(etype, evalue))
        out_list.append(lines)

        exception = self.get_parts_of_chained_exception(evalue)

        if exception and not id(exception[1]) in chained_exc_ids:
            chained_exception_message = self.prepare_chained_exception_message(
                evalue.__cause__)[0]
            etype, evalue, etb = exception
            # Trace exception to avoid infinite 'cause' loop
            chained_exc_ids.add(id(exception[1]))
            chained_exceptions_tb_offset = 0
            out_list = (
                self.structured_traceback(
                    etype, evalue, (etb, chained_exc_ids),
                    chained_exceptions_tb_offset, context)
                + chained_exception_message
                + out_list)

        return out_list

    def _format_list(self, extracted_list):
        """Format a list of traceback entry tuples for printing.

        Given a list of tuples as returned by extract_tb() or
        extract_stack(), return a list of strings ready for printing.
        Each string in the resulting list corresponds to the item with the
        same index in the argument list.  Each string ends in a newline;
        the strings may contain internal newlines as well, for those items
        whose source text line is not None.

        Lifted almost verbatim from traceback.py
        """

        Colors = self.Colors
        list = []
        for filename, lineno, name, line in extracted_list[:-1]:
            item = '  File %s"%s"%s, line %s%d%s, in %s%s%s\n' % \
                   (Colors.filename, filename, Colors.Normal,
                    Colors.lineno, lineno, Colors.Normal,
                    Colors.name, name, Colors.Normal)
            if line:
                item += '    %s\n' % line.strip()
            list.append(item)
        # Emphasize the last entry
        filename, lineno, name, line = extracted_list[-1]
        item = '%s  File %s"%s"%s, line %s%d%s, in %s%s%s%s\n' % \
               (Colors.normalEm,
                Colors.filenameEm, filename, Colors.normalEm,
                Colors.linenoEm, lineno, Colors.normalEm,
                Colors.nameEm, name, Colors.normalEm,
                Colors.Normal)
        if line:
            item += '%s    %s%s\n' % (Colors.line, line.strip(),
                                      Colors.Normal)
        list.append(item)
        return list

    def _format_exception_only(self, etype, value):
        """Format the exception part of a traceback.

        The arguments are the exception type and value such as given by
        sys.exc_info()[:2]. The return value is a list of strings, each ending
        in a newline.  Normally, the list contains a single string; however,
        for SyntaxError exceptions, it contains several lines that (when
        printed) display detailed information about where the syntax error
        occurred.  The message indicating which exception occurred is the
        always last string in the list.

        Also lifted nearly verbatim from traceback.py
        """
        have_filedata = False
        Colors = self.Colors
        list = []
        stype = py3compat.cast_unicode(Colors.excName + etype.__name__ + Colors.Normal)
        if value is None:
            # Not sure if this can still happen in Python 2.6 and above
            list.append(stype + '\n')
        else:
            if issubclass(etype, SyntaxError):
                have_filedata = True
                if not value.filename: value.filename = "<string>"
                if value.lineno:
                    lineno = value.lineno
                    textline = linecache.getline(value.filename, value.lineno)
                else:
                    lineno = 'unknown'
                    textline = ''
                list.append('%s  File %s"%s"%s, line %s%s%s\n' % \
                            (Colors.normalEm,
                             Colors.filenameEm, py3compat.cast_unicode(value.filename), Colors.normalEm,
                             Colors.linenoEm, lineno, Colors.Normal  ))
                if textline == '':
                    textline = py3compat.cast_unicode(value.text, "utf-8")

                if textline is not None:
                    i = 0
                    while i < len(textline) and textline[i].isspace():
                        i += 1
                    list.append('%s    %s%s\n' % (Colors.line,
                                                  textline.strip(),
                                                  Colors.Normal))
                    if value.offset is not None:
                        s = '    '
                        for c in textline[i:value.offset - 1]:
                            if c.isspace():
                                s += c
                            else:
                                s += ' '
                        list.append('%s%s^%s\n' % (Colors.caret, s,
                                                   Colors.Normal))

            try:
                s = value.msg
            except Exception:
                s = self._some_str(value)
            if s:
                list.append('%s%s:%s %s\n' % (stype, Colors.excName,
                                              Colors.Normal, s))
            else:
                list.append('%s\n' % stype)

        # sync with user hooks
        if have_filedata:
            ipinst = get_ipython()
            if ipinst is not None:
                ipinst.hooks.synchronize_with_editor(value.filename, value.lineno, 0)

        return list

    def get_exception_only(self, etype, value):
        """Only print the exception type and message, without a traceback.

        Parameters
        ----------
        etype : exception type
        value : exception value
        """
        return ListTB.structured_traceback(self, etype, value)

    def show_exception_only(self, etype, evalue):
        """Only print the exception type and message, without a traceback.

        Parameters
        ----------
        etype : exception type
        value : exception value
        """
        # This method needs to use __call__ from *this* class, not the one from
        # a subclass whose signature or behavior may be different
        ostream = self.ostream
        ostream.flush()
        ostream.write('\n'.join(self.get_exception_only(etype, evalue)))
        ostream.flush()

    def _some_str(self, value):
        # Lifted from traceback.py
        try:
            return py3compat.cast_unicode(str(value))
        except:
            return u'<unprintable %s object>' % type(value).__name__


#----------------------------------------------------------------------------
class VerboseTB(TBTools):
    """A port of Ka-Ping Yee's cgitb.py module that outputs color text instead
    of HTML.  Requires inspect and pydoc.  Crazy, man.

    Modified version which optionally strips the topmost entries from the
    traceback, to be used with alternate interpreters (because their own code
    would appear in the traceback)."""

    def __init__(self, color_scheme='Linux', call_pdb=False, ostream=None,
                 tb_offset=0, long_header=False, include_vars=True,
                 check_cache=None, debugger_cls = None,
                 parent=None, config=None):
        """Specify traceback offset, headers and color scheme.

        Define how many frames to drop from the tracebacks. Calling it with
        tb_offset=1 allows use of this handler in interpreters which will have
        their own code at the top of the traceback (VerboseTB will first
        remove that frame before printing the traceback info)."""
        TBTools.__init__(self, color_scheme=color_scheme, call_pdb=call_pdb,
                         ostream=ostream, parent=parent, config=config)
        self.tb_offset = tb_offset
        self.long_header = long_header
        self.include_vars = include_vars
        # By default we use linecache.checkcache, but the user can provide a
        # different check_cache implementation.  This is used by the IPython
        # kernel to provide tracebacks for interactive code that is cached,
        # by a compiler instance that flushes the linecache but preserves its
        # own code cache.
        if check_cache is None:
            check_cache = linecache.checkcache
        self.check_cache = check_cache

        self.debugger_cls = debugger_cls or debugger.Pdb
        self.skip_hidden = True

    def format_records(self, records, last_unique, recursion_repeat):
        """Format the stack frames of the traceback"""
        frames = []

        skipped = 0
        lastrecord = len(records) - 1
        for i, r in enumerate(records[: last_unique + recursion_repeat + 1]):
            if self.skip_hidden:
                if r[0].f_locals.get("__tracebackhide__", 0) and i != lastrecord:
                    skipped += 1
                    continue
            if skipped:
                Colors = self.Colors  # just a shorthand + quicker name lookup
                ColorsNormal = Colors.Normal  # used a lot
                frames.append(
                    "    %s[... skipping hidden %s frame]%s\n"
                    % (Colors.excName, skipped, ColorsNormal)
                )
                skipped = 0

            frames.append(self.format_record(*r))
            
        if skipped:
            Colors = self.Colors  # just a shorthand + quicker name lookup
            ColorsNormal = Colors.Normal  # used a lot
            frames.append(
                "    %s[... skipping hidden %s frame]%s\n"
                % (Colors.excName, skipped, ColorsNormal)
            )

        if recursion_repeat:
            frames.append('... last %d frames repeated, from the frame below ...\n' % recursion_repeat)
            frames.append(self.format_record(*records[last_unique+recursion_repeat+1]))

        return frames

    def format_record(self, frame, file, lnum, func, lines, index):
        """Format a single stack frame"""
        Colors = self.Colors  # just a shorthand + quicker name lookup
        ColorsNormal = Colors.Normal  # used a lot
        col_scheme = self.color_scheme_table.active_scheme_name
        indent = ' ' * INDENT_SIZE
        em_normal = '%s\n%s%s' % (Colors.valEm, indent, ColorsNormal)
        undefined = '%sundefined%s' % (Colors.em, ColorsNormal)
        tpl_link = '%s%%s%s' % (Colors.filenameEm, ColorsNormal)
        tpl_call = 'in %s%%s%s%%s%s' % (Colors.vName, Colors.valEm,
                                        ColorsNormal)
        tpl_call_fail = 'in %s%%s%s(***failed resolving arguments***)%s' % \
                        (Colors.vName, Colors.valEm, ColorsNormal)
        tpl_local_var = '%s%%s%s' % (Colors.vName, ColorsNormal)
        tpl_global_var = '%sglobal%s %s%%s%s' % (Colors.em, ColorsNormal,
                                                 Colors.vName, ColorsNormal)
        tpl_name_val = '%%s %s= %%s%s' % (Colors.valEm, ColorsNormal)

        if not file:
            file = '?'
        elif file.startswith(str("<")) and file.endswith(str(">")):
            # Not a real filename, no problem...
            pass
        elif not os.path.isabs(file):
            # Try to make the filename absolute by trying all
            # sys.path entries (which is also what linecache does)
            for dirname in sys.path:
                try:
                    fullname = os.path.join(dirname, file)
                    if os.path.isfile(fullname):
                        file = os.path.abspath(fullname)
                        break
                except Exception:
                    # Just in case that sys.path contains very
                    # strange entries...
                    pass

        file = py3compat.cast_unicode(file, util_path.fs_encoding)
        link = tpl_link % util_path.compress_user(file)
        args, varargs, varkw, locals_ = inspect.getargvalues(frame)

        if func == '?':
            call = ''
        elif func == '<module>':
            call = tpl_call % (func, '')
        else:
            # Decide whether to include variable details or not
            var_repr = eqrepr if self.include_vars else nullrepr
            try:
                call = tpl_call % (func, inspect.formatargvalues(args,
                                                                 varargs, varkw,
                                                                 locals_, formatvalue=var_repr))
            except KeyError:
                # This happens in situations like errors inside generator
                # expressions, where local variables are listed in the
                # line, but can't be extracted from the frame.  I'm not
                # 100% sure this isn't actually a bug in inspect itself,
                # but since there's no info for us to compute with, the
                # best we can do is report the failure and move on.  Here
                # we must *not* call any traceback construction again,
                # because that would mess up use of %debug later on.  So we
                # simply report the failure and move on.  The only
                # limitation will be that this frame won't have locals
                # listed in the call signature.  Quite subtle problem...
                # I can't think of a good way to validate this in a unit
                # test, but running a script consisting of:
                #  dict( (k,v.strip()) for (k,v) in range(10) )
                # will illustrate the error, if this exception catch is
                # disabled.
                call = tpl_call_fail % func

        # Don't attempt to tokenize binary files.
        if file.endswith(('.so', '.pyd', '.dll')):
            return '%s %s\n' % (link, call)

        elif file.endswith(('.pyc', '.pyo')):
            # Look up the corresponding source file.
            try:
                file = source_from_cache(file)
            except ValueError:
                # Failed to get the source file for some reason
                # E.g. https://github.com/ipython/ipython/issues/9486
                return '%s %s\n' % (link, call)

        def linereader(file=file, lnum=[lnum], getline=linecache.getline):
            line = getline(file, lnum[0])
            lnum[0] += 1
            return line

        # Build the list of names on this line of code where the exception
        # occurred.
        try:
            names = []
            name_cont = False

            for token_type, token, start, end, line in generate_tokens(linereader):
                # build composite names
                if token_type == tokenize.NAME and token not in keyword.kwlist:
                    if name_cont:
                        # Continuation of a dotted name
                        try:
                            names[-1].append(token)
                        except IndexError:
                            names.append([token])
                        name_cont = False
                    else:
                        # Regular new names.  We append everything, the caller
                        # will be responsible for pruning the list later.  It's
                        # very tricky to try to prune as we go, b/c composite
                        # names can fool us.  The pruning at the end is easy
                        # to do (or the caller can print a list with repeated
                        # names if so desired.
                        names.append([token])
                elif token == '.':
                    name_cont = True
                elif token_type == tokenize.NEWLINE:
                    break

        except (IndexError, UnicodeDecodeError, SyntaxError):
            # signals exit of tokenizer
            # SyntaxError can occur if the file is not actually Python
            #  - see gh-6300
            pass
        except tokenize.TokenError as msg:
            # Tokenizing may fail for various reasons, many of which are
            # harmless. (A good example is when the line in question is the
            # close of a triple-quoted string, cf gh-6864). We don't want to
            # show this to users, but want make it available for debugging
            # purposes.
            _m = ("An unexpected error occurred while tokenizing input\n"
                  "The following traceback may be corrupted or invalid\n"
                  "The error message is: %s\n" % msg)
            debug(_m)

        # Join composite names (e.g. "dict.fromkeys")
        names = ['.'.join(n) for n in names]
        # prune names list of duplicates, but keep the right order
        unique_names = uniq_stable(names)

        # Start loop over vars
        lvals = ''
        lvals_list = []
        if self.include_vars:
            for name_full in unique_names:
                name_base = name_full.split('.', 1)[0]
                if name_base in frame.f_code.co_varnames:
                    if name_base in locals_:
                        try:
                            value = repr(eval(name_full, locals_))
                        except:
                            value = undefined
                    else:
                        value = undefined
                    name = tpl_local_var % name_full
                else:
                    if name_base in frame.f_globals:
                        try:
                            value = repr(eval(name_full, frame.f_globals))
                        except:
                            value = undefined
                    else:
                        value = undefined
                    name = tpl_global_var % name_full
                lvals_list.append(tpl_name_val % (name, value))
        if lvals_list:
            lvals = '%s%s' % (indent, em_normal.join(lvals_list))

        level = '%s %s\n' % (link, call)

        if index is None:
            return level
        else:
            _line_format = PyColorize.Parser(style=col_scheme, parent=self).format2
            return '%s%s' % (level, ''.join(
                _format_traceback_lines(lnum, index, lines, Colors, lvals,
                                         _line_format)))

    def prepare_header(self, etype, long_version=False):
        colors = self.Colors  # just a shorthand + quicker name lookup
        colorsnormal = colors.Normal  # used a lot
        exc = '%s%s%s' % (colors.excName, etype, colorsnormal)
        width = min(75, get_terminal_size()[0])
        if long_version:
            # Header with the exception type, python version, and date
            pyver = 'Python ' + sys.version.split()[0] + ': ' + sys.executable
            date = time.ctime(time.time())

            head = '%s%s%s\n%s%s%s\n%s' % (colors.topline, '-' * width, colorsnormal,
                                           exc, ' ' * (width - len(str(etype)) - len(pyver)),
                                           pyver, date.rjust(width) )
            head += "\nA problem occurred executing Python code.  Here is the sequence of function" \
                    "\ncalls leading up to the error, with the most recent (innermost) call last."
        else:
            # Simplified header
            head = '%s%s' % (exc, 'Traceback (most recent call last)'. \
                             rjust(width - len(str(etype))) )

        return head

    def format_exception(self, etype, evalue):
        colors = self.Colors  # just a shorthand + quicker name lookup
        colorsnormal = colors.Normal  # used a lot
        # Get (safely) a string form of the exception info
        try:
            etype_str, evalue_str = map(str, (etype, evalue))
        except:
            # User exception is improperly defined.
            etype, evalue = str, sys.exc_info()[:2]
            etype_str, evalue_str = map(str, (etype, evalue))
        # ... and format it
        return ['%s%s%s: %s' % (colors.excName, etype_str,
                                colorsnormal, py3compat.cast_unicode(evalue_str))]

    def format_exception_as_a_whole(self, etype, evalue, etb, number_of_lines_of_context, tb_offset):
        """Formats the header, traceback and exception message for a single exception.

        This may be called multiple times by Python 3 exception chaining
        (PEP 3134).
        """
        # some locals
        orig_etype = etype
        try:
            etype = etype.__name__
        except AttributeError:
            pass

        tb_offset = self.tb_offset if tb_offset is None else tb_offset
        head = self.prepare_header(etype, self.long_header)
        records = self.get_records(etb, number_of_lines_of_context, tb_offset)


        last_unique, recursion_repeat = find_recursion(orig_etype, evalue, records)

        frames = self.format_records(records, last_unique, recursion_repeat)

        formatted_exception = self.format_exception(etype, evalue)
        if records:
            filepath, lnum = records[-1][1:3]
            filepath = os.path.abspath(filepath)
            ipinst = get_ipython()
            if ipinst is not None:
                ipinst.hooks.synchronize_with_editor(filepath, lnum, 0)

        return [[head] + frames + [''.join(formatted_exception[0])]]

    def get_records(self, etb, number_of_lines_of_context, tb_offset):
        try:
            # Try the default getinnerframes and Alex's: Alex's fixes some
            # problems, but it generates empty tracebacks for console errors
            # (5 blanks lines) where none should be returned.
            return _fixed_getinnerframes(etb, number_of_lines_of_context, tb_offset)
        except UnicodeDecodeError:
            # This can occur if a file's encoding magic comment is wrong.
            # I can't see a way to recover without duplicating a bunch of code
            # from the stdlib traceback module. --TK
            error('\nUnicodeDecodeError while processing traceback.\n')
            return None
        except:
            # FIXME: I've been getting many crash reports from python 2.3
            # users, traceable to inspect.py.  If I can find a small test-case
            # to reproduce this, I should either write a better workaround or
            # file a bug report against inspect (if that's the real problem).
            # So far, I haven't been able to find an isolated example to
            # reproduce the problem.
            inspect_error()
            traceback.print_exc(file=self.ostream)
            info('\nUnfortunately, your original traceback can not be constructed.\n')
            return None

    def structured_traceback(self, etype, evalue, etb, tb_offset=None,
                             number_of_lines_of_context=5):
        """Return a nice text document describing the traceback."""

        formatted_exception = self.format_exception_as_a_whole(etype, evalue, etb, number_of_lines_of_context,
                                                               tb_offset)

        colors = self.Colors  # just a shorthand + quicker name lookup
        colorsnormal = colors.Normal  # used a lot
        head = '%s%s%s' % (colors.topline, '-' * min(75, get_terminal_size()[0]), colorsnormal)
        structured_traceback_parts = [head]
        chained_exceptions_tb_offset = 0
        lines_of_context = 3
        formatted_exceptions = formatted_exception
        exception = self.get_parts_of_chained_exception(evalue)
        if exception:
            formatted_exceptions += self.prepare_chained_exception_message(evalue.__cause__)
            etype, evalue, etb = exception
        else:
            evalue = None
        chained_exc_ids = set()
        while evalue:
            formatted_exceptions += self.format_exception_as_a_whole(etype, evalue, etb, lines_of_context,
                                                                     chained_exceptions_tb_offset)
            exception = self.get_parts_of_chained_exception(evalue)

            if exception and not id(exception[1]) in chained_exc_ids:
                chained_exc_ids.add(id(exception[1])) # trace exception to avoid infinite 'cause' loop
                formatted_exceptions += self.prepare_chained_exception_message(evalue.__cause__)
                etype, evalue, etb = exception
            else:
                evalue = None

        # we want to see exceptions in a reversed order:
        # the first exception should be on top
        for formatted_exception in reversed(formatted_exceptions):
            structured_traceback_parts += formatted_exception

        return structured_traceback_parts

    def debugger(self, force=False):
        """Call up the pdb debugger if desired, always clean up the tb
        reference.

        Keywords:

          - force(False): by default, this routine checks the instance call_pdb
            flag and does not actually invoke the debugger if the flag is false.
            The 'force' option forces the debugger to activate even if the flag
            is false.

        If the call_pdb flag is set, the pdb interactive debugger is
        invoked. In all cases, the self.tb reference to the current traceback
        is deleted to prevent lingering references which hamper memory
        management.

        Note that each call to pdb() does an 'import readline', so if your app
        requires a special setup for the readline completers, you'll have to
        fix that by hand after invoking the exception handler."""

        if force or self.call_pdb:
            if self.pdb is None:
                self.pdb = self.debugger_cls()
            # the system displayhook may have changed, restore the original
            # for pdb
            display_trap = DisplayTrap(hook=sys.__displayhook__)
            with display_trap:
                self.pdb.reset()
                # Find the right frame so we don't pop up inside ipython itself
                if hasattr(self, 'tb') and self.tb is not None:
                    etb = self.tb
                else:
                    etb = self.tb = sys.last_traceback
                while self.tb is not None and self.tb.tb_next is not None:
                    self.tb = self.tb.tb_next
                if etb and etb.tb_next:
                    etb = etb.tb_next
                self.pdb.botframe = etb.tb_frame
                self.pdb.interaction(None, etb)

        if hasattr(self, 'tb'):
            del self.tb

    def handler(self, info=None):
        (etype, evalue, etb) = info or sys.exc_info()
        self.tb = etb
        ostream = self.ostream
        ostream.flush()
        ostream.write(self.text(etype, evalue, etb))
        ostream.write('\n')
        ostream.flush()

    # Changed so an instance can just be called as VerboseTB_inst() and print
    # out the right info on its own.
    def __call__(self, etype=None, evalue=None, etb=None):
        """This hook can replace sys.excepthook (for Python 2.1 or higher)."""
        if etb is None:
            self.handler()
        else:
            self.handler((etype, evalue, etb))
        try:
            self.debugger()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")


#----------------------------------------------------------------------------
class FormattedTB(VerboseTB, ListTB):
    """Subclass ListTB but allow calling with a traceback.

    It can thus be used as a sys.excepthook for Python > 2.1.

    Also adds 'Context' and 'Verbose' modes, not available in ListTB.

    Allows a tb_offset to be specified. This is useful for situations where
    one needs to remove a number of topmost frames from the traceback (such as
    occurs with python programs that themselves execute other python code,
    like Python shells).  """

    def __init__(self, mode='Plain', color_scheme='Linux', call_pdb=False,
                 ostream=None,
                 tb_offset=0, long_header=False, include_vars=False,
                 check_cache=None, debugger_cls=None,
                 parent=None, config=None):

        # NEVER change the order of this list. Put new modes at the end:
        self.valid_modes = ['Plain', 'Context', 'Verbose', 'Minimal']
        self.verbose_modes = self.valid_modes[1:3]

        VerboseTB.__init__(self, color_scheme=color_scheme, call_pdb=call_pdb,
                           ostream=ostream, tb_offset=tb_offset,
                           long_header=long_header, include_vars=include_vars,
                           check_cache=check_cache, debugger_cls=debugger_cls,
                           parent=parent, config=config)

        # Different types of tracebacks are joined with different separators to
        # form a single string.  They are taken from this dict
        self._join_chars = dict(Plain='', Context='\n', Verbose='\n',
                                Minimal='')
        # set_mode also sets the tb_join_char attribute
        self.set_mode(mode)

    def structured_traceback(self, etype, value, tb, tb_offset=None, number_of_lines_of_context=5):
        tb_offset = self.tb_offset if tb_offset is None else tb_offset
        mode = self.mode
        if mode in self.verbose_modes:
            # Verbose modes need a full traceback
            return VerboseTB.structured_traceback(
                self, etype, value, tb, tb_offset, number_of_lines_of_context
            )
        elif mode == 'Minimal':
            return ListTB.get_exception_only(self, etype, value)
        else:
            # We must check the source cache because otherwise we can print
            # out-of-date source code.
            self.check_cache()
            # Now we can extract and format the exception
            return ListTB.structured_traceback(
                self, etype, value, tb, tb_offset, number_of_lines_of_context
            )

    def stb2text(self, stb):
        """Convert a structured traceback (a list) to a string."""
        return self.tb_join_char.join(stb)


    def set_mode(self, mode=None):
        """Switch to the desired mode.

        If mode is not specified, cycles through the available modes."""

        if not mode:
            new_idx = (self.valid_modes.index(self.mode) + 1 ) % \
                      len(self.valid_modes)
            self.mode = self.valid_modes[new_idx]
        elif mode not in self.valid_modes:
            raise ValueError('Unrecognized mode in FormattedTB: <' + mode + '>\n'
                                                                            'Valid modes: ' + str(self.valid_modes))
        else:
            self.mode = mode
        # include variable details only in 'Verbose' mode
        self.include_vars = (self.mode == self.valid_modes[2])
        # Set the join character for generating text tracebacks
        self.tb_join_char = self._join_chars[self.mode]

    # some convenient shortcuts
    def plain(self):
        self.set_mode(self.valid_modes[0])

    def context(self):
        self.set_mode(self.valid_modes[1])

    def verbose(self):
        self.set_mode(self.valid_modes[2])

    def minimal(self):
        self.set_mode(self.valid_modes[3])


#----------------------------------------------------------------------------
class AutoFormattedTB(FormattedTB):
    """A traceback printer which can be called on the fly.

    It will find out about exceptions by itself.

    A brief example::

        AutoTB = AutoFormattedTB(mode = 'Verbose',color_scheme='Linux')
        try:
          ...
        except:
          AutoTB()  # or AutoTB(out=logfile) where logfile is an open file object
    """

    def __call__(self, etype=None, evalue=None, etb=None,
                 out=None, tb_offset=None):
        """Print out a formatted exception traceback.

        Optional arguments:
          - out: an open file-like object to direct output to.

          - tb_offset: the number of frames to skip over in the stack, on a
          per-call basis (this overrides temporarily the instance's tb_offset
          given at initialization time.  """

        if out is None:
            out = self.ostream
        out.flush()
        out.write(self.text(etype, evalue, etb, tb_offset))
        out.write('\n')
        out.flush()
        # FIXME: we should remove the auto pdb behavior from here and leave
        # that to the clients.
        try:
            self.debugger()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")

    def structured_traceback(self, etype=None, value=None, tb=None,
                             tb_offset=None, number_of_lines_of_context=5):
        if etype is None:
            etype, value, tb = sys.exc_info()
        if isinstance(tb, tuple):
            # tb is a tuple if this is a chained exception.
            self.tb = tb[0]
        else:
            self.tb = tb
        return FormattedTB.structured_traceback(
            self, etype, value, tb, tb_offset, number_of_lines_of_context)


#---------------------------------------------------------------------------

# A simple class to preserve Nathan's original functionality.
class ColorTB(FormattedTB):
    """Shorthand to initialize a FormattedTB in Linux colors mode."""

    def __init__(self, color_scheme='Linux', call_pdb=0, **kwargs):
        FormattedTB.__init__(self, color_scheme=color_scheme,
                             call_pdb=call_pdb, **kwargs)


class SyntaxTB(ListTB):
    """Extension which holds some state: the last exception value"""

    def __init__(self, color_scheme='NoColor', parent=None, config=None):
        ListTB.__init__(self, color_scheme, parent=parent, config=config)
        self.last_syntax_error = None

    def __call__(self, etype, value, elist):
        self.last_syntax_error = value

        ListTB.__call__(self, etype, value, elist)

    def structured_traceback(self, etype, value, elist, tb_offset=None,
                             context=5):
        # If the source file has been edited, the line in the syntax error can
        # be wrong (retrieved from an outdated cache). This replaces it with
        # the current value.
        if isinstance(value, SyntaxError) \
                and isinstance(value.filename, str) \
                and isinstance(value.lineno, int):
            linecache.checkcache(value.filename)
            newtext = linecache.getline(value.filename, value.lineno)
            if newtext:
                value.text = newtext
        self.last_syntax_error = value
        return super(SyntaxTB, self).structured_traceback(etype, value, elist,
                                                          tb_offset=tb_offset, context=context)

    def clear_err_state(self):
        """Return the current error state and clear it"""
        e = self.last_syntax_error
        self.last_syntax_error = None
        return e

    def stb2text(self, stb):
        """Convert a structured traceback (a list) to a string."""
        return ''.join(stb)


# some internal-use functions
def text_repr(value):
    """Hopefully pretty robust repr equivalent."""
    # this is pretty horrible but should always return *something*
    try:
        return pydoc.text.repr(value)
    except KeyboardInterrupt:
        raise
    except:
        try:
            return repr(value)
        except KeyboardInterrupt:
            raise
        except:
            try:
                # all still in an except block so we catch
                # getattr raising
                name = getattr(value, '__name__', None)
                if name:
                    # ick, recursion
                    return text_repr(name)
                klass = getattr(value, '__class__', None)
                if klass:
                    return '%s instance' % text_repr(klass)
            except KeyboardInterrupt:
                raise
            except:
                return 'UNRECOVERABLE REPR FAILURE'


def eqrepr(value, repr=text_repr):
    return '=%s' % repr(value)


def nullrepr(value, repr=text_repr):
    return ''
