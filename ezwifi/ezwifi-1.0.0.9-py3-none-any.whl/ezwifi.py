#pip install win32wifi

from ezwifi.ezwlan import *

import binascii, asyncio, pkgutil, os, time, threading, pprint

class WifiSupporter:
    def __init__(self):
        self.authDict = dict()
        self.authDict[0] = "open"
        self.authDict[1] = "WPA2PSK"
        self.open_xml = open_xml
        self.wpa2psk_xml = wpa2psk_xml

        self.event = False
        self.eventCode = None
        self.eventCaller = None
        self.eventDict = dict()
        self.eventDict['scan'] = ['wlan_notification_acm_scan_list_refresh', 'wlan_notification_acm_scan_fail']
        self.eventDict['connect'] = ['wlan_notification_acm_connection_attempt_fail', 'wlan_notification_acm_connection_complete']

        self.timeout_flag = True

    # def set_xml(self, auth):
    #     folder = 'resources/xml'
    #     filename = f'{self.authDict[auth]}.xml'
    #     if self.authDict[auth] == "open":
    #         xml = open_xml
    #     else:
    #         xml = pkgutil.get_data(__name__, os.path.join(folder, filename)).decode()
    #     #xml = ''.join(open(self.authDict[auth] + '_xml.txt', mode='r', encoding='utf-8').readlines())

    #     return xml
    
    def get_xml(self, auth, ssid, passwd=None, mode="manual"):
        if auth:
            xml = self.wpa2psk_xml.format(profile=ssid, ssid_hex = binascii.hexlify(ssid.encode()).decode().upper(), ssid=ssid, mode=mode, passwd=passwd)
        else:
            xml = self.open_xml.format(profile=ssid, ssid_hex = binascii.hexlify(ssid.encode()).decode().upper(), ssid=ssid, mode=mode)
        
        return xml

    def wait_for_event(self, eventCaller):
        handle = registerNotification(self.event_loop)
        self.event = True
        self.eventCaller = eventCaller
        t = threading.Timer(10, self.timeout)
        t.start()
        while(self.event and self.timeout_flag):
            pass
        unregisterNotification(handle)

        if self.timeout_flag == False:
            self.timeout_flag = True
            exit()
        else:
            t.cancel()

        return self.eventCode

    def event_loop(self, e):
        for eventCode in self.eventDict[self.eventCaller]:
            if e.notificationCode == eventCode:
                self.eventCode = eventCode
                self.event = False

    def listen_event(self):
        handle = registerNotification(self.event_loop_test)
        self.event = True
        while(self.event):
            pass
        unregisterNotification(handle)

    def event_loop_test(self, e):
        print(e)

    def timeout(self):
        print("Timeout")
        self.timeout_flag = False


class Wifi:
    def __init__(self):
        self.interfaceNum = 0
        self.ifaces = getWirelessInterfaces()
        self.iface = self.ifaces[0]
        self.profiles = getWirelessProfiles(self.iface)
        self.WifiSupporter = WifiSupporter()

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
            self.interfaceNum = num
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

        result = ezwlan._setProfile(self.iface, xml_profile)

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
            result.append(wifi.ssid.decode("utf-8", "ignore"))
        return result

    def get_current(self):
        res = queryInterface(self.iface, "current_connection")
        return res[1]['strProfileName']

    # 일반 함수 집합
    def scan(self, ssid=""):
        result = ezwlan._scan(self.iface, ssid)
        if result == 0:
            print("Scanning WiFi")
            eventCode = self.WifiSupporter.wait_for_event("scan")
            self.refresh_list()
            if eventCode == self.WifiSupporter.eventDict['scan'][0]:
                print("Complete Scanning")
            elif eventCode == self.WifiSupporter.eventDict['scan'][1]:
                print("Failed to Scan. Please Try again")
    
        else:
            print("WlanScan error code: " + str(result))

    def delete_profile(self, name):
        result = int
        try:
            result = deleteProfile(self.iface, name)
        except Exception as e:
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

open_xml = str()  
open_xml += '<?xml version="1.0"?>\n'
open_xml += '<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">\n'
open_xml += '        <name>{profile}</name>\n'
open_xml += '        <SSIDConfig>\n'
open_xml += '                <SSID>\n'
open_xml += '                        <hex>{ssid_hex}</hex>\n'
open_xml += '                        <name>{ssid}</name>\n'
open_xml += '                </SSID>\n'
open_xml += '        </SSIDConfig>\n'
open_xml += '        <connectionType>ESS</connectionType>\n'
open_xml += '        <connectionMode>{mode}</connectionMode>\n'
open_xml += '        <MSM>\n'
open_xml += '                <security>\n'
open_xml += '                        <authEncryption>\n'
open_xml += '                                <authentication>open</authentication>\n'
open_xml += '                                <encryption>none</encryption>\n'
open_xml += '                        </authEncryption>\n'
open_xml += '                </security>\n'
open_xml += '        </MSM>\n'
open_xml += '        <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">\n'
open_xml += '                <enableRandomization>false</enableRandomization>\n'
open_xml += '        </MacRandomization>\n'
open_xml += '</WLANProfile>\n'

wpa2psk_xml = str()
wpa2psk_xml += '<?xml version="1.0"?>\n'
wpa2psk_xml += '<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">\n'
wpa2psk_xml += '        <name>{profile}</name>\n'
wpa2psk_xml += '        <SSIDConfig>\n'
wpa2psk_xml += '                <SSID>\n'
wpa2psk_xml += '                        <hex>{ssid_hex}</hex>\n'
wpa2psk_xml += '                        <name>{ssid}</name>\n'
wpa2psk_xml += '                </SSID>\n'
wpa2psk_xml += '        </SSIDConfig>\n'
wpa2psk_xml += '        <connectionType>ESS</connectionType>\n'
wpa2psk_xml += '        <connectionMode>{mode}</connectionMode>\n'
wpa2psk_xml += '        <MSM>\n'
wpa2psk_xml += '                <security>\n'
wpa2psk_xml += '                        <authEncryption>\n'
wpa2psk_xml += '                                <authentication>WPA2PSK</authentication>\n'
wpa2psk_xml += '                                <encryption>AES</encryption>\n'
wpa2psk_xml += '                                <useOneX>false</useOneX>\n'
wpa2psk_xml += '                        </authEncryption>\n'
wpa2psk_xml += '                        <sharedKey>\n'
wpa2psk_xml += '                                <keyType>passPhrase</keyType>\n'
wpa2psk_xml += '                                <protected>false</protected>\n'
wpa2psk_xml += '                                <keyMaterial>{passwd}</keyMaterial>\n'
wpa2psk_xml += '                        </sharedKey>\n'
wpa2psk_xml += '                </security>\n'
wpa2psk_xml += '        </MSM>\n'
wpa2psk_xml += '        <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">\n'
wpa2psk_xml += '                <enableRandomization>false</enableRandomization>\n'
wpa2psk_xml += '        </MacRandomization>\n'
wpa2psk_xml += '</WLANProfile>\n'