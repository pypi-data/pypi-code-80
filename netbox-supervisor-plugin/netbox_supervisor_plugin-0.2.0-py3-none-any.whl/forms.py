from django import forms

from utilities.forms import BootstrapMixin, DynamicModelMultipleChoiceField, DynamicModelChoiceField
from tenancy.models import Tenant
from .models import VirtualCircuitStatusChoices, Supervisor, SupervisorTenant

BLANK_CHOICE = (("", "---------"),)


# SUPERVISOR
class SupervisorForm(BootstrapMixin, forms.ModelForm):

    tenant = DynamicModelChoiceField(
        label='Учреждение',
        queryset=Tenant.objects.all(),
        required=False
    )

    class Meta:
        model = Supervisor
        fields = [
            'sid',
            'name',
            'email',
            'phone',
            'tenant',
            'tenants',
            'status',
            'comments',
            'is_active',
        ]


class SupervisorFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(
        required=False,
        label="Поиск",
    )
    status = forms.ChoiceField(
        choices=BLANK_CHOICE + VirtualCircuitStatusChoices.CHOICES,
        label="Статус",
        required=False
    )
    tenant = DynamicModelMultipleChoiceField(
        label='Учреждение',
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None'
    )

    class Meta:
        model = Supervisor
        fields = [
            'q',
            # 'status',
            # 'tenant',
            # 'comments',
        ]


class SupervisorTenantForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = SupervisorTenant
        fields = [
            'supervisor',
            'tenant',
        ]
