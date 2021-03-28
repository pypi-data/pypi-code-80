from ezwifi.wlanapi import *
from win32wifi.Win32Wifi import *


class ezwlan:

    def _setProfile(wireless_interface, xml_profile):
        handle = WlanOpenHandle()
        result = WlanSetProfile(handle, wireless_interface.guid, xml_profile)
        WlanCloseHandle(handle)

        return result

    def _scan(wireless_interface, ssid=""):
        handle = WlanOpenHandle()
        result = WlanScan(handle, wireless_interface.guid, ssid.encode())
        WlanCloseHandle(handle)

        return result