from pprint import pprint
from gladier.client import GladierClient

custom_flow_definition = {
        'Comment': 'Hello Gladier Automate Flow',
        'StartAt': 'HelloFuncX',
        'States': {
            'HelloFuncX': {
                'Comment': 'Say hello to the world!',
                'Type': 'Action',
                'ActionUrl': 'https://api.funcx.org/automate',
                'ActionScope': 'https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/automate2',
                'Parameters': {
                    'tasks': [{
                        'endpoint.$': '$.input.funcx_endpoint_non_compute',
                        'func.$': '$.input.say_hello_funcx_id',
                        'payload.$': '$.input.alternate_message'
                    }]
                },
                'ResultPath': '$.HelloFuncXResult',
                'WaitTime': 300,
                'End': True,
            },
        }
    }


class HelloWorldClient(GladierClient):
    client_id = 'e6c75d97-532a-4c88-b031-8584a319fa3e'
    gladier_tools = [
        'gladier.tests.my_tool.MyTool'
    ]
    # flow_definition = 'gladier.tests.my_tool.MyTool'
    flow_definition = custom_flow_definition


hw_cli = HelloWorldClient()
flow = hw_cli.start_flow()
hw_cli.progress(flow['action_id'])
details = hw_cli.get_status(flow['action_id'])
pprint(details)
