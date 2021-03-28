import unittest
import parchments
import datetime
import decimal


TEST_INDEX = (
    ('goats', 'int', 0),
    ('price', 'dollar', 2),
    ('value', 'percentage', 4),
    ('names', 'string', 0),
    ('animal', 'bool', 0),
)

PERIOD_DATA = [
    200,
    10000.00,
    0.7000,
    'goaty mc goaterson',
    True,
]

OTHER_PERIOD_DATA = [
    300,
    12000.00,
    0.6000,
    'douglas bahhhhh',
    True,
]

MORE_PERIOD_DATA = [
    400,
    14400.00,
    0.5000,
    'waaaaaaaaah sheep licker',
    False,
]

test_grid = parchments.Grid(TEST_INDEX)
test_grid.add_period(datetime.datetime(2020, 2, 1), PERIOD_DATA)
test_grid.add_period(datetime.datetime(2020, 3, 1), OTHER_PERIOD_DATA)
test_grid.add_period(datetime.datetime(2020, 4, 1), MORE_PERIOD_DATA)
test_grid.project_future(datetime.datetime(2020, 6, 1), 'median')


class TestMedian(unittest.TestCase):

    def test_median_int_gain_value(self):
        print(test_grid.as_dict()['row_data']['goats'][3]['value']['clean'])
        print(test_grid.as_dict()['row_data']['goats'][4]['value']['clean'])
        self.assertTrue(test_grid.as_dict()['row_data']['goats'][3]['value']['clean'] == 566)
        self.assertFalse(test_grid.as_dict()['row_data']['goats'][3]['value']['clean'] == 567)

    def test_median_dollar_gain_value(self):
        print(test_grid.as_dict()['row_data']['price'][3]['value']['clean'])
        print(test_grid.as_dict()['row_data']['price'][4]['value']['clean'])
        self.assertTrue(test_grid.as_dict()['row_data']['price'][3]['value']['clean'] == 17280.00)
        self.assertFalse(test_grid.as_dict()['row_data']['price'][3]['value']['clean'] == 17280.01)

    def test_median_percentage_loss_value(self):
        print(test_grid.as_dict()['row_data']['value'][3]['value']['clean'])
        print(test_grid.as_dict()['row_data']['value'][4]['value']['clean'])
        self.assertTrue(test_grid.as_dict()['row_data']['value'][3]['value']['clean'] == 0.4226)
        self.assertFalse(test_grid.as_dict()['row_data']['value'][3]['value']['clean'] == 0.4225)
