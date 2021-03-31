from tenancy.models import Tenant
from extras.plugins import PluginTemplateExtension

from .models import SupervisorTenant, Supervisor


class SupervisorCount(PluginTemplateExtension):
    model = 'tenancy.tenant'

    def right_page(self):
        # Map Supervisor' IDs to Tenants' IDs.
        m = {}
        # Filter Tenants by tenant.
        tenants = Tenant.objects.filter(name=self.context['object'])
        for t in tenants:
            # If a Tenant is presented, map back to its Supervisor to prevent duplicates.
            # if SupervisorTenant.objects.filter(tenant=t).count() == 1:
            #     stenant = SupervisorTenant.objects.get(tenant=t)
            #     m[stenant.supervisor.id] = stenant.tenant.id
            #
            # elif SupervisorTenant.objects.filter(tenant=t).count() > 1:
            #     stenants = [st.supervisor.id for st in SupervisorTenant.objects.filter(tenant=t)]
            #     ttenants = [st.tenant.id for st in SupervisorTenant.objects.filter(tenant=t)]
            #     m = dict(zip(stenants, ttenants))
            print(t)
            if Supervisor.objects.filter(tenant=t):
                # super = Supervisor.objects.filter(tenant=t)
                tr = Supervisor.objects.filter(tenant=t)
                print(tr)
                stenants = [st.id for st in Supervisor.objects.filter(tenant=t)]
                ttenants = [st.tenant.id for st in Supervisor.objects.filter(tenant=t)]
                print(stenants)
                print(ttenants)
                m = dict(zip(stenants, ttenants))
                print(m)
                # for j in super:
                #     m[j.id] = j.tenant.id
                #     break

        return self.render('netbox_supervisor_plugin/supervisor_tenant.html', extra_context={
            'count': len(m),
        })


template_extensions = [SupervisorCount]
