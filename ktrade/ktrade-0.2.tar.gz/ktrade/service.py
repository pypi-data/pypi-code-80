import asyncio
import websockets
from websockets.client import WebSocketClientProtocol

from .protocol import tunnel_pb2
from .stock.async_stocksubscriber import AsyncStockSubscriber
from .stock.async_stockhandler import AsyncStockHandler
from .stock.async_client import AsyncClient
from .stock.async_stockprovider import AsyncStockProvider

from . import exceptions


def get_result_code(data) -> tunnel_pb2.Result:
    r = tunnel_pb2.Result()
    r.ParseFromString(data)
    return r.result_code


async def handshake(role, vendor, channel_type, service, options
) -> (WebSocketClientProtocol, int, tunnel_pb2.Node):
    try:
        ws = await websockets.connect('ws://localhost:8765')
    except:
        raise

    node = tunnel_pb2.Node()
    node.vendor = vendor
    node.role = role
    node.channel_type = channel_type
    node.service = service
    node.name = '' if 'name' not in options else options['name']

    await ws.send(node.SerializeToString())
    result_code = get_result_code(await ws.recv())

    return ws, result_code, node


async def stock_service(vendor, channel_type, **kwargs) -> AsyncClient:
    try:
        ws, result_code, node = await handshake(tunnel_pb2.CLIENT,
                                                vendor,
                                                channel_type,
                                                tunnel_pb2.STOCK, kwargs)
    except:
        raise
    else:
        if result_code == tunnel_pb2.Result.OK:
            if channel_type == tunnel_pb2.REQ_RES:
                return AsyncStockHandler(node, ws)
            elif channel_type == tunnel_pb2.PUBLISH_SUBSCRIBE:
                try:
                    return AsyncStockSubscriber(node,
                                                ws,
                                                kwargs['callback'])
                except KeyError:
                    return AsyncStockSubscriber(node, ws, None)
        else:
            raise exceptions.KrossClientException('handshake failed')
    

async def stock_provider_service(vendor, channel_type, **kwargs) -> AsyncStockProvider:
    try:
        ws, result_code, node = await handshake(tunnel_pb2.PROVIDER,
                                                vendor,
                                                channel_type,
                                                tunnel_pb2.STOCK,
                                                kwargs)
    except:
        raise
    else:
        if result_code == tunnel_pb2.Result.OK: 
            try:
                return AsyncStockProvider(node,
                                          ws,
                                          kwargs['callback'])
            except:
                pass

    raise exceptions.KrossClientException('handshake failed')


def run(entry_point) -> None:
    asyncio.get_event_loop().run_until_complete(entry_point)
    asyncio.get_event_loop().run_forever()
