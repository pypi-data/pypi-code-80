from django.http import Http404
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.conf import settings
from kitchensink.utils.auth import secure
from django.contrib.auth.mixins import UserPassesTestMixin


@secure
class CMSBaseView(UserPassesTestMixin, TemplateView):
    model = None

    def setup(self, request, *args, **kwargs):
        if self.model:
            self.test_model_instance_exists(request, *args, **kwargs)
            try:
                self.test_model_instance_exists(request, *args, **kwargs)
            except:
                raise Http404("No {} found.".format(self.model.__name__))

        return super().setup(request, *args, **kwargs)

    def test_func(self):
        """
        Used with the UserPassesTestMixin.
        """
        # if not hasattr(self, "required_role"):
        #     return True

        # u = User.get_from_user(self.request.user)
        # if u is None:
        #     return False

        # return u.role == self.required_role or u.role == "ADM"
        return True

    def test_model_instance_exists():
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = []
        context["user"] = self.request.user
        context["API_TOKEN"] = settings.KITCHENSINK_API_TOKEN
        context["API_ROOT"] = reverse_lazy("kitchensink:api:apiv1:api-root")
        context["APP_ROOT"] = reverse_lazy("kitchensink:home")

        context["SERVICES_TOKEN"] = settings.KITCHENSINK_SERVICES_TOKEN

        return context
