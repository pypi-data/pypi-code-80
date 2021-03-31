from django.urls import reverse


from kitchensink.utils.auth import secure
from .base import CMSBaseView


@secure
class Home(CMSBaseView):
    template_name = "kitchensink/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = {
            "home": {
                "name": "Kitchen Sink",
                "url": reverse("kitchensink:home"),
            }
        }

        return context
