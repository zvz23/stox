import requests
import time
import parsel
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import csv
import io
import db
import os
from sheets import append_rows
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')



HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
}

START_URL = 'https://stox.quickbase.com/db/bk42uehek?a=q&qid=10'
BASE_URL = 'https://stox.quickbase.com/db/'


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
    response = requests.get(BASE_URL + download_link)
    with open('test.csv', 'wb') as f:
        for data in response.iter_content(128):
            f.write(data)

    strio = io.StringIO(response.text)
    reader = csv.DictReader(strio)
    rows = []
    for row in reader:
        stox_id = row['STOX#'].strip()
        if not db.is_stox_exists(stox_id):
            rows.append(list(row.values()))
            db.save_stox(stox_id)
    append_rows(SPREADSHEET_ID,'Sheet1', rows)
    


if __name__ == '__main__':
    main()
