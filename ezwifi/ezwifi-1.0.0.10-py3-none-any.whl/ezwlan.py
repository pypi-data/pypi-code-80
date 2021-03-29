from ezwifi.wlanapi import *
from win32wifi.Win32Wifi import *

import binascii, threading


class Ezwlan:

    def __init__(self):
        pass

    def _setProfile(self, wireless_interface, xml_profile):
        handle = WlanOpenHandle()
        result = WlanSetProfile(handle, wireless_interface.guid, xml_profile)
        WlanCloseHandle(handle)

        return result

    def _scan(self, wireless_interface, ssid=""):
        handle = WlanOpenHandle()
        result = WlanScan(handle, wireless_interface.guid, ssid.encode())
        WlanCloseHandle(handle)

        return result


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