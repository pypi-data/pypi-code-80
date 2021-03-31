from django.contrib import admin

from kitchensink.models import ArchieDoc, Sheet, Project, FormContent, FormType


class ArchieDocAdmin(admin.ModelAdmin):
    fields = (
        "project",
        "title",
        "google_id",
        "favorites",
        "version",
        "validation_schema",
    )


class SheetsAdmin(admin.ModelAdmin):
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
