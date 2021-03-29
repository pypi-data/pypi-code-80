import json
import random

from .mixins import ChartObjectMixin


class BarChart(ChartObjectMixin):
    def __init__(self):
        super().__init__()
        self.type_chart = "bar"

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

    def generate_dataset(self):
        return {
            "labels": self.labels,
            "datasets": [
                {
                    "label": self.tooltips
                    if len(self.tooltips) > 0
                    else self.data_label,
                    "backgroundColor": self.get_colors,
                    "data": self.data,
                }
            ],
        }


class HorizontalBarChart(BarChart):
    def __init__(self):
        super().__init__()
        self.type_chart = "horizontalBar"


class PieChart(ChartObjectMixin):
    def __init__(self):
        super().__init__()
        self.type_chart = "pie"
        self.position = "top"  # top,right, bottom, left

    def generate_options(self):
        context = super().generate_options()
        context["legend"].update({"position": self.position})
        return context

    def generate_dataset(self):
        return {
            "labels": self.labels,
            "datasets": [
                {
                    "label": self.data_label if self.data_label else "",
                    "backgroundColor": self.get_colors,
                    "data": self.data,
                }
            ],
        }


class DoughnutChart(PieChart):
    type_chart = "doughnut"


class PolarAreaChart(PieChart):
    type_chart = "polarArea"


class LineChart(ChartObjectMixin):
    def __init__(self):
        super().__init__()
        self.type_chart = "line"

    def create_node(self, label, data, fill=False, color=None):
        """
            this method create special line node, you must pass parameters
            `label` str -> an label individual node, `data`  list -> data render on chart,
            `fill` bool -> default is False, use this to create area chart
            `color` str -> hex color representation (when fill is True)
        """
        color_data = color if color is not None else self._get_color()
        return {
            "data": list(data),
            "label": label,
            "backgroundColor": self._get_rgba_from_hex(color_data),
            "borderColor": color_data,
            "fill": fill,
        }

    def generate_options(self):
        context = super().generate_options()
        context["scales"] = {
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
        return context

    def generate_dataset(self):
        return {"labels": self.labels, "datasets": self.data}

    def build_chart(self):
        return json.dumps(
            {
                "type": self.type_chart,
                "data": self.generate_dataset(),
                "options": self.generate_options(),
            },
            ensure_ascii=False,
        )


class GroupChart(ChartObjectMixin):
    def __init__(self):
        super().__init__()
        self.type_chart = "bar"

    def create_node(self, label, data, color=None):
        """
            This method create an special node to group chart:
            `label` -> (str) text to represent individual data
            `data` -> (list) data to render in chart
            `color` -> (str) hex string representation of color, default is None
        """
        color_data = color if color is not None else self._get_color()
        return {"label": label, "backgroundColor": color_data, "data": list(data)}

    def generate_dataset(self):
        dataset = {"labels": self.labels, "datasets": self.data}

    def build_chart(self):
        return json.dumps(
            {
                "type": self.type_chart,
                "data": self.generate_dataset(),
                "options": self.generate_options(),
            },
            ensure_ascii=False,
        )


class RadarChart(ChartObjectMixin):
    def __init__(self):
        super().__init__()
        self.type_chart = "radar"

    def create_node(self, label, data, color=None):
        color_data = color if color is not None else self._get_rgba_from_hex(color)
        return {
            "label": label,
            "fill": True,
            "backgroundColor": color_data,
            "borderColor": color,
            "pointBorderColor": "#fff",
            "pointBackgroundColor": color,
            "data": list(data),
        }

    def generate_dataset(self):
        return {"labels": self.labels, "datasets": self.data}

    def build_chart(self):
        return json.dumps(
            {
                "type": self.type_chart,
                "data": self.generate_dataset(),
                "options": self.generate_options(),
            },
            ensure_ascii=False,
        )
