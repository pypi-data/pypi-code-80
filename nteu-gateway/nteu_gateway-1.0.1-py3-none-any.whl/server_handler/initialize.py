from nteu_gateway.logger import logger
from aiohttp import web
from nteu_gateway.nteu_gateway_name import NTEU_GATEWAY_NAME
from nteu_gateway.nteu_gateway import NTEUGateway


async def initialize(request: web.Request) -> web.Response:
    # Gateway
    nteu_gateway: NTEUGateway = request.app[NTEU_GATEWAY_NAME]

    # Num Request
    logger.info(f'Initialize UI')
    return web.json_response({
        "srcLang": nteu_gateway.src_Lang,
        "tgtLang": nteu_gateway.tgt_lang,
        "langDescription": nteu_gateway.description,
        "gatewayType": "nteu",
        "help": nteu_gateway.help
    })

















