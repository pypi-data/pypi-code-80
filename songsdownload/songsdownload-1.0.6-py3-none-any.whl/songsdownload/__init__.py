from googlesearch import search
import requests
import bs4
import time,sys,os

qlyrics = " lklyrics"
qmp3 = " ananmanan"
b = []
c = []


def checkInternet():
    print("Checking Internet Connection...")
    time.sleep(0.2)
    if ping("https://www.google.com/") == True:
        return True
    else:
        print("Internet is not available. Please try again.")
        sys.exit()


def ping(url):
    try:
        req = requests.get(url)
        if req.status_code == 200:
            return True
        else:
            return False
    except:
        return False


class Songsdetails:
    def __init__(self,query,location = os.getcwd()):
        self.query = query
        self.location = location


    def downloadsongs(self):
        if checkInternet() == True:
            for i in search(self.query + qmp3, tld="com", num=10, stop=10, pause=1):
                if "ananmanan" in i:
                    c.append(i)
            try:
                mp = requests.get(c[0]).text
                print("[*]Getting Information on mp3....")
                id = str(c[0]).split("song/")[1].split("/")[0]
                link = requests.get("https://www.ananmanan.lk/free-sinhala-mp3/download.php?id=" + str(id)).url
                name = (str(c[0]).split(".html")[0].split("/")[-1].replace("-", " "))
                down = requests.get(url=link, stream=True)
                from tqdm import tqdm
                print("[*]Downloading MP3..............")
                size = float(down.headers['content-length'])
                os.chdir(self.location)
                with open(name + ".mp3", "wb") as f:
                    for chunk in tqdm(iterable=down.iter_content(1024),unit='KB',total=size/1024,desc="Downloading :"):
                        f.write(chunk)
                print("[*]"+self.query+" Download Completed \n\n")


            except:
                print("[*]MP3 downloading error")
                print("[*]Try again with different query\n\n")

    def downloadlyrics(self):
        if checkInternet() == True:

            for i in search(self.query + qlyrics, tld="com", num=10, stop=10, pause=1):
                if "lklyrics" in i:
                    b.append(i)

            try:
                ly = requests.get(b[0]).text
                print("[*]Getting Information lyrics....")
                soup = bs4.BeautifulSoup(ly, "lxml")
                ss = (soup.find_all("img")[1])
                lylink = str(ss).split('src="')[1].split('"')[0]
                lylink = requests.get(lylink, stream=True)
                print("[*]Downloading Lyrics.................")
                size = float(lylink.headers['content-length'])
                from tqdm import tqdm
                pbar = tqdm(iterable=lylink.iter_content(1024),unit='KB',total=size/1024,desc="Downloading :")
                import time
                os.chdir(self.location)

                with open(self.query+".png", "wb") as f:
                    for chunk in pbar:
                        f.write(chunk)
                print("[*]"+self.query+" Download Completed \n\n")


            except:
                print("[*]Lyrics downloading error")
                print("[*]Try again with another query\n\n")




