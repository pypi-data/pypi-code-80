import json
import random
from abc import ABC, abstractmethod


class BaseChartView(ABC):

    type_chart = None
    title = None
    legend = None
    begin_at_zero = False
    aspect_ratio = True
    step_size = 0.5
    width = 100
    height = 100
    colors = []

    def get_tooltips(self) -> list:
        return []

    @abstractmethod
    def generate_values(self):
        pass

    def generate_options(self):
        return {
            "responsive": True,
            "maintainAspectRatio": self.aspect_ratio,
            "legend": {"display": self.legend},
            "title": {"display": True if self.title else False, "text": self.title},
        }

    @abstractmethod
    def generate_labels(self):
        """
            suggestion: insert colors in self.colors array
            ex.: self.colors = ['#ffff','#121212']
        """
        pass

    def _get_color(self):
        return "#{:02x}{:02x}{:02x}".format(
            *map(lambda x: random.randint(0, 255), range(3))
        )

    def _get_rgba_from_hex(self, color_hex, alpha=0.6):
        color = color_hex.lstrip("#")
        rgb = [int(color[i : i + 2], 16) for i in [0, 2, 4]]

        return "rgba({},{},{}, {})".format(*map(lambda x: x, rgb), alpha)

    def get_context_data(self, **kwargs):
        context = {}
        context["chart"] = json.dumps(
            {
                "type": self.type_chart,
                "data": self.generate_values(),
                "options": self.generate_options(),
            },
            ensure_ascii=False,
        )

        context["tooltips"] = (self.get_tooltips() if self.get_tooltips() else " ",)

        if not self.aspect_ratio:
            context["width"] = self.width
            context["height"] = self.height

        return context


"""
    Objects represent chartjs instances
"""


class ChartObjectMixin(ABC):
    def __init__(self):
        # principal data chart
        self.data = []
        self.labels = []
        self.data_label = ""
        # options values
        self.begin_at_zero = True
        self.aspect_ratio = True
        self.step_size = 0.5
        self.title = None
        self.legend = False
        self.type_chart = None
        self._colors = []
        self.tooltips = []

    @abstractmethod
    def generate_dataset(self):
        pass

    def generate_options(self):
        return {
            "responsive": True,
            "maintainAspectRatio": self.aspect_ratio,
            "legend": {"display": self.legend},
            "title": {
                "fontSize": 14,
                "display": True if self.title else False,
                "text": self.title if self.title else "",
            },
        }

    def _generate_colors(self, labels):
        return [
            "#{:02x}{:02x}{:02x}".format(
                *map(lambda x: random.randint(0, 255), range(3))
            )
            for entry in labels
        ]

    def set_colors(self, colors):
        self._colors = colors

    @property
    def get_colors(self):
        return self._colors

    def _get_color(self):
        return "#{:02x}{:02x}{:02x}".format(
            *map(lambda x: random.randint(0, 255), range(3))
        )

    def _get_rgba_from_hex(self, color_hex):
        color = color_hex.lstrip("#")
        rgb = [int(color[i : i + 2], 16) for i in [0, 2, 4]]

        return "rgba({},{},{},0.6)".format(*map(lambda x: x, rgb))

    def build_chart(self):
        self._colors = (
            self._colors if self._colors else self._generate_colors(self.labels)
        )
        return json.dumps(
            {
                "type": self.type_chart,
                "data": self.generate_dataset(),
                "options": self.generate_options(),
            },
            ensure_ascii=False,
        )
