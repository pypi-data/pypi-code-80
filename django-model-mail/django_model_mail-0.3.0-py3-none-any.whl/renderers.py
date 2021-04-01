from .utils import get_choice_display


class FieldRenderer:
    def __init__(self, field):
        self.field = field

    def render(self, value):
        return f"{self.render_label()}: {self.render_value(value)}"

    def render_label(self):
        return self.field.verbose_name

    def render_value(self, value):
        return value if value else "—"


class ChoiceFieldRenderer(FieldRenderer):
    def render_value(self, value):
        return get_choice_display(self.field, value)
