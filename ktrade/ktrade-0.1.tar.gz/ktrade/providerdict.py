import asyncio
import collections
from .protocol import tunnel_pb2


dict_lock = asyncio.Lock()
vendor_dict = dict()


# depth 1: vendor, depth 2: channel, depth 3: service
def _add_to_dict(provider):
    print('add_to_dict', provider)
    vendor = provider.node.vendor
    channel = provider.node.channel_type
    service = provider.node.service
    if vendor not in vendor_dict:
        vendor_dict[vendor] = dict()

    if channel not in vendor_dict[vendor]:
        vendor_dict[vendor][channel] = dict()

    if service not in vendor_dict[vendor][channel]:
        vendor_dict[vendor][channel][service] = collections.deque()

    vendor_dict[vendor][channel][service].append(provider)


async def add_provider(provider):
    async with dict_lock:
        _add_to_dict(provider)


def _clear_provider():
    global vendor_dict
    vendor_dict = dict()


async def find_rqrs_provider(vendor, channel, service):
    try:
        providers = vendor_dict[vendor][channel][service]
    except KeyError:
        return None
    
    available_provider = None
    for provider in providers:
        if not provider.pending:
            provider.pending = True
            available_provider = provider
            providers.rotate(-1)
            break
    
    return available_provider


async def find_provider(vendor, channel, service):
    available_provider = None
    if channel == tunnel_pb2.REQ_RES:
        available_provider = await find_rqrs_provider(vendor, channel, service)
    elif channel == tunnel_pb2.PUBLISH_SUBSCRIBE:
        pass

    return available_provider
