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
    devices = api.get_devices(site_id=sites[0].id)
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
    # for device in devices:
    #    print(device.label)
    #    print(device.device_definition.get("label"))
    #    print(device.settings)

    action_device = api.action_device(
        site_id="M1mxSzd6uGF2uyStnYk2DsWMYPdWlaiG", device_id="OncxHUAVqmJP6e2OMNrdCOcVNiyrpVpT", action="shutter_open"
    )
    snapshot = api.camera_snapshot(
        site_id="M1mxSzd6uGF2uyStnYk2DsWMYPdWlaiG", device_id="OncxHUAVqmJP6e2OMNrdCOcVNiyrpVpT"
    )
    snapshot = api.camera_refresh_snapshot(
        site_id="M1mxSzd6uGF2uyStnYk2DsWMYPdWlaiG", device_id="OncxHUAVqmJP6e2OMNrdCOcVNiyrpVpT"
    )

    # disarmed = api.update_site(site_id=sites[0].id, security_level="disarmed")
    # print(f"Task: {disarmed})
