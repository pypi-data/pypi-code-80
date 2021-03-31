import os
import requests as req
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen, urlretrieve
import time


class Downloader:
    count: int = 1

    def __init__(self, keyword, driver="Chrome", website="google"):
        self.keyword = keyword
        self.driver = driver
        self.website = website

    def instagram(self):
        time.sleep(3)
            
        self.browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        mail = 'thisisrobotacc@gmail.com'
        pwd = 'qwer@1234'
        id = self.browser.find_element_by_css_selector('#loginForm > div > div:nth-child(1) > div > label > input')
        id.send_keys(mail)
        password = self.browser.find_element_by_css_selector('#loginForm > div > div:nth-child(2) > div > label > input')
        password.send_keys(pwd)
        password.submit()

        time.sleep(3)

    def createBroswer(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        if(self.driver == "Chrome"):
            path = "./driver/chromedriver.exe"

            if not os.path.exists(path):
                path = "chromedriver.exe"
        elif(self.driver == "Firefox"):
            path = "./driver/geckodriver.exe"
            
            if not os.path.exists(path):
                path = "geckodriver.exe"
        else:
            exit(0)

        self.browser = webdriver.Chrome(
            executable_path=path)
        if(self.website == "google"):
            self.website = "https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi-ucSO7NnvAhULiZQKHcgcAUUQ_AUoAXoECAIQAw" 
        elif(self.website == "naver"):
            self.website = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query={}"
        elif(self.website == 'instagram'):
            self.instagram()
            self.website = "https://www.instagram.com/explore/tags/{}"
        self.browser.get(self.website.format(self.keyword))

    def download(self):
        self.createBroswer()

        if not os.path.exists(self.keyword):
            os.mkdir(self.keyword)

        for _ in range(500):
            self.browser.execute_script("window.scrollBy(0,10000)")

        for x in self.browser.find_elements_by_tag_name("img"):
            url = x.get_attribute('src')

            if url != None:
                if url[0] == 'h':
                    print("[+] url : ", url)

                    target = urlopen(url).read()
                    image = "{}_".format(self.keyword) + \
                        str(self.count) + ".png"

                    urlretrieve(url, './{}/'.format(self.keyword) + image)
                    self.count += 1
                else:
                    pass
            else:
                pass

        print('[+] download image : ', self.count - 1)

        self.browser.close()
