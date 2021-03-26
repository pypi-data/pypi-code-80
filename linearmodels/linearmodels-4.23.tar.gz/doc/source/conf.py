#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# linearmodels documentation build configuration file, created by
# sphinx-quickstart on Thu Feb 16 13:04:40 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.


#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from distutils.version import LooseVersion
import glob
import hashlib
import os
from typing import Dict, List

import sphinx_material

import linearmodels

# ...

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "numpydoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.doctest",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "nbsphinx",
    "sphinx_material",
]

try:
    import sphinxcontrib.spelling  # noqa: F401
except ImportError as err:  # noqa: F841
    pass
else:
    extensions.append("sphinxcontrib.spelling")

spelling_word_list_filename = ["spelling_wordlist.txt", "names_wordlist.txt"]
spelling_ignore_pypi_package_names = True

add_module_names = False

# Copy over notebooks from examples to docs for build
files = glob.glob("../../examples/*.ipynb") + glob.glob("../../examples/*.png")
for file_to_copy in files:
    full_name = os.path.split(file_to_copy)[-1]
    folder, file_name = full_name.split("_")
    if not file_name.endswith("ipynb"):
        file_name = "_".join((folder, file_name))
    out_dir = os.path.join(folder, "examples")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, file_name)
    existing_hash = ""
    with open(file_to_copy, "rb") as example:
        example_file = example.read()
        example_hash = hashlib.sha512(example_file).hexdigest()
    if os.path.exists(out_file):
        with open(out_file, "rb") as existing:
            existing_hash = hashlib.sha512(existing.read()).hexdigest()
    if existing_hash != example_hash:
        print(f"Copying {file_to_copy} to {out_file}")
        with open(out_file, "wb") as out:
            out.write(example_file)

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "linearmodels"
copyright = "2017, Kevin Sheppard"
author = "Kevin Sheppard"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# The short X.Y version.
loose_version = LooseVersion(linearmodels.__version__)
short_version = version = linearmodels.__version__
if "+" in loose_version.version:
    version = version.replace(".dirty", "")
    version = version.split("+")
    commits, tag = version[1].split(".")
    version = version[0]
    short_tag = " (+{0})".format(commits)
    tag = " (+" + commits + ", " + tag + ")"
    short_version = version + short_tag
    version = version + tag

# The full version, including alpha/beta/rc tags.
release = linearmodels.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns: List[str] = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "colorful"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"
# Adds an HTML table visitor to apply Bootstrap table classes

# sphinx_material theme options (see theme.conf for more information)
html_theme_options = {
    "base_url": "http://bashtage.github.io/linearmodels/",
    "repo_url": "https://github.com/bashtage/linearmodels/",
    "repo_name": "linearmodels",
    # Set the name of the project to appear in the sidebar
    "nav_title": project + " " + short_version,
    "globaltoc_depth": 2,
    "globaltoc_collapse": True,
    "globaltoc_includehidden": True,
    "theme_color": "#2196f3",
    "color_primary": "blue",
    "color_accent": "orange",
    "html_minify": True,
    "css_minify": True,
    "master_doc": False,
    "heroes": {
        "index": "Models for panel data, system regression, instrumental \
        variables and asset pricing."
    },
    "version_dropdown": True,
    "version_info": {
        "Release": "https://bashtage.github.io/linearmodels/",
        "Development": "https://bashtage.github.io/linearmodels/devel/",
    },
}

html_favicon = "images/favicon.ico"
html_logo = "images/bw-logo.svg"

#  Register the theme as an extension to generate a sitemap.xml

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}
# -- Options for HTMLHelp output ------------------------------------------

# -- Options for LaTeX output ---------------------------------------------

latex_elements: Dict[str, str] = {
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
        "linearmodels.tex",
        "linearmodels Documentation",
        "Kevin Sheppard",
        "manual",
    ),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "linearmodels", "linearmodels Documentation", [author], 1)]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "linearmodels",
        "linearmodels Documentation",
        author,
        "linearmodels",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "statsmodels": ("https://www.statsmodels.org/dev/", None),
    "matplotlib": ("https://matplotlib.org/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "xarray": ("https://xarray.pydata.org/en/stable/", None),
}

extlinks = {"issue": ("https://github.com/bashtage/linearmodels/issues/%s", "GH")}


doctest_global_setup = """
import numpy as np
import pandas as pd

entities = ['entity.{0}'.format(i) for i in range(100)]
time = list(range(10))
mi = pd.MultiIndex.from_product((entities,time), names=('entities','time'))
panel_data = pd.DataFrame(np.random.randn(1000,5), index=mi, columns=['y','x1','x2','x3','x4'])
y = panel_data.y
x = panel_data.x1
"""

napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = True

autosummary_generate = True
autoclass_content = "class"

# Create xrefs
numpydoc_use_autodoc_signature = True
numpydoc_xref_param_type = True
numpydoc_class_members_toctree = False
numpydoc_xref_aliases = {
    "Figure": "matplotlib.figure.Figure",
    "Axes": "matplotlib.axes.Axes",
    "AxesSubplot": "matplotlib.axes.Axes",
    "DataFrame": "pandas.DataFrame",
    "Series": "pandas.Series",
    "BetweenOLS": "linearmodels.panel.model.BetweenOLS",
    "FamaMacBeth": "linearmodels.panel.model.FamaMacBeth",
    "FirstDifferenceOLS": "linearmodels.panel.model.FirstDifferenceOLS",
    "IV2SLS": "linearmodels.iv.model.IV2SLS",
    "IV3SLS": "linearmodels.system.model.IV3SLS",
    "IVGMM": "linearmodels.iv.model.IVGMM",
    "IVGMMCUE": "linearmodels.iv.model.IVGMMCUE",
    "IVLIML": "linearmodels.iv.model.IVLIML",
    "IVSystemGMM": "linearmodels.system.model.IVSystemGMM",
    "LinearFactorModel": "linearmodels.asset_pricing.model.LinearFactorModel",
    "LinearFactorModelGMM": "linearmodels.asset_pricing.model.LinearFactorModelGMM",
    "OLS": "linearmodels.iv.model.OLS",
    "PanelOLS": "linearmodels.panel.model.PanelOLS",
    "PooledOLS": "linearmodels.panel.model.PooledOLS",
    "RandomEffects": "linearmodels.panel.model.RandomEffects",
    "SUR": "linearmodels.system.model.SUR",
    "TradedFactorModel": "linearmodels.asset_pricing.model.TradedFactorModel",
    "AbsorbingLSResults": "linearmodels.iv.absorbing.AbsorbingLSResults",
    "FirstStageResults": "linearmodels.iv.results.FirstStageResults",
    "IVGMMResults": "linearmodels.iv.results.IVGMMResults",
    "IVModelComparison": "linearmodels.iv.results.IVModelComparison",
    "IVResults": "linearmodels.iv.results.IVResults",
    "InvalidTestStatistic": "linearmodels.shared.InvalidTestStatistic",
    "OLSResults": "linearmodels.iv.results.OLSResults",
    "WaldTestStatistic": "linearmodels.shared.WaldTestStatistic",
    "PanelEffectsResults": "linearmodels.panel.results.PanelEffectsResults",
    "PanelModelComparison": "linearmodels.panel.results.PanelModelComparison",
    "PanelResults": "linearmodels.panel.results.PanelResults",
    "RandomEffectsResults": "linearmodels.panel.results.RandomEffectsResults",
    "GMMSystemResults": "linearmodels.system.results.GMMSystemResults",
    "Summary": "linearmodels.compat.statsmodels.Summary",
    "SystemEquationResult": "linearmodels.system.results.SystemEquationResult",
    "SystemResults": "linearmodels.system.results.SystemResults",
    "GMMFactorModelResults": "linearmodels.asset_pricing.results.GMMFactorModelResults",
    "LinearFactorModelResults": "linearmodels.asset_pricing.results.LinearFactorModelResults",
    "PanelData": "linearmodels.panel.data.PanelData",
    "IVData": "linearmodels.iv.data.IVData",
    "AttrDict": "linearmodels.shared.AttrDict",
}
