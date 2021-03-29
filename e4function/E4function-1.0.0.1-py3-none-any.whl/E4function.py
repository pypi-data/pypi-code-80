from uuid import getnode

class Mac:
    def get_mac(self):
        hexMac = hex(getnode())
        mac = self.hex_to_mac(hexMac)
        return mac

    # hexStr (str) : 0xc80aa8900b09 
    # mac (str) : C8:0A:A8:90:0B:09
    def hex_to_mac(self, hexStr):
        hexMac = hexStr.replace("0x", "")
        hexList = list()
        for i in range(6):
            index = i*2
            hexList.append(hexMac[index:index+2].upper())
        mac = ":".join(hexList)
        return mac