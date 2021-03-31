from django.urls import reverse

from kitchensink.models import FormType
from kitchensink.utils.auth import secure
from .base import CMSBaseView


@secure
class FormTypeView(CMSBaseView):
    template_name = "kitchensink/form-type.html"
    model = FormType

    def test_model_instance_exists(self, request, *args, **kwargs):
        FormType.objects.get(id=kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = kwargs["id"]

        return context


@secure
class FormTypeNewView(CMSBaseView):
    template_name = "kitchensink/form-type.html"
    model = FormType

    def test_model_instance_exists(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = {
            "home": {
                "name": "Kitchen Sink",
                "url": reverse("kitchensink:home"),
            }
        }

        return context
