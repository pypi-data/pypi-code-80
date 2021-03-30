from gladier.defaults import GladierDefaults


def say_hello(input_message):
    raise ValueError("Oh no, this broke everything " + input_message)
    return f'Hello, my message is {input_message}'


class MyTool(GladierDefaults):

    flow_definition = {
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
                        'payload.$': '$.input.message'
                    }]
                },
                'ResultPath': '$.HelloFuncXResult',
                'WaitTime': 300,
                'End': True,
            },
        }
    }

    required_input = [
        'message',
        'funcx_endpoint_non_compute',
        'somethig_you_need_to_include',
    ]

    flow_input = {
        'message': 'hello world',
        'alternate_message': 'Hola Mundo',
        # Shamelessly reuse the FuncX Tutorial Endpoint if it doesn't exist
        'funcx_endpoint_non_compute': '4b116d3c-1703-4f8f-9f6f-39921e5864df'
    }

    funcx_functions = [
        say_hello,
    ]