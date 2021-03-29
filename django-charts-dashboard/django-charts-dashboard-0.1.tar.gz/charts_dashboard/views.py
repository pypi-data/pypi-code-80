import json
import random

from .mixins import BaseChartView


class BarChartView(BaseChartView):

    type_chart = "bar"

    def _generate_data(self):
        return {
            "labels": self.generate_labels(),
            "datasets": self._generate_dataset(self.generate_values()),
        }

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [
                {
                    "display": True,
                    "ticks": {
                        "beginAtZero": self.begin_at_zero,
                        "stepSize": self.step_size,
                    },
                }
            ]
        }

        return options

    def _generate_dataset(self, values: list):
        collection = []
        dataset = {
            "label": self.get_tooltips() if self.get_tooltips() else "",
            "backgroundColor": [self._get_color()] * len(values)
            if not self.colors
            else self.colors,
            "data": values,
        }
        collection.append(dataset)

        return collection


class RadarChartView(BaseChartView):

    type_chart = "radar"

    def generate_labels(self):
        return []

    def generate_values(self):
        return []

    def create_node(self, label, data, color=None):
        color_data = color if color is not None else self._get_color()
        return {
            "label": label,
            "fill": True,
            "backgroundColor": self._get_rgba_from_hex(color_data),
            "borderColor": color_data,
            "pointBorderColor": "#fff",
            "pointBackgroundColor": color_data,
            "data": list(data),
        }

    def _generate_data(self):
        return {"labels": self.generate_labels(), "datasets": self.generate_values()}


class LineChartView(BaseChartView):

    type_chart = "line"

    """
        the params accept `label` string, and `data` list of values (numeric)
        fill is False to default
    """

    def create_node(self, label, data, fill=False, color=None):
        color_data = color if color is not None else self._get_color()
        return {
            "data": list(data),
            "label": label,
            "borderColor": color_data,
            "backgroundColor": self._get_rgba_from_hex(color_data),
            "fill": fill,
        }

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [
                {
                    "display": True,
                    "ticks": {
                        "beginAtZero": self.begin_at_zero,
                        "stepSize": self.step_size,
                    },
                }
            ]
        }
        return json.dumps(options, ensure_ascii=False)

    def _get_color(self):
        return "rgba({},{},{},0.4)".format(
            *map(lambda x: random.randint(0, 255), range(5))
        )

    def _generate_data(self):
        return json.dumps(
            {"labels": self.generate_labels(), "datasets": self.generate_values()},
            ensure_ascii=False,
        )


class GroupChartView(BaseChartView):

    type_bar = "bar"

    def create_node(self, data, label):
        return {
            "label": label,
            "backgroundColor": "#{:02x}{:02x}{:02x}".format(
                *map(lambda x: random.randint(0, 255), range(3))
            ),
            "data": list(data),
        }

    def _generate_data(self):
        return json.dumps(
            {"labels": self.generate_labels(), "datasets": self.generate_values()},
            ensure_ascii=False,
        )


class HorizontalBarChartView(BarChartView):
    type_chart = "horizontalBar"


class PolarAreaChartView(BarChartView):
    type_chart = "polarArea"


class PieChartView(BarChartView):
    type_chart = "pie"
    position = "top"  # top,right, bottom, left

    def generate_options(self):
        options = {
            "legend": {"display": self.legend, "position": self.position},
            "title": {
                "display": True if self.title is not None else False,
                "text": self.title,
            },
        }

        return json.dumps(options, ensure_ascii=False)

    def get_legend_text(self):
        return ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["legend"] = self.get_legend_text()
        return context


class DoughnutChartView(PieChartView):
    type_chart = "doughnut"
