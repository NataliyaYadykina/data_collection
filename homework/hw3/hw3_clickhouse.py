from clickhouse_driver import Client
import json
from pprint import pprint

# Подключение к серверу ClickHouse
client = Client(host='localhost', user='default', port=9000, password='123')

# Создание базы данных (если она не существует)
client.execute('CREATE DATABASE IF NOT EXISTS hw3')

# Создание таблицы
client.execute('''
CREATE TABLE IF NOT EXISTS hw3.books (
    id UInt64 primary key,
    name String,
    url String,
    price Float,
    instock Int64,
    description String
) ENGINE = MergeTree()
ORDER BY id
''')

print("Таблица создана успешно.")

with open('hw3.json', 'r') as file:
    data = json.load(file)

# Вставка данных в таблицу
for book in data:

    # Вставка данных
    client.execute("""
    INSERT INTO hw3.books (
        name, url,
        price, instock, description
    ) VALUES""",
                   [(
                       book['name'] or "",
                       book['url'] or "",
                       book['price'] or "",
                       book['instock'] or "",
                       book['description'] or "")])

print("Данные введены успешно.")

# Проверка успешности вставки
result = client.execute("SELECT * FROM hw3.books")
pprint(result[0])
