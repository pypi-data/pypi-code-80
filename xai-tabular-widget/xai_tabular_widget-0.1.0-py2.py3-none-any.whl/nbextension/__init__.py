#!/usr/bin/env python
# coding: utf-8
"""Set notebook extension paths."""


def _jupyter_nbextension_paths():
  return [{
      'section': 'notebook',
      'src': 'nbextension/static',
      'dest': '{{ cookiecutter.python_package_name }}',
      'require': '{{ cookiecutter.python_package_name }}/extension'
  }]
