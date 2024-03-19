from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json

url_base = "https://fitosila.ru/"
query = "чай"

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)

driver.get(url_base)

time.sleep(4)
input = driver.find_element(By.ID, 'title')
input.send_keys(query)
input.send_keys(Keys.ENTER)

time.sleep(4)

products = []

while True:
    time.sleep(5)
    cards = driver.find_elements(
        By.XPATH, "//div[@id='indexerproduct']//div[contains(@class, 'item')]")
    print(cards[0])

    for card in cards:
        name = card.find_element(
            By.XPATH, ".//div[@class='head']/a").get_attribute('title')
        articul = card.find_element(
            By.XPATH, ".//div[@class='head']/span").text
        price = card.find_element(
            By.XPATH, ".//div[@class='col col-7 small strong']/span").text
        url = card.find_element(
            By.XPATH, ".//div[@class='head']/a").get_attribute('href')
        product_info = {
            'name': name,
            'articul': articul,
            'price': price,
            'url': url
        }
        products.append(product_info)

    try:
        button = card.find_element(
            By.XPATH, "//li[@class='next']/a")
        button.click()
    except Exception:
        break

with open('homework/hw7/hw7.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False)

print(len(products))
