import os

# Icinga settings
ICINGA_API_USER = os.getenv('ICINGA_API_USER', 'root')
ICINGA_API_PASS = os.getenv('ICINGA_API_PASS', 'd0c87be02fdb79f0')

# Zabbix settings
ZABBIX_API_USER = os.getenv('ZABBIX_API_USER', 'Admin')
ZABBIX_API_PASS = os.getenv('ZABBIX_API_PASS', 'zabbix')

# General settings
NOTIFICATIONS_SCRAPE_INTERVAL_SECONDS = os.getenv('NOTIFICATIONS_SCRAPE_INTERVAL', 5)

# Collector settings
GATE_HOST = os.getenv('GATE_HOST', 'http://127.0.0.1:8081/api/v1/gate-collector')

# Temp MS settings
ZABBIX_SYSTEMS = [
    "http://127.0.0.1:8084"
]

ICINGA_SYSTEMS = [
    "127.0.0.1"
]

# LOCATIONS = {
#     "zabbix": {
#         "zabbix.aws": "http://127.0.0.1:8084/api_jsonrpc.php"
#     },
#     "icinga": {
#         "icinga.aws": "127.0.0.1"
#     }
# }


