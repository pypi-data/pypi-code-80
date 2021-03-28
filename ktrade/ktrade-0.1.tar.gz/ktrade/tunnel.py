import asyncio
import websockets

import google.protobuf.message as message
from .protocol import tunnel_pb2
from . import provider
from . import client
from . import providerdict

""" for debugging websockets
import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
"""


async def _add_node(node, ws) -> None:
    node_wrapper = None

    if node.role == tunnel_pb2.PROVIDER:
        node_wrapper = provider.KrossProvider(ws, node)
        await providerdict.add_provider(node_wrapper)
    elif node.role == tunnel_pb2.CLIENT:
        node_wrapper = client.KrossClient(ws, node)

    if node_wrapper is not None:
        await ws.send(_create_result(tunnel_pb2.Result.OK).SerializeToString())
        await node_wrapper.listen()
    else:
        await ws.send(_create_result(tunnel_pb2.Result.NOT_AVAILABLE).SerializeToString())


def _create_result(code) -> tunnel_pb2.Result:
    r = tunnel_pb2.Result()
    r.result_code = code
    return r


async def accept(ws, path) -> None:
    print('node connected')
    recv_data = await ws.recv()
    node = tunnel_pb2.Node()
    try:
        node.ParseFromString(recv_data)
    except message.DecodeError:
        await ws.send(_create_result(tunnel_pb2.Result.MESSAGE_ERROR).SerializeToString())
    else:
        await _add_node(node, ws)


if __name__ == '__main__':
    start_server = websockets.serve(accept, "localhost", 8765, 
                                    ping_timeout=5, ping_interval=5, compression=None)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
