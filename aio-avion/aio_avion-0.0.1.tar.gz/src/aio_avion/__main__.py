import asyncio
import os

from . import AviOnBridge

async def main():
    bridge = AviOnBridge(os.environ.get('EMAIL'), os.environ.get('PASSWORD'))
    token1 = await bridge.get_token()
    token2 = await bridge.get_token()

    print(token1)
    print(token2)


if __name__ == "__main__":
    # execute only if run as a script
    asyncio.run(main())

