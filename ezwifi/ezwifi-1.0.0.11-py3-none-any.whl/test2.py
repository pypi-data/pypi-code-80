import ezwifi

wifi = ezwifi.Wifi()
print(wifi.get_current()['mac'])