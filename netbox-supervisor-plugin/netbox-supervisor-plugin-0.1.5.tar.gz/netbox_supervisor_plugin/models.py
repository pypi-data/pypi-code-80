from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from tenancy.models import Tenant
from extras.models import ChangeLoggedModel

from .choices import VirtualCircuitStatusChoices


class Supervisor(ChangeLoggedModel):
    """Supervisor model."""

    sid = models.CharField(
        verbose_name='Код организации',
        max_length=8,
        unique=True
    )

    tenant = models.ForeignKey(
        to=Tenant,
        on_delete=models.CASCADE,
        related_name='supervisor',
        verbose_name='Основное учреждение',
    )
    tenants = models.ManyToManyField(
        to=Tenant,
        related_name='tenants_all',
        verbose_name='Дополнительные учреждения',
        blank=True
    )

    name = models.CharField(
        max_length=64,
        verbose_name='ФИО',
    )
    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        blank=True
    )
    status = models.CharField(
        max_length=30,
        verbose_name='Роль',
        choices=VirtualCircuitStatusChoices,
        default=VirtualCircuitStatusChoices.STATUS_PENDING_CONFIGURATION,
    )
    comments = models.CharField(
        max_length=100,
        verbose_name='Комментарий',
        blank=True,
    )
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
        ordering = ['sid']
        verbose_name = 'Ответственный'
        verbose_name_plural = 'Ответственные'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_supervisor_plugin:supervisor', args=[self.pk])


class SupervisorTenant(ChangeLoggedModel):
    """Supervisor to Tenant relationship."""

    supervisor = models.ForeignKey(
        to=Supervisor,
        on_delete=models.CASCADE,
        related_name='tenantss',
        verbose_name='Ответственный',
    )

    tenant = models.ForeignKey(
        to=Tenant,
        on_delete=models.CASCADE,
        related_name='supervisors',
        verbose_name='Учреждение',
    )

    class Meta:
        ordering = ['supervisor']
        verbose_name = 'Связь ответственного'
        verbose_name_plural = 'Связи ответственных'

    def get_absolute_url(self):
        return reverse('plugins:netbox_supervisor_plugin:supervisor', args=[self.supervisor.id])


# @receiver(post_save, sender=Supervisor)
# def save_tsup_ten(sender, *args, **kwargs):
#     print('*'*30)
#     superv = Supervisor.objects.all()
#     test = Supervisor.objects.all().order_by('-id')[0]
#     print(test)
#     print(test.id)
#     test = Supervisor.objects.all().last()
#     print(test)
#     print(test.tenant.id)
#     # print(sender)
#     # print(sender.tenant)
#     print('*' * 30)
#     # print(self.id)
#     # tenant = Tenant.objects.filter(pk=self.tenant.id)
#     # print(tenant)
#     SupervisorTenant.objects.create(supervisor_id=test.id,
#                                     tenant_id=test.tenant.id)
