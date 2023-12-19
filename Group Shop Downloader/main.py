import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import json
import re

def clean_text(text):
    # Add your own text cleaning logic here
    cleaned_text = re.sub(r'[^\w\s.-]', '', text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def scrape_roblox_images():
    URL = "GROUP CLOTHES SHOP HERE"
    IDs = []
    names = []
    IDsDict = {}
    output_dir = 'clothes'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    driver = webdriver.Chrome()
    driver.implicitly_wait(6)
    driver.get(URL)
    mainSec = driver.find_element(By.CSS_SELECTOR, '.hlist.item-cards-stackable.ng-scope')
    elementList = mainSec.find_elements(By.CLASS_NAME , 'item-card-container')

    for x in elementList:
        link_element = x.get_attribute('href').split('/')
        xStr = x.text[0:x.text.find("By ")]
        if len(link_element) == 1:
            pass
        else:
            names.append(xStr)
            num = link_element[4]
            IDs.append(num)
            IDsDict.update({num: xStr})

    time.sleep(1)
    for x in IDsDict:
        driver.get("https://assetdelivery.roblox.com/v1/assetId/" + x)
        mainSTR = driver.find_element(By.XPATH, "/html/body/pre").text
        link = str(json.loads(mainSTR)["location"])
        try:
            pngID = str(requests.get(link).content).split('<url>http://www.roblox.com/asset/?id=')[1].split('</url>')[0]
            driver.get("https://assetdelivery.roblox.com/v1/assetId/" + pngID)
            mainSTR = driver.find_element(By.XPATH, "/html/body/pre").text
            link = str(json.loads(mainSTR)["location"])

            cleaned_text = clean_text(IDsDict.get(x))
            filename = f'{cleaned_text}.png'

            if os.path.exists(os.path.join(output_dir, filename)):
                counter = 1
                while True:
                    new_filename = f'{cleaned_text}_{counter}.png'
                    if not os.path.exists(os.path.join(output_dir, new_filename)):
                        filename = new_filename
                        break
                    counter += 1

            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(requests.get(link).content)
                print(f"{x} was saved to {filename}")
        except IndexError:
            print("not pants or shirt")

    driver.quit()

if __name__ == "__main__":
    scrape_roblox_images()
