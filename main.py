import requests
import time
import parsel
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import csv
import io
import db


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
}

START_URL = 'https://stox.quickbase.com/db/bk42uehek?a=q&qid=10'
BASE_URL = 'https://stox.quickbase.com/db/'
OUTPUT_PATH = "D:\Ziegfred\Fiverr\stox\output_path"
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)


def main():
    driver = uc.Chrome(headless=True)
    driver.get(START_URL)
    time.sleep(5)
    style_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@role='switch']"))
    )
    style_button.click()
    date_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'DateRange')]"))
    )
    date_button.click()
    date_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'DateRange')]"))
    )
    date_button.click()
    today_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Today')]"))
    )
    today_button.click()
    done_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Done')]"))
    )
    done_button.click()
    time.sleep(2)
    more_button = driver.find_element(By.ID, "moreAction")
    save_button = driver.find_element(By.ID, "vexpss")
    hover = ActionChains(driver).click(more_button).move_to_element(save_button)
    hover.perform()
    time.sleep(2)
    selector = parsel.Selector(text=driver.page_source)
    download_link = selector.xpath("//a[@id='vexpss']/@href").get()
    file_name = selector.xpath("//span[@class='Display']/text()").get().split(' - ')[0].strip()
    response = requests.get(BASE_URL + download_link)
    strio = io.StringIO(response.text)
    reader = csv.DictReader(strio)
    for r in reader:
        db.save_lead(list(r.values()))

if __name__ == '__main__':
    main()
