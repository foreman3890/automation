from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import csv
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
driver_path = 'chromedriver.exe'
url = 'http://192.168.9.1/html/content.html#home'
options = webdriver.ChromeOptions()
service = ChromeService(executable_path=driver_path)


def checkWindowsOpen():
    current = driver.current_window_handle
    multi_window = driver.window_handles

    for window in multi_window:
        if window != current:
            driver.switch_to.window(window)
            driver.close()
    driver.switch_to.window(current)


def checkConnectInternet(url):
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False
    print('connected' if connect() else 'no internet!')


def check_exists_by_class(class_ele):
    try:
        driver.find_element(By.CLASS_NAME, class_ele)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_xpath(xpath_ele):
    try:
        driver.find_element(By.XPATH, xpath_ele)
    except NoSuchElementException:
        return False
    return True


def check_click_by_class(class_ele):
    try:
        driver.find_element(By.CLASS_NAME, class_ele).click()
    except ElementClickInterceptedException:
        return False
    return True


def connectToWebsite():
    time.sleep(2)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(2)

    # nhập vào input password
    input_psw = driver.find_element(By.ID, 'password')
    input_psw.send_keys('cadgasuet1@')  # nhập vào mật khẩu metamask

    if (check_click_by_class('button.btn--rounded.btn-default') == False):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'button.btn--rounded.btn-secondary'))).click()
        networks = driver.find_elements(By.TAG_NAME, 'li')
        networks[0].click()
        # click vào button unlock
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/button'))).click()
        print('ko click được')
    else:
        # click vào button unlock
        print('click đc')
    print('Connected Success with site')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def reConnectDcom():
    time.sleep(2)
    print('Get token completed')
    # Xử lý với cửa sổ dcom
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element(By.CLASS_NAME, 'ic_reboot').click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, 'btn_normal_short.pull-left.margin_left_12'))).click()
    time.sleep(4)
    driver.quit()


def get_token():
    driver.execute_script(
        "window.open('https://labs.zetachain.com/get-zeta');")
    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 20).until(EC.visibility_of_any_elements_located(
        (By.XPATH, '//*[@id="__next"]/div/div/main/div/div[1]/div[3]')))

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/main/div/div[1]/button[2]'))).click()

    time.sleep(1)

options.add_argument('--load-extensions')
options.add_argument('--disable-software-rasterizer')
# options.add_argument("excludeSwitches", ["enable-logging"])
options.add_argument(
    "user-data-dir=C:/Users/DreamStore/AppData/Local/Google/Chrome/User Data")

file = open('info.csv')
reader = csv.reader(file, delimiter=',')

for row in reader:
    time.sleep(2)
    print(row[0])
    options.add_argument('--profile-directory=%s' % (row[0]))  # e.g. Profile 3
    driver = webdriver.Chrome(service=service, options=options)

    n = 0  # biến kiểm tra connect internet
    while (n < 1):
        if (checkConnectInternet(url) == True):
            driver.get(url)
            n = 1
        else:
            time.sleep(1)
    
    checkWindowsOpen()

    connectToWebsite()

    checkWindowsOpen()

    # driver.switch_to.window(driver.window_handles[0])
    # checkWindowsOpen()
    # time.sleep(1)

    # driver.execute_script(
    #     "window.open('https://labs.zetachain.com/swap');")
    # driver.switch_to.window(driver.window_handles[1])

    get_token()

    reConnectDcom()

file.close()
