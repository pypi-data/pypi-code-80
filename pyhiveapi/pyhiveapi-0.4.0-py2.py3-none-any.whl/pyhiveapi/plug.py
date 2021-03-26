"""Hive Switch Module."""

from .helper.const import HIVETOHA


class HiveSmartPlug:
    """Plug Device.

    Returns:
        object: Returns Plug object
    """

    plugType = "Switch"

    def getState(self, device: dict):
        """Get smart plug state.

        Args:
            device (dict): Device to get the plug state for.

        Returns:
            boolean: Returns True or False based on if the plug is on
        """
        state = None

        try:
            data = self.session.data.products[device["hiveID"]]
            state = data["state"]["status"]
            state = HIVETOHA["Switch"].get(state, state)
        except KeyError as e:
            self.session.log.error(e)

        return state

    def getPowerUsage(self, device: dict):
        """Get smart plug current power usage.

        Args:
            device (dict): [description]

        Returns:
            [type]: [description]
        """
        state = None

        try:
            data = self.session.data.products[device["hiveID"]]
            state = data["props"]["powerConsumption"]
        except KeyError as e:
            self.session.log.error(e)

        return state

    def setStatusOn(self, device: dict):
        """Set smart plug to turn on.

        Args:
            device (dict): Device to switch on.

        Returns:
            boolean: True/False if successful
        """
        final = False

        if (
            device["hiveID"] in self.session.data.products
            and device["deviceData"]["online"]
        ):
            self.session.hiveRefreshTokens()
            data = self.session.data.products[device["hiveID"]]
            resp = self.session.api.setState(
                data["type"], data["id"], status="ON"
            )
            if resp["original"] == 200:
                final = True
                self.session.getDevices(device["hiveID"])

        return final

    def setStatusOff(self, device: dict):
        """Set smart plug to turn off.

        Args:
            device (dict): Device to switch off.

        Returns:
            boolean: True/False if successful
        """
        final = False

        if (
            device["hiveID"] in self.session.data.products
            and device["deviceData"]["online"]
        ):
            self.session.hiveRefreshTokens()
            data = self.session.data.products[device["hiveID"]]
            resp = self.session.api.setState(
                data["type"], data["id"], status="OFF"
            )
            if resp["original"] == 200:
                final = True
                self.session.getDevices(device["hiveID"])

        return final


class Switch(HiveSmartPlug):
    """Home Assistant switch class.

    Args:
        SmartPlug (Class): Initialises the Smartplug Class.
    """

    def __init__(self, session: object):
        """Initialise switch.

        Args:
            session (object): This is the session object to interact with the current session.
        """
        self.session = session

    def getSwitch(self, device: dict):
        """Home assistant wrapper to get switch device.

        Args:
            device (dict): Device to be update.

        Returns:
            dict: Return device after update is complete.
        """
        device["deviceData"].update(
            {"online": self.session.attr.onlineOffline(device["device_id"])}
        )
        dev_data = {}

        if device["deviceData"]["online"]:
            self.session.helper.deviceRecovered(device["device_id"])
            data = self.session.data.devices[device["device_id"]]
            dev_data = {
                "hiveID": device["hiveID"],
                "hiveName": device["hiveName"],
                "hiveType": device["hiveType"],
                "haName": device["haName"],
                "haType": device["haType"],
                "device_id": device["device_id"],
                "device_name": device["device_name"],
                "status": {
                    "state": self.getSwitchState(device),
                },
                "deviceData": data.get("props", None),
                "parentDevice": data.get("parent", None),
                "custom": device.get("custom", None),
                "attributes": {},
            }

            if device["hiveType"] == "activeplug":
                dev_data["status"].update(
                    {
                        "status": {
                            "state": dev_data["status"]["state"],
                            "power_usage": self.getPowerUsage(device),
                        },
                        "attributes": self.session.attr.stateAttributes(
                            device["device_id"], device["hiveType"]
                        ),
                    }
                )

            self.session.devices.update({device["hiveID"]: dev_data})
            return self.session.devices[device["hiveID"]]
        else:
            self.session.log.errorCheck(
                device["device_id"], "ERROR", device["deviceData"]["online"]
            )
            return device

    def getSwitchState(self, device: dict):
        """Home Assistant wrapper to get updated switch state.

        Args:
            device (dict): Device to get state for

        Returns:
            boolean: Return True or False for the state.
        """
        if device["hiveType"] == "Heating_Heat_On_Demand":
            return self.session.heating.getHeatOnDemand(device)
        else:
            return self.getState(device)

    def turnOn(self, device: dict):
        """Home Assisatnt wrapper for turning switch on.

        Args:
            device (dict): Device to switch on.

        Returns:
            function: Calls relevant function.
        """
        if device["hiveType"] == "Heating_Heat_On_Demand":
            return self.session.heating.setHeatOnDemand(device, "ENABLED")
        else:
            return self.setStatusOn(device)

    def turnOff(self, device: dict):
        """Home Assisatnt wrapper for turning switch off.

        Args:
            device (dict): Device to switch off.

        Returns:
            function: Calls relevant function.
        """
        if device["hiveType"] == "Heating_Heat_On_Demand":
            return self.session.heating.setHeatOnDemand(device, "DISABLED")
        else:
            return self.setStatusOff(device)
