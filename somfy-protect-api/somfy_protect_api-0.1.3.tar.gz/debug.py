import json
import os
import time

from somfy_protect_api.api.devices.category import Category
from somfy_protect_api.api.devices.outdoor_siren import OutDoorSiren
from somfy_protect_api.api.somfy_protect_api import SomfyProtectApi

USERNAME = "homeassistant@minims.fr"
PASSWORD = "HA+9kgTYd"
CACHE_PATH = "token.json"


def get_token():
    """Retrieve a token from a file
    """
    try:
        with open(CACHE_PATH, "r") as cache:
            return json.loads(cache.read())
    except IOError:
        pass


def set_token(token) -> None:
    """WWrite a toek into a file
    """
    with open(CACHE_PATH, "w") as cache:
        cache.write(json.dumps(token))


if __name__ == "__main__":

    api = SomfyProtectApi(username=USERNAME, password=PASSWORD, token=get_token(), token_updater=set_token)

    # Check if we already have a token
    if not os.path.isfile(CACHE_PATH):
        set_token(api.request_token())

    # List Sites
    sites = api.get_sites()

    # Retieve Alarm Status
    print(f"Alarm Status for {sites[0].label} is {sites[0].security_level}")

    # Get Data from a Device.
    devices = api.get_devices(site_id=sites[0].id, category=Category.OUTDOOR_SIREN)
    sirens = [OutDoorSiren(site=sites[0], device=d, api=api) for d in devices]
    for siren in sirens:
        print(f"Device {siren.device.label} return a Temperature of {siren.get_temperature()} °C")
        print(f"Device {siren.device.label} return a Link Quality of {siren.get_rlink_quality()} %")
        print(f"Device {siren.device.label} return a Battery Level of {siren.get_battery_level()} %")

    # Update Device
    # device = api.get_device(site_id=sites[0].id, device_id="JDqONDjHwavr7FM825nQY8FqZHQmYdpM")
    # print(device.settings)
    # settings = device.settings
    # settings["global"]["sensitivity"] = 9
    # update = api.update_device(site_id=sites[0].id, device_id="JDqONDjHwavr7FM825nQY8FqZHQmYdpM", device_label=device.label, settings=settings)
    # print(update)
    # time.sleep(1)
    # device = api.get_device(site_id=sites[0].id, device_id="JDqONDjHwavr7FM825nQY8FqZHQmYdpM")
    # print(device.settings)

    # Get Camera
    # homeassistant/switch/M1mxSzd6uGF2uyStnYk2DsWMYPdWlaiG_OncxHUAVqmJP6e2OMNrdCOcVNiyrpVpT
    camera = api.get_device(site_id=sites[0].id, device_id="OncxHUAVqmJP6e2OMNrdCOcVNiyrpVpT")
    print(camera)

    # disarmed = api.update_site(site_id=sites[0].id, security_level="disarmed")
    # print(f"Task: {disarmed})
