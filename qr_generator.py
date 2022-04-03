import os
if not os.path.exists('generated'):
    os.makedirs('generated')

import json
def load_config(category, setting):
    with open("config.json") as f:
        cfg_data = json.load(f)

    return cfg_data[category][setting]

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import base64
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, executable_path=load_config("chromedriver", "path"))

driver.get('https://discord.com/login')

try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, load_config("discord", "qr_class")))
    WebDriverWait(driver, 10).until(element_present)
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, features='lxml')

    div = soup.find('div', {'class': load_config("discord", "qr_class")})
    qr_code = div.find('img')['src']
    file = os.path.join(os.getcwd(), 'generated/qr_code.png')

    img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

    with open(file,'wb') as handler:
        handler.write(img_data)

    print('QR Code saved to: ' + file)
    print("Waiting for QR Code to be scanned...")

    while driver.current_url == "https://discord.com/login":
        time.sleep(1)
    
    print("logged")
    input()

except TimeoutException:
    print("Timed out waiting for page to load") 
