from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup


def ElementLocater(dr,l):
    curr_handler = dr
    for i in l:
        curr_handler = curr_handler.find_element_by_xpath(i)
        print(i)
        print(curr_handler.get_attribute("class"))
        print(curr_handler.get_attribute("style"))
    return curr_handler
    

class TypeRacer:
    
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        self.driver.get("https://play.typeracer.com/")
        
    def OpenNewGame(self):
        #self.driver.refresh()
        time.sleep(2)
        ElementLocater(self.driver , ["//div[1]",".//div[1]" , ".//div[1]" , './/div[@class="main"]' ,'.//div[@class="themeContent"]' , './/div[@id="dUI"]' , ".//table[1]" , ".//tbody[1]",".//tr[2]" , ".//td[2]" , ".//div[1]" , ".//div[1]" , ".//div[1]" , ".//div[1]" , ".//div[1]" , ".//a[1]"]).click()
    
    def StartHack(self):
        soup = BeautifulSoup(self.driver.page_source , "html.parser")
        otpt = ""
        for i in(soup.find_all("span" , {"unselectable" : "on"})):
            otpt = otpt+i.text
        print(otpt)
        text_box = ElementLocater(self.driver,["//div[1]",".//div[1]" , ".//div[1]" , './/div[@class="main"]' ,'.//div[@class="themeContent"]' , './/div[@id="dUI"]' , ".//table[1]" , ".//tbody[1]",".//tr[2]" , ".//td[2]" , './/div[@class="mainViewportHolder"]' , './/div[@class="mainViewport"]' , ".//div[1]" , ".//table[1]" , ".//tbody[1]" , ".//tr[2]" , './/td[3]' , ".//table[1]" , ".//tbody[1]" , './/table[@class="inputPanel"]' , ".//tbody[1]" , './/input[@class="txtInput"]'])
        for h in otpt:
            text_box.send_keys(h)

        
        
        
tr = TypeRacer()
tr.OpenNewGame()


while True:
    if(input() == "h"):
        break
    
tr.StartHack()