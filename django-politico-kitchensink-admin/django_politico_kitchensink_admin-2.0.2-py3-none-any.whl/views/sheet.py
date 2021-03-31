from kitchensink.models import Sheet
from kitchensink.utils.auth import secure
from .base import CMSBaseView


@secure
class SheetView(CMSBaseView):
    template_name = "kitchensink/sheet.html"
    model = Sheet

    def test_model_instance_exists(self, request, *args, **kwargs):
        Sheet.objects.get(id=kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sheet"] = kwargs["id"]

        return context
