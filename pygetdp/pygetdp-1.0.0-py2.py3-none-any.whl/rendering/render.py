#!/usr/bin/env python
import os

from pygments import highlight
from pygments.formatters import HtmlFormatter, Terminal256Formatter

from .prolexer import CustomLexer
from .prostyle import ProStyle


def render(
    pro_filename,
    out_filename=None,
    font_size=48,
    formatting="terminal",
    print_output=True,
    font_name=None,
):
    if os.path.isfile(pro_filename):
        if font_name == None:
            font_cmd = ""
        else:
            font_cmd = ",font_name='{}'".format(font_name)
        cmd = "pygmentize -O full,line_numbers=False,style=prostyle{},font_size={} -l pro".format(
            font_cmd, font_size
        )
        if out_filename:
            cmd += " -o {}".format(out_filename)
        cmd += " {}".format(pro_filename)
        os.system(cmd)
    else:
        if formatting == "terminal":
            formatter = Terminal256Formatter(style=ProStyle)
        elif formatting == "html":
            formatter = HtmlFormatter(style=ProStyle)
        else:
            raise Exception("Wrong formatting, choose between html and terminal")
        highlighted_code = highlight(pro_filename, CustomLexer(), formatter)

        if print_output:
            print(highlighted_code)
        return highlighted_code
