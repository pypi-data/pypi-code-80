import os

try:
    import colorama

except:
    os.system("pip3 install colorama")

import colorama
from colorama import Fore
colorama.init()


n = Fore.LIGHTMAGENTA_EX + "SKBINSTALLER" + Fore.LIGHTGREEN_EX
print(Fore.LIGHTGREEN_EX + "-------------- {} --------------".format(n))
print(Fore.LIGHTGREEN_EX + "    Author: http://vk.com/danilskisluk    ")
print(Fore.LIGHTGREEN_EX + "    Version: 1.0 (02.04.2021)             ")
print(Fore.LIGHTGREEN_EX + "------------------------------------------")
n = Fore.LIGHTMAGENTA_EX + "[SKBINSTALLER] " + Fore.LIGHTCYAN_EX
reset = Fore.RESET


print(n + "start installation (y/n)? ", end="")
if input().lower() != "y":
    exit(n + "canceled")


installation_data = {
    "cython" : "sudo pip3 install -y cython",

    "build-essential" : "sudo apt-get install -y build-essential",
    "git" : "sudo apt-get install -y git",
    "python3-dev" : "sudo apt-get install -y python3-dev",
    "ffmpeg" : "sudo apt-get install -y ffmpeg",
    "zlib1g-dev" : "sudo apt-get install -y zlib1g-dev",
    "libsdl2-dev" : "sudo apt-get install -y libsdl2-dev",
    "libsdl2-image-dev" : "sudo apt-get install -y libsdl2-image-dev",
    "libsdl2-mixer-dev" : "sudo apt-get install -y libsdl2-mixer-dev",
    "libsdl2-ttf-dev" : "sudo apt-get install -y libsdl2-ttf-dev",
    "libportmidi-dev" : "sudo apt-get install -y libportmidi-dev",
    "libswscale-dev" : "sudo apt-get install -y libswscale-dev",
    "libavformat-dev" : "sudo apt-get install -y libavformat-dev",
    "libavcodec-dev" : "sudo apt-get install -y libavcodec-dev",

    "libncurses5:i386" : "sudo apt install -y libncurses5:i386",
    "libstdc++6:i386" : "sudo apt install -y libstdc++6:i386",
    "libgtk2.0-0:i386" : "sudo apt install -y libgtk2.0-0:i386",
    "libpangox-1.0-0:i386" : "sudo apt install -y libpangox-1.0-0:i386",
    "libpangoxft-1.0-0:i386" : "sudo apt install -y libpangoxft-1.0-0:i386",
    "libidn11:i386" : "sudo apt install -y libidn11:i386",
    "libltdl-dev" : "sudo apt install -y libltdl-dev",
    "libffi-dev" : "sudo apt install -y libffi-dev",
    "libssl-dev" : "sudo apt install -y libssl-dev",

    "build-essential" : "sudo apt install -y build-essential",
    "ccache" : "sudo apt install -y ccache",
    "openjdk-8-jdk" : "sudo apt install -y openjdk-8-jdk",
    "unzip" : "sudo apt install -y unzip",
    "autoconf" : "sudo apt install -y autoconf",
    "autotools-dev" : "sudo apt install -y autotools-dev",
    "cmake" : "sudo apt install -y cmake",
    "android-sdk" : "sudo apt install -y android-sdk",

    "buildozer.git" : "git clone https://github.com/kivy/buildozer.git",
    "buildozer" : "sudo python3 buildozer/setup.py install"
}


for elem in installation_data:
    print(n + "installation " + elem + reset)
    os.system(installation_data[elem])


exit(n + "installation completed")
