from django.contrib import admin
from django.http import HttpResponseRedirect
import logging
from jsonschema.exceptions import ValidationError
from kitchensink.models import ArchieDoc, Sheet, Project, FormContent, FormType


class ValidationExceptionMixin:
    """
    Mixin to catch Validation Exceptions in the Django Admin
    and map them to user-visible errors.
    """
    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super().change_view(
                request,
                object_id,
                form_url,
                extra_context
            )
        except ValidationError as e:
            self.message_user(
                request,
                'Validation: %s' % e.message,
                level=logging.ERROR
            )

            return HttpResponseRedirect(request.path)


class ArchieDocAdmin(ValidationExceptionMixin, admin.ModelAdmin):
    fields = (
        "project",
        "title",
        "google_id",
        "favorites",
        "version",
        "validation_schema",
    )


class SheetsAdmin(ValidationExceptionMixin, admin.ModelAdmin):
    fields = (
        "project",
        "title",
        "google_id",
        "favorites",
        "version",
        "validation_schema",
    )


class FormTypeAdmin(admin.ModelAdmin):
    fields = ("title", "json", "ui")


class FormContentAdmin(admin.ModelAdmin):
    fields = ("project", "type", "title", "favorites", "version", "data")


admin.site.register(Sheet, SheetsAdmin)
admin.site.register(ArchieDoc, ArchieDocAdmin)
admin.site.register(Project)
admin.site.register(FormType, FormTypeAdmin)
admin.site.register(FormContent, FormContentAdmin)
