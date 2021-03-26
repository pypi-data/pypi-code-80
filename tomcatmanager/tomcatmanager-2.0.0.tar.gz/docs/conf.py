#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# -- General configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"


project = "tomcatmanager"
copyright = ""
author = ""
html_show_copyright = False

# get the version and release via setuptools_scm
from pkg_resources import get_distribution

release = get_distribution("tomcatmanager").version
version = ".".join(release.split(".")[:2])

import sphinx_rtd_theme

# ignore nitpicky references to standard library stuff
nitpick_ignore = [("py:exc", "ValueError")]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# when we autodoc classes, show the methods in the order they are in the
# source
autodoc_member_order = "bysource"

# Make the default role of ` try to link to anything it can find.
# This allows for cleaner docstrings which still get linked when
# we build the documentation.
default_role = "any"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
# exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "prev_next_buttons_location": "both",
    "navigation_depth": 2,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "tomcatmanagerdoc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "tomcatmanager.tex",
        "tomcatmanager Documentation",
        "Jared Crapo",
        "manual",
    ),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "tomcatmanager", "tomcatmanager Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "tomcatmanager",
        "tomcatmanager Documentation",
        author,
        "tomcatmanager",
        "One line description of project.",
        "Miscellaneous",
    ),
]
