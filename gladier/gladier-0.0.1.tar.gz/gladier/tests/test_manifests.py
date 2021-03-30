import gladier.tests  # noqa -- Enables debug logging
from gladier.client import GladierClient
from pprint import pprint


class GladierManifestToFuncXTasks(GladierClient):
    client_id = 'e6c75d97-532a-4c88-b031-8584a319fa3e'
    gladier_tools = [
        'gladier_tools.manifest.ManifestToFuncXTasks',
        'gladier_xpcs.Reprocessing',
        'some_third_party_package.Thing',
    ]
    flow_definition = 'gladier.tools.manifest.ManifestToFuncXTasks'


def run_gladier_client(gladier_client, flow_input=None):
    flow = gladier_client.start_flow(flow_input=flow_input)
    gladier_client.progress(flow['action_id'])
    details = gladier_client.get_status(flow['action_id'])
    pprint(details)


if __name__ == '__main__':
    # run_gladier_client(GladierManifestTransfer())

    shameful_funcx_tutorial_ep = '4b116d3c-1703-4f8f-9f6f-39921e5864df'
    manifests_to_tasks_input = {
        'input': {
            'manifest_to_tasks_manifest_id': '22ea05b3-a708-4524-b2c7-b3a635ffb1c3',
            'funcx_endpoint_non_compute': shameful_funcx_tutorial_ep,
            'manifest_to_funcx_tasks_funcx_endpoint_compute': shameful_funcx_tutorial_ep,
            'manifest_to_funcx_tasks_callback_funcx_id': 'b5f21ae2-9ceb-4b1f-8600-bc23e7fcac4d',

        },
    }
    run_gladier_client(GladierManifestToFuncXTasks(), manifests_to_tasks_input)