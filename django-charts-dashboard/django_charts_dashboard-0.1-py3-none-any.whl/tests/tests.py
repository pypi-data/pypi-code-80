import json
from django.test import TestCase
from charts.objects import BarChart, PieChart, HorizontalBarChart


class TestCaseChart(TestCase):

    def test_should_return_barchart_data(self):
        chart = BarChart()
        chart.title = "Example charts title"

        chart.labels = ["test 1", "test 2", "test 3", "test 4"]
        chart.data = [2, 3, 10, 6]
        chart.data_label = "Test"

        data = chart.build_chart()
        options = chart.generate_options()

        assert data == expected_data(chart, options)

    def test_should_return_horizontal_barchart_data(self):
        chart = HorizontalBarChart()
        chart.title = "Example charts title"

        chart.labels = ["test 1", "test 2", "test 3", "test 4"]
        chart.data = [2, 3, 10, 6]
        chart.data_label = "Test"

        data = chart.build_chart()
        options = chart.generate_options()

        assert data == expected_data(chart, options)

    def test_should_return_piechart_data(self):
        chart = PieChart()
        chart.title = "Example charts title"

        chart.labels = ["test 1", "test 2", "test 3", "test 4"]
        chart.data = [2, 3, 10, 6]
        chart.data_label = "Test"

        data = chart.build_chart()
        options = chart.generate_options()

        assert data == expected_pie_data(chart, options)

def expected_data(chart, options):
    return json.dumps({
        "type": chart.type_chart,
        "data": {
            "labels": [label for label in chart.labels],
            "datasets": [
                {
                    "label": chart.data_label,
                    "backgroundColor": [color for color in chart.get_colors],
                    "data": [value for value in chart.data]
                }
            ]
        },
        "options": {
            "responsive": options["responsive"],
            "maintainAspectRatio": options["maintainAspectRatio"],
            "legend": {
                "display": chart.legend,
            },
            "title": {
                "fontSize": 14,
                "display": True if chart.title else False,
                "text": chart.title if chart.title else ""
            },
            "scales": {
                "yAxes": [
                    {
                        "display": True,
                        "ticks": {
                            "beginAtZero": chart.begin_at_zero,
                            "stepSize": chart.step_size
                        }
                    }
                ]
            }
        }
    }, ensure_ascii=False)

def expected_pie_data(chart, options):
    return json.dumps({
        "type": chart.type_chart,
        "data": {
            "labels": [label for label in chart.labels],
            "datasets": [
                {
                    "label": chart.data_label,
                    "backgroundColor": [color for color in chart.get_colors],
                    "data": [value for value in chart.data]
                }
            ]
        },
        "options": {
            "responsive": options["responsive"],
            "maintainAspectRatio": options["maintainAspectRatio"],
            "legend": {
                "display": chart.legend,
                "position": chart.position,
            },
            "title": {
                "fontSize": 14,
                "display": True if chart.title else False,
                "text": chart.title if chart.title else ""
            },
        }
    }, ensure_ascii=False)
