from kitchensink.models import FormContent
from kitchensink.utils.auth import secure
from .base import CMSBaseView


@secure
class FormContentView(CMSBaseView):
    template_name = "kitchensink/form-content.html"
    model = FormContent

    def test_model_instance_exists(self, request, *args, **kwargs):
        FormContent.objects.get(id=kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = kwargs["id"]

        return context


@secure
class FormContentNewView(CMSBaseView):
    template_name = "kitchensink/form-content.html"
    model = FormContent

    def test_model_instance_exists(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
