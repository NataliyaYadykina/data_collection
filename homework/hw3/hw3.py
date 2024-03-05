from pymongo import MongoClient
import json
from pprint import pprint

# Создаем подключение к Mongodb локально
client = MongoClient('mongodb://localhost:27017')

# Загрузим из файла json данные о книгах, полученные с помощью скрейпинга
with open('homework/hw3/hw3.json', 'r', encoding='utf8') as file:
    data = json.load(file)

# Создаем базу данных
db = client.hw3
books = db.books

books.delete_many({})

# Записываем документы в базу данных
for book in data:
    db.books.insert_one(book)

# Получение количества документов в коллекции
# с помощью функции count_documents()
count = books.count_documents({})
print(f'Число записей в базе данных: {count}')

# фильтрация документов по критериям
query = {"name": "Ajin: Demi-Human, Volume 1 (Ajin: Demi-Human #1)"}
print(
    f"Книга с заголовком 'Ajin: Demi-Human, Volume 1 (Ajin: Demi-Human #1)'"
)
pprint(books.find_one(query))

query = {"instock": {"$lt": 5}}
print(
    f"Количество книг в наличии менее 5: {books.count_documents(query)}")

# Использование оператора $regex
query = {"name": {"$regex": "[L,l]ight"}}
print(
    f"Количество документов, содержащих в заголовке 'Light' или 'light': {books.count_documents(query)}"
)

# Запросим данные о книгах из базы данных и выведем их в консоль
# for doc in db.books.find():
#     pprint(doc)
