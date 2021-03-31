from django.contrib import admin
from .models import Supervisor, SupervisorTenant


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    """Administrative view for Supervisor."""
    list_display = ('sid', 'name', 'email', 'phone', 'status', 'comments', 'is_active')
    save_on_top = True
    save_as = True


# @admin.register(SupervisorTenant)
# class SupervisorTenantAdmin(admin.ModelAdmin):
#     """Administrative view for SupervisorTenant."""
#     list_display = ('tenant')
#     fieldsets = (
#         (None, {
#             'fields': ('supervisor', 'tenant', )}),
#         #
#         # (None, {
#         #     'fields':
#         #         ('tenant')
#     )
#     save_on_top = True
#     save_as = True