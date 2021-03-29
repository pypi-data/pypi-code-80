import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'derezzed'
copyright = '2021, Iain Learmonth'
author = 'Iain Learmonth'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc'
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
