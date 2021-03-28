#e-denvnik auth api
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ednevnik:
    def __init__(self,username,passowrd,path):
        self.username = username
        self.password = passowrd
        self.path = path

    def auth(self):

        state = True

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(self.path, options=chrome_options)

        driver.get("https://ocjene.skole.hr/login")

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        submit = driver.find_element_by_xpath('//input[@type="submit"]')

        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

        if driver.current_url == 'https://ocjene.skole.hr/course':  return state
        else:
            state = False
            return state

    def grade(self):

        state = True

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(self.path, options=chrome_options)

        driver.get("https://ocjene.skole.hr/login")

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        submit = driver.find_element_by_xpath('//input[@type="submit"]')

        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

        if driver.current_url == 'https://ocjene.skole.hr/course': state = True
        else:   state = False

        if state:
            grade_position = driver.find_element_by_xpath('//*[@id="class-administration-menu"]/div[1]/div/div[1]/span[1]')
            grade = grade_position.text
            return grade

    def nameSurname(self):

        state = True

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(self.path, options=chrome_options)

        driver.get("https://ocjene.skole.hr/login")

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        submit = driver.find_element_by_xpath('//input[@type="submit"]')

        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

        if driver.current_url == 'https://ocjene.skole.hr/course':  state = True
        else:   state = False

        if state:
            nameSurnamePosition = driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/span')
            nameSurname = nameSurnamePosition.text
            return nameSurname

    def userNumber(self):

        state = True

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(self.path, options=chrome_options)

        driver.get("https://ocjene.skole.hr/login")

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        submit = driver.find_element_by_xpath('//input[@type="submit"]')

        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

        if driver.current_url == 'https://ocjene.skole.hr/course':  state = True
        else:   state = False

        if state:
            driver.get("https://ocjene.skole.hr/personal_data")
            userNumberPosition = driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[4]/div/div[2]/span[2]')
            userNumber = userNumberPosition.text
            return userNumber


    def userInfo(self):

        information = []

        state = True

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(self.path, options=chrome_options)

        driver.get("https://ocjene.skole.hr/login")

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        submit = driver.find_element_by_xpath('//input[@type="submit"]')

        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

        if driver.current_url == 'https://ocjene.skole.hr/course':  state = True
        else:   state = False

        if state:
            grade_position = driver.find_element_by_xpath('//*[@id="class-administration-menu"]/div[1]/div/div[1]/span[1]')
            grade = grade_position.text
            information.append(grade)
            nameSurnamePosition = driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/span')
            nameSurname = nameSurnamePosition.text
            information.append(nameSurname)
            driver.get("https://ocjene.skole.hr/personal_data")
            userNumberPosition = driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[4]/div/div[2]/span[2]')
            userNumber = userNumberPosition.text
            information.append(userNumber)
            return information