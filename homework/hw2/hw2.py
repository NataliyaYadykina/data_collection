# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
# и извлечь информацию о всех книгах на сайте во всех категориях:
# название, цену, количество товара в наличии
# (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import re
import json

ua = UserAgent()

url = 'http://books.toscrape.com/catalogue/'
page_number = 1
headers = {"User-Agent": ua.random}

all_books = []

while True:
    links = []

    url_page = f'page-{page_number}.html'
    response = requests.get(url + url_page, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', {'class': 'product_pod'})

    # Парсинг ограниченного количества страниц
    # if page_number == 3:
    #     break

    # Парсинг всех страниц
    if response.status_code != 200:
        break

    for book in books:
        links.append(url + book.find('a').get('href'))

    for link in links:
        book_info = {}

        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        book_main = soup.find('div', {'class': 'product_main'})

        name_info = book_main.find('h1')
        book_info['name'] = name_info.getText()
        book_info['url'] = link

        price_info = book_main.find('p', {'class': 'price_color'})
        price = price_info.getText()
        price = float(re.sub(r'[^\d.]+', '', price))
        book_info['price'] = price

        instock_info = book_main.find('p', {'class': 'instock'})
        instock = instock_info.getText()
        instock = int(re.sub(r'[^\d.]+', '', instock))
        book_info['instock'] = instock

        try:
            description_info = soup.find(
                'div', {'id': 'product_description'}).find_next_sibling('p')
            description = description_info.getText()
            book_info['description'] = description
        except:
            print(f'Not description, book: {book_info["name"]}')
            book_info['description'] = None

        all_books.append(book_info)

    print(f"Обработана {page_number} страница.")
    page_number += 1

with open('homework/hw2/hw2.json', 'w') as f:
    json.dump(all_books, f)

pprint(all_books)
pprint(len(all_books))
