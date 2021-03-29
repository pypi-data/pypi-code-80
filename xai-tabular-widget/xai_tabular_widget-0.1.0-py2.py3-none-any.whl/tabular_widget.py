# coding: utf-8

"""The python widget for tabular attribution that will be mapped to the typescript widget."""

from ._frontend import module_name
from ._frontend import module_version
from ipywidgets import DOMWidget
from traitlets import Bool
from traitlets import Dict
from traitlets import Unicode


class TabularWidget(DOMWidget):
  """A class to store the widget's model and view and properties that will be synced."""
  _model_name = Unicode('TabularWidgetModel').tag(sync=True)
  _model_module = Unicode(module_name).tag(sync=True)
  _model_module_version = Unicode(module_version).tag(sync=True)
  _view_name = Unicode('TabularWidgetView').tag(sync=True)
  _view_module = Unicode(module_name).tag(sync=True)
  _view_module_version = Unicode(module_version).tag(sync=True)

  description = Unicode('A widget to visualize tabular attributions.').tag(sync=True)

  _data_url = Unicode('A url for loading data').tag(sync=True)
  _data_str = Unicode('A json string to be loaded').tag(sync=True)
  _data_dict = Dict({}).tag(sync=True)
  ready = Bool(False).tag(sync=True)

  def __init__(self):
    super(TabularWidget, self).__init__()

    self._data_url = ''
    self._data_str = ''
    self._data_dict = {}
    self.ready = False

  def load_data_from_url(self, data_url):
    self._data_url = ''  # resets first to ensure it detects changes
    self._data_url = data_url

  def get_data_url(self):
    return self._data_url

  def load_data_from_json(self, data_str):
    self._data_str = ''  # resets first to ensure it detects changes
    self._data_str = data_str

  def get_data_str(self):
    return self._data_str

  def load_data_from_dict(self, data_dict):
    self._data_dict = {}  # resets first to ensure it detects changes
    self._data_dict = data_dict

  def get_data_dict(self):
    return self._data_dict
