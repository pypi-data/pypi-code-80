import logging

from discord_webhook_logging import DiscordWebhookHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = DiscordWebhookHandler(webhook_url='https://discord.com/api/webhooks/823687444481835028/XfqnGeox1fI_wp2vUgK9HpmfVMOUl9t6HefjfQEhnyQwgtnzyjr_2uYrWDWQlS0NW6mn')
logger.addHandler(handler)

logger.info('0'*2000 + '1'*50)
