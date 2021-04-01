from django.urls import path
from . import views


urlpatterns = (
    # Supervisor.
    path('', views.SupervisorListView.as_view(), name='supervisor_list'),
    path("add/", views.SupervisorCreateView.as_view(), name='supervisor_add'),
    path("delete/", views.SupervisorBulkDeleteView.as_view(), name='supervisor_bulk_delete'),
    path('<int:pk>/', views.SupervisorView.as_view(), name='supervisor'),
    path('<int:pk>/edit/', views.SupervisorEditView.as_view(), name='supervisor_edit'),
    path('<int:pk>/delete/', views.SupervisorDeleteView.as_view(), name='supervisor_delete'),

    # SupervisorTenant connections.
    path("tenant/", views.SupervisorTenantListView.as_view(), name='supervisor_tenant_list'),
    path("tenant/add/", views.SupervisorTenantCreateView.as_view(), name='supervisor_tenant_add'),
    path("tenant/delete/", views.SupervisorTenantBulkDeleteView.as_view(), name='supervisor_tenant_bulk_delete'),
)
