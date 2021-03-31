import os

# General settings
NOTIFICATIONS_SCRAPE_INTERVAL_SECONDS = os.getenv('NOTIFICATIONS_SCRAPE_INTERVAL', 5)
PATH_TO_MS_CONFIG = os.getenv('PATH_TO_MS_CONFIG', '/etc/harp-gate-client/config.json')

# Collector settings
GATE_HOST = os.getenv('GATE_HOST', 'http://127.0.0.1:8081/api/v1/gate-collector')

# Example: {'url': 'http://127.0.0.1:8084', 'user': 'Admin', 'password': 'zabbix'}
ZABBIX_SYSTEMS = []

# Example: {'url': 'http://127.0.0.1', 'user': 'root', 'password': 'd0c87be02fdb79f0'}
ICINGA_SYSTEMS = []


