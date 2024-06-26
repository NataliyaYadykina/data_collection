import requests
import json
# import os
# from dotenv import load_dotenv

# dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     print('Not found env')

url = "https://api.foursquare.com/v3/places/search"

query = input(
    'Введите категорию для поиска (например, кофейни, парки, рестораны и т.д.): ')

headers = {
    "accept": "application/json",
    "Authorization": 'fsq3qokEN4ucJRwc8D8oPNMbL6c+s1j5qCSzlFXLTDRBFaA='
}

params = {
    "query": query
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print("Результаты:")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        print("Название:", venue["name"])
        print("Страна:", venue["location"]["country"])
        if 'address' in venue["location"].keys():
            print("Населенный пункт:", venue["location"]["locality"])
        else:
            print("Населенный пункт:", "Не указан")
        if 'address' in venue["location"].keys():
            print("Адрес:", venue["location"]["address"])
        else:
            print("Адрес:", "Не указан")
        print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:",
          response.status_code)
    print(response.text)
