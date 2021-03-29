from ezwifi import ezwifi

testWifi = "KOLOK"
testWifiPass = "ee903212"

w = ezwifi.Wifi()
w.show_list()
w.connect(testWifi)
w.disconnect()
w.delete_profile(testWifi)
w.connect(testWifi, testWifiPass)