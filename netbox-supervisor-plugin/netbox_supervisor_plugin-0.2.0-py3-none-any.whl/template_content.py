from tenancy.models import Tenant
from extras.plugins import PluginTemplateExtension

from .models import SupervisorTenant, Supervisor


class SupervisorCount(PluginTemplateExtension):
    model = 'tenancy.tenant'

    def right_page(self):
        # Map Supervisor' IDs to Tenants' IDs.
        m = {}
        supervisors = []
        tenants = []
        # Filter Tenants by tenant.
        tenant = Tenant.objects.filter(name=self.context['object'])
        for t in tenant:
            if Supervisor.objects.filter(tenant=t):
                supervisors = [st.id for st in Supervisor.objects.filter(tenant=t)]
                tenants = [st.tenant.id for st in Supervisor.objects.filter(tenant=t)]
            if Supervisor.objects.filter(tenants__in=[t]):
                supervisors_of_this_tenant = Supervisor.objects.filter(tenants__in=[t])
                for supervisor in supervisors_of_this_tenant:
                    supervisors.append(supervisor.id)
                    tenants.append(t.id)
            m = dict(zip(supervisors, tenants))
        return self.render('netbox_supervisor_plugin/supervisor_tenant.html', extra_context={
            'count': len(m),
        })


template_extensions = [SupervisorCount]
