#pip install win32wifi

from ezwifi.ezwlan import *
from E4function import E4function

import asyncio, pkgutil, os, time, pprint

class Wifi:
    def __init__(self):
        self.ifaceNum = 0
        self.ifaces = getWirelessInterfaces()
        self.iface = self.ifaces[0]
        self.profiles = getWirelessProfiles(self.iface)
        self.WifiSupporter = WifiSupporter()
        self.ezwlan = Ezwlan()

        self.scan()

    # show 함수 집합
    def show_interfaces(self):
        count = 0
        for iface in self.ifaces:
            print("Interface Number: " + str(count))
            print(iface.__str__())
            print()
    
    def show_profiles(self):
        for profile in self.profiles:
            print(profile.name)
    
    def show_list(self):
        for wifi in self.wifiList:
            print(wifi.ssid.decode("utf-8", "ignore"))

    def show_details(self, ssid):
        for wifi in self.wifiList:
            if ssid.encode() == wifi.ssid:
                print(wifi.__str__())
                break
    def show_current(self):
        pp = pprint.PrettyPrinter(indent=4)
        res = queryInterface(self.iface, "current_connection")
        pp.pprint(res[1])

    # set 함수 집합
    def set_interface(self, num):
        maximum = len(self.ifaces) - 1
        if maximum >= num:
            self.ifaceNum = num
            self.iface = self.ifaces[num]
        else:
            print("Maximum Interface Num is " + str(maximum))

    def set_profile(self, ssid, passwd=None, mode="manual"):
        wifi = self.search(ssid)
        if wifi.security_enabled is None:
            print("Cannot find WiFi named " + ssid)
            return False

        if wifi.security_enabled is True and passwd is None:
            print("Need WiFi Password")
            return False
        if passwd == "":
            passwd = None
        xml_profile = self.WifiSupporter.get_xml(wifi.security_enabled, ssid, passwd, mode)

        result = self.ezwlan._setProfile(self.iface, xml_profile)

        if result == 0:
            self.profiles = getWirelessProfiles(self.iface)
            print("Set WiFi Profile " + ssid + " is succeed")
            return True
        else:
            print("WlanSetProfile Error code " + result)
            return False

    # get 함수 집합
    def get_list(self):
        result = list()
        for wifi in self.wifiList:
            wifiInfo = dict()
            wifiInfo['ssid'] = wifi.ssid.decode("utf-8", "ignore")
            wifiInfo['signal_quality'] = wifi.signal_quality
            result.append(wifiInfo)
        return result

    def get_current(self):
        res = queryInterface(self.iface, "current_connection")
        wifiInfo = dict()
        wifiInfo['ssid'] = res[1]['wlanAssociationAttributes']['dot11Ssid'].decode("utf-8", "ignore")
        wifiInfo['mac'] = E4function.Mac().get_mac()
        wifiInfo['ap_mac'] = res[1]['wlanAssociationAttributes']['dot11Bssid']
        wifiInfo['siganl_quality'] = res[1]['wlanAssociationAttributes']['wlanSignalQuality']
        return wifiInfo

    # 일반 함수 집합
    def scan(self, ssid=""):
        result = self.ezwlan._scan(self.iface, ssid)
        if result == 0:
            print("Scanning WiFi")
            eventCode = self.WifiSupporter.wait_for_event("scan")
            self.refresh_list()
            if eventCode == self.WifiSupporter.eventDict['scan'][0]:
                print("Complete Scanning\n")
            elif eventCode == self.WifiSupporter.eventDict['scan'][1]:
                print("Failed to Scan. Please Try again\n")
    
        else:
            print("WlanScan error code: " + str(result))

    def delete_profile(self, name):
        result = int
        try:
            result = deleteProfile(self.iface, name)
        except Exception as e:
            errCode = e.__str__().split(',')[1].replace(" ", "").replace(')', "")
            if errCode == "1168":
                print(name + " profile is not exist")
            else:
                print(e)

        if result == 0:
            print("Deleting WiFi profile named " + name + " is succeed")
            self.refresh_profiles()
    
    def search(self, ssid):
        for wifi in self.wifiList:
            if ssid.encode() == wifi.ssid:
                return wifi

    def search_profile(self, ssid):
        for profile in self.profiles:
            if profile.name == ssid:
                return profile

    def disconnect(self):
        disconnect(self.iface)
        print("Disconnecting WiFi is Succeed")

    def connect(self, ssid, passwd=None, mode="manual"):
        wifi = self.search(ssid)
        if wifi == None:
            self.scan()
            wifi = self.search(ssid)
            if wifi == None:
                print(ssid + " is not exist")
                print("Please try again next time")
                return
        profile = self.search_profile(ssid)
        if profile is None:
            result = self.set_profile(ssid, passwd)
            if result is False:
                return
            profile = self.search_profile(ssid)
        
        connection_params = dict()
        connection_params["connectionMode"] = 'wlan_connection_mode_profile'
        connection_params["profile"] = ssid
        connection_params["ssid"] = None
        connection_params["bssidList"] = None
        connection_params["bssType"] = wifi.bss_type
        connection_params["flags"] = profile.flags
        try:
            connect(self.iface, connection_params)
        except Exception as e:
            print(e)
            return

        eventCode = self.WifiSupporter.wait_for_event("connect")

        if eventCode == self.WifiSupporter.eventDict['connect'][0]:
            self.delete_profile(ssid)
            print("Please Check SSID or PASSWORD")
        elif eventCode == self.WifiSupporter.eventDict['connect'][1]:
            print(ssid + " is connected")
        else:
            print("Unknown Error of eventCode: " + self.eventCode)


    # 기타 함수
    def refresh_list(self):
        self.wifiList = getWirelessAvailableNetworkList(self.iface)

    def refresh_profiles(self):
        self.profiles = getWirelessProfiles(self.iface)

    def event_loop(self, e):
        for eventCode in self.WifiSupporter.eventDict[self.WifiSupporter.eventCaller]:
            if e.notificationCode == eventCode:
                self.eventCode = eventCode
                self.event = False

