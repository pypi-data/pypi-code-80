#!/usr/bin/env python
# coding: utf-8
"""Test nbextension path."""
# Check that magic function can be imported from package root:
from xai_tabular_widget.xai_tabular_widget.nbextension import _jupyter_nbextension_paths


def test_nbextension_path():
  # Ensure that it can be called without incident:
  path = _jupyter_nbextension_paths()
  # Some sanity checks:
  assert len(path) == 1
  assert isinstance(path[0], dict)
