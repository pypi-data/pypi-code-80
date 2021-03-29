import os
import platform
import tarfile
import time
import urllib.request
import warnings

import io
import pandas as pd
import requests
import openpyxl
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

try:
    import xlrd
except ModuleNotFoundError:
    pass


def get_download_path():
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


if platform.system() == "Windows":
    uzanti = ".exe"
elif platform.system() == "Linux":
    uzanti = ""
elif platform.system() == "Darwin":
    uzanti = ""


def firefox(developer=False):
    if platform.system() == "Windows":
        if not os.path.isfile(os.path.join(get_download_path(), "geckodriver" + uzanti)):
            r = requests.get(
                "https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-win64.zip")
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(get_download_path())
    elif platform.system() == "Linux":
        if not os.path.isfile(os.path.join(get_download_path(), "geckodriver" + uzanti)):
            thetarfile = "https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz"
            ftpstream = urllib.request.urlopen(thetarfile)
            thetarfile = tarfile.open(fileobj=ftpstream, mode="r|gz")
            thetarfile.extractall(get_download_path())
    elif platform.system() == "Darwin":
        if not os.path.isfile(os.path.join(get_download_path(), "geckodriver" + uzanti)):
            thetarfile = "https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-macos.tar.gz"
            ftpstream = urllib.request.urlopen(thetarfile)
            thetarfile = tarfile.open(fileobj=ftpstream, mode="r|gz")
            thetarfile.extractall(get_download_path())

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", get_download_path())
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/ms-excel')
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    if not developer:
        options.add_argument('--headless')
    driver_path = os.path.join(get_download_path(), "geckodriver" + uzanti)
    driver = webdriver.Firefox(executable_path=driver_path, firefox_profile=profile, options=options)
    return driver


def chrome(developer=False):
    if not os.path.isfile(os.path.join(get_download_path(), "chromedriver" + uzanti)):
        if platform.system() == "Windows":
            r = requests.get("https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_win32.zip")
        elif platform.system() == "Linux":
            r = requests.get("https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip")
        elif platform.system() == "Darwin":
            r = requests.get("https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_mac64.zip")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(get_download_path())

    if platform.system() == "Linux":
        os.chmod(os.path.join(get_download_path(), "chromedriver" + uzanti), 0o755)
    if platform.system() == "Darwin":
        os.chmod(os.path.join(get_download_path(), "chromedriver" + uzanti), 0o755)

    chromeoptions = webdriver.ChromeOptions()
    prefs = {'download.prompt_for_download': False,
             'download.default_directory': get_download_path(),
             'download.directory_upgrage': True,
             'profile.default_content_settings.popups': 0,
             }
    chromeoptions.add_experimental_option('prefs', prefs)
    if not developer:
        chromeoptions.headless = True
    driver_path = os.path.join(get_download_path(), "chromedriver" + uzanti)
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chromeoptions)
    return driver


def aylik_kalem(kalems=None, browser="firefox", dev=False):
    if browser == "firefox":
        driver = firefox(developer=dev)
    if browser == "chrome":
        driver = chrome(developer=dev)
    driver.get("https://www.bddk.org.tr/BultenAylik/tr/Home/Gelismis")
    driver.find_element_by_id("ddlTabloKalem_chosen").click()
    html_list = driver.find_element_by_id("ddlTabloKalem_chosen")
    items = html_list.find_elements_by_tag_name("li")
    if kalems is None:
        for item in items:
            print(item.text)
    else:
        for item in items:
            if kalems.lower() in item.text.lower():
                print(item.text)
    driver.quit()


def aylik_taraf(browser="firefox", dev=False):
    if browser == "firefox":
        driver = firefox(developer=dev)
    if browser == "chrome":
        driver = chrome(developer=dev)
    driver.get("https://www.bddk.org.tr/BultenAylik/tr/Home/Gelismis")
    driver.find_element_by_id("ddlTaraf_chosen").click()
    html_list = driver.find_element_by_id("ddlTaraf_chosen")
    items = html_list.find_elements_by_tag_name("li")
    for item in items:
        print(item.text)
    driver.quit()


def aylik_rapor(kalem, basyil, basay, bityil, bitay, per, para="TL", taraf=None, zaman=120, browser="firefox", dev=False):
    if browser == "firefox":
        driver = firefox(developer=dev)
    if browser == "chrome":
        driver = chrome(developer=dev)
    print("Yukleniyor...")
    driver.get("https://www.bddk.org.tr/BultenAylik/tr/Home/Gelismis")

    # Rapor temizleme
    if os.path.isfile(os.path.join(get_download_path(), 'Rapor.xlsx')):
        os.remove(os.path.join(get_download_path(), 'Rapor.xlsx'))

    # Baslangic yil
    driver.find_element_by_id("ddlBaslangicYil_chosen").click()
    html_list = driver.find_element_by_id("ddlBaslangicYil_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(basyil))].click()

    # Bitis yil
    driver.find_element_by_id("ddlBitisYil_chosen").click()
    html_list = driver.find_element_by_id("ddlBitisYil_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(bityil))].click()

    # Baslangic ay
    driver.find_element_by_id("ddlBaslangicAy_chosen").click()
    html_list = driver.find_element_by_id("ddlBaslangicAy_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(basay))].click()

    # Bitis ay
    driver.find_element_by_id("ddlBitisAy_chosen").click()
    html_list = driver.find_element_by_id("ddlBitisAy_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(bitay))].click()

    # Periyot
    driver.find_element_by_id("ddlPeriyot_chosen").click()
    html_list = driver.find_element_by_id("ddlPeriyot_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(per))].click()

    # Para Birimi
    driver.find_element_by_id("ddlParaBirimi_chosen").click()
    html_list = driver.find_element_by_id("ddlParaBirimi_chosen")
    items = html_list.find_elements_by_tag_name("li")
    text = []
    for item in items:
        text.append(item.text)
    items[text.index(str(para))].click()

    # Kalem
    for i, kal in enumerate(kalem):
        driver.find_element_by_id("ddlTabloKalem_chosen").click()
        html_list = driver.find_element_by_id("ddlTabloKalem_chosen")
        items = html_list.find_elements_by_tag_name("li")
        if kal == kalem[0]:
            text = []
            for item in items:
                text.append(item.text)
        items[text.index(str(kal)) + i].click()

    # taraf
    if taraf is not None:
        for j, tar in enumerate(taraf):
            driver.find_element_by_id("ddlTaraf_chosen").click()
            html_list = driver.find_element_by_id("ddlTaraf_chosen")
            items = html_list.find_elements_by_tag_name("li")
            if tar == taraf[0]:
                text = []
                for item in items:
                    text.append(item.text)
            items[text.index(str(tar)) + j].click()

    # rapor
    driver.find_element_by_id("btnRaporOlustur").click()

    # Excel
    WebDriverWait(driver, zaman).until(EC.element_to_be_clickable((By.ID, "btnExcel")))
    driver.find_element_by_id("btnExcel").click()

    # csv
    warnings.filterwarnings("ignore", category=UserWarning)
    enginexlrd = 0
    try:
        if xlrd.__version__ < "2.0":
            enginexlrd = 1
    except NameError:
        pass
    ilk_zaman = 0
    if enginexlrd == 0:
        while ilk_zaman < zaman:
            time.sleep(1)
            if os.path.isfile(os.path.join(get_download_path(), 'Rapor.xlsx')):
                sonuc = pd.read_excel(os.path.join(get_download_path(), 'Rapor.xlsx'), engine="openpyxl")
                break
            ilk_zaman += ilk_zaman
    elif enginexlrd == 1:
        while ilk_zaman < zaman:
            time.sleep(1)
            if os.path.isfile(os.path.join(get_download_path(), 'Rapor.xlsx')):
                sonuc = pd.read_excel(os.path.join(get_download_path(), 'Rapor.xlsx'))
                break
            ilk_zaman += ilk_zaman
    print("Veri alindi.")
    driver.quit()
    os.remove(os.path.join(get_download_path(), 'Rapor.xlsx'))
    return sonuc


def haftalik_rapor(kalem, bastarih, bittarih, para=None, sutun=None, taraf=None, zaman=30, browser="chrome",
                       dev=False):
    if browser == "firefox":
        driver = firefox(developer=dev)
    if browser == "chrome":
        driver = chrome(developer=dev)
    print("Yukleniyor...")
    driver.get("https://www.bddk.org.tr/BultenHaftalik/tr/Gelismis")

    # Rapor Temizleme
    if os.path.isfile(os.path.join(get_download_path(), 'HaftalikBulten(GelismisGosterim).xls')):
        os.remove(os.path.join(get_download_path(), 'HaftalikBulten(GelismisGosterim).xls'))

    # Bekleme
    WebDriverWait(driver, zaman).until(EC.element_to_be_clickable((By.ID, "Tablolar")))

    # Kalem
    kalem_dict = {
        'Krediler': "Kalemler-253",
        'Takipteki Alacaklar': "Kalemler-254",
        'Menkul Değerler': "Kalemler-255",
        'Mevduat': "Kalemler-256",
        'Diğer Bilanço Kalemleri': "Kalemler-257",
        'Bilanço Dışı İşlemler': "Kalemler-258",
        'Bankalarda Saklanan Menkul Değerler - 1': "Kalemler-259",
        'Bankalarda Saklanan Menkul Değerler - 2': "Kalemler-260",
        'Yabancı Para Pozisyonu': "Kalemler-261",
    }
    for k in kalem:
        time.sleep(zaman/100)
        html_list = driver.find_element_by_id("Tablolar")
        items = html_list.find_elements_by_tag_name("tr")
        text = []
        for item in items:
            text.append(item.text)
        items[text.index(str(k))].click()
        time.sleep(zaman/100)
        # altkalem
        html_list = driver.find_element_by_id(kalem_dict[k])
        items = html_list.find_elements_by_tag_name("tr")
        for item in items:
            time.sleep(zaman/400)
            item.click()
        html_list.find_elements_by_tag_name("i")[0].click()

    # Baslangic Tarihi
    select = Select(driver.find_element_by_id("baslangicTarih"))
    select.select_by_visible_text(bastarih)

    # Bitis Tarihi
    select = Select(driver.find_element_by_id("bitisTarih"))
    select.select_by_visible_text(bittarih)

    # Para Birimi
    if para is not None:
        select = Select(driver.find_element_by_id("CokluPara"))
        select.select_by_visible_text(para)

    # Sutun
    if sutun is not None:
        select = Select(driver.find_element_by_id("kalemSutunSec"))
        select.select_by_visible_text(sutun)

    # Taraf
    if taraf is not None:
        for t in taraf:
            html_list = driver.find_element_by_id("taraflar")
            items = html_list.find_elements_by_tag_name("tr")
            text = []
            for item in items:
                text.append(item.text)
            items[text.index(str(t))].click()

    # Rapor olusturma ve indirme
    driver.find_element_by_id("gelismisRaporGetir").click()
    time.sleep(zaman / 100)
    driver.find_element_by_css_selector("[title^='Excel']").click()

    # csv
    warnings.filterwarnings("ignore", category=UserWarning)
    enginexlrd = 0
    try:
        if xlrd.__version__ < "2.0":
            enginexlrd = 1
    except NameError:
        pass
    ilk_zaman = 0
    if enginexlrd == 0:
        while ilk_zaman < zaman:
            time.sleep(1)
            if os.path.isfile(os.path.join(get_download_path(), 'HaftalikBulten(GelismisGosterim).xls')):
                sonuc = pd.read_html(os.path.join(get_download_path(), 'HaftalikBulten(GelismisGosterim).xls'),
                                     engine="openpyxl")
                break
            ilk_zaman += ilk_zaman
    elif enginexlrd == 1:
        while ilk_zaman < zaman:
            time.sleep(1)
            if os.path.isfile(os.path.join(get_download_path(), 'HaftalikBulten(GelismisGosterim).xls')):
                sonuc = pd.read_html(os.path.join(get_download_path(), 'HaftalikBulten(GelismisGosterim).xls'))
                break
            ilk_zaman += ilk_zaman
    print("Veri alindi.")
    driver.quit()
    os.remove(os.path.join(get_download_path(), 'HaftalikBulten(GelismisGosterim).xls'))
    return sonuc[0]


def haftalik_taraf(browser="chrome", dev=False):
    if browser == "firefox":
        driver = firefox(developer=dev)
    if browser == "chrome":
        driver = chrome(developer=dev)
    driver.get("https://www.bddk.org.tr/BultenHaftalik/tr/Gelismis")

    html_list = driver.find_element_by_id("taraflar")
    items = html_list.find_elements_by_tag_name("tr")
    for item in items:
        print(item.text)
    driver.quit()


def haftalik_kalem(browser="chrome", dev=False):
    if browser == "firefox":
        driver = firefox(developer=dev)
    if browser == "chrome":
        driver = chrome(developer=dev)
    driver.get("https://www.bddk.org.tr/BultenHaftalik/tr/Gelismis")

    html_list = driver.find_element_by_id("Tablolar")
    items = html_list.find_elements_by_tag_name("tr")
    for item in items:
        print(item.text)
    driver.quit()


def haftalik_tarih(tarih="baslangic", browser="chrome", dev=False):
    if browser == "firefox":
        driver = firefox(developer=dev)
    if browser == "chrome":
        driver = chrome(developer=dev)
    driver.get("https://www.bddk.org.tr/BultenHaftalik/tr/Gelismis")

    if tarih == "baslangic":
        print("BASLANGIC TARIHLERI")
        select = Select(driver.find_element_by_id("baslangicTarih"))
        for option in select.options:
            print(option.text)

    if tarih == "bitis":
        print("BITIS TARIHLERI")
        select = Select(driver.find_element_by_id("bitisTarih"))
        for option in select.options:
            print(option.text)
    driver.quit()

