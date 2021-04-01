from .renderers import ChoiceFieldRenderer, FieldRenderer


class MailRenderersLibrary:
    def __init__(self):
        self.storage = {}

    def register(self, model_field):
        def dec(renderer):
            self.storage[model_field] = renderer
            return renderer

        return dec

    def get_renderer(self, field):
        if field.choices:
            return ChoiceFieldRenderer(field)
        try:
            return self.storage[type(field)](field)
        except KeyError:
            return FieldRenderer(field)


renderers_library = MailRenderersLibrary()
