# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки
# HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml,
# чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
# Ваш код должен включать следующее:
# Строку агента пользователя в заголовке HTTP-запроса,
# чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных
# таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.

# Импорт необходимых библиотек
import requests
from lxml import html
import csv

# Определение целевого URL
url = "https://www.gb.ru/posts"

# Отправка HTTP GET запроса на целевой URL
# с пользовательским заголовком User-Agent
response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

# Парсинг HTML-содержимого ответа с помощью библиотеки lxml
tree = html.fromstring(response.content.decode('utf-8'))

# Использование выражения XPath для выбора
# всех блоков постов с классом 'post-item event'
posts = tree.xpath("//div[@class='post-item event']")

data = []


def get_description(list_element):
    try:
        return list_element[0]
    except:
        return "Нет описания"


for post in posts:
    data.append({
        'title': post.xpath(".//a[contains(@class, 'h3')]/text()")[0],
        'description': get_description(
            post.xpath(".//div[@class='m-t-sm']//span/text()")),
        'date': post.xpath(".//div[contains(@class, 'm-t-xs')]/text()")[0],
        'views': int(post.xpath(
            ".//div[contains(@class, 'post-counter')]/span/text()")[0]),
        'comments': int(post.xpath(
            ".//div[contains(@class, 'post-counter')]/span/text()")[1])
    })

# print(data)
# print(len(data))

with open('homework/hw4/hw4.csv', 'w', encoding='utf-8') as output:
    write = csv.DictWriter(
        output, ['title', 'description', 'date', 'views', 'comments'])
    write.writeheader()
    write.writerows(data)
