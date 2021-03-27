"""Instantiate a playwright chrominium browser.

Respect PWBROWSER_ environ variables in .env
"""
from typing import Union, Optional

from playwright.async_api import async_playwright, Browser
from get_pwbrowser.config import Settings

import logzero
from logzero import logger

config = Settings()
HEADLESS = not config.headful
DEBUG = config.debug
PROXY = config.proxy


# fmt: off
async def get_pwbrowser(
        headless: bool = HEADLESS,
        verbose: Union[bool, int] = DEBUG,
        proxy: Optional[Union[str, dict]] = PROXY,
        **kwargs
) -> Browser:
    # fmt: on
    """Instantiate a playwright chrominium browser.

    if isinstance(verbose, bool):
        verbose = 10 if verbose else 20
    logzero.loglevel(verbose)

    browser = await get_browser(headless)
    context = await browser.newContext()
    page = await context.newPage()
    await page.goto('https://httpbin.org/ip') https://httpbin.org/ip
    # https://getfoxyproxy.org/geoip/
    # http://whatsmyuseragent.org/
    https://playwright.dev/python/docs/intro/

    proxy setup: https://playwright.dev/python/docs/network?_highlight=proxy#http-proxy
        browser = await chromium.launch(proxy={
          "server": "http://myproxy.com:3128",
          "user": "usr",
          "password": "pwd"
        })
    https://scrapingant.com/blog/how-to-use-a-proxy-in-playwright
        chrominium
            const launchOptions = {
                args: [ '--proxy-server=http://222.165.235.2:80' ]
            };
            browser = await playwright['chromium'].launch(launchOptions)

    """
    if isinstance(verbose, bool):
        verbose = 10 if verbose else 20
    logzero.loglevel(verbose)

    kwargs.update({
        "headless": headless,
    })

    if proxy:
        proxy = {"server": proxy}
        kwargs.update({
            "proxy": proxy,
        })

    try:
        playwright = await async_playwright().start()
    except Exception as exc:
        logger.error(exc)
        raise

    try:
        browser = await playwright.chromium.launch(**kwargs)
    except Exception as exc:
        logger.error(exc)
        raise

    return browser
