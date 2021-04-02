from kitchensink.models import ArchieDoc
from kitchensink.utils.auth import secure
from .base import CMSBaseView


@secure
class ArchieDocView(CMSBaseView):
    template_name = "kitchensink/archie_doc.html"
    model = ArchieDoc

    def test_model_instance_exists(self, request, *args, **kwargs):
        ArchieDoc.objects.get(id=kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archie"] = kwargs["id"]

        return context
