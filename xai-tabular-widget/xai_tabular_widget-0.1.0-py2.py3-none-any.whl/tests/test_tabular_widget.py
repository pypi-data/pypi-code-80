#!/usr/bin/env python
# coding: utf-8
"""Testing the widget."""

import json

from ..tabular_widget import TabularWidget

mock_data_dict = {
    'output_name': 'duration',
    'baseline_score': 13.988130569458008,
    'example_score': 17.95456886291504,
    'label_index': 0,
    'attributions': {
        'start_hr': [0.0],
        'weekday': [-0.05342555791139603],
        'euclidean': [4.390988060249646],
        'temp': [-0.0936920156327119],
        'dew_point': [-0.14339413940906542],
        'wdsp': [-0.0],
        'max_temp': [-0.13253182758112966],
        'fog': [-0.0, 2.0, 3.0],
        'prcp': [-0.0, -1.0],
        'rain_drizzle': [-1.5763989408]
    },
    'approx_error': 0.00037974276745948894
}

mock_data_str = json.dumps(mock_data_dict)


def test_tabular_widget_creation_blank():
  w = TabularWidget()
  assert w.description == 'A widget to visualize tabular attributions.'


def test_tabular_widget_data_url():
  w = TabularWidget()
  assert not w.get_data_url()
  w.load_data_from_url(
      'http://localhost:8888/tree/examples/example_attributions.json')
  assert w.get_data_url(
  ) == 'http://localhost:8888/tree/examples/example_attributions.json'


def test_tabular_widget_data_json():
  w = TabularWidget()
  assert not w.get_data_str()
  w.load_data_from_json(mock_data_str)
  assert w.get_data_str() == mock_data_str


def test_tabular_widget_data_dict():
  w = TabularWidget()
  assert not w.get_data_dict()
  w.load_data_from_dict(mock_data_dict)
  assert w.get_data_dict() == mock_data_dict
