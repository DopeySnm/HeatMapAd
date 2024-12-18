import requests
import random


class Parser:
    def check_value(self, value):
        if value:
            return value.text
        else:
            return None

    def get_coordinates(self, address):
        base_url = "https://geocode-maps.yandex.ru/1.x"
        API = ["bbabb904-f267-4246-8120-2a1235a3d785", "c5b657e2-a966-4f81-8b3f-7681db6fbb37", "bbabf1e2-3749-4076-b863-eac9711b5d7b", "cdc3fb00-237e-4f3c-a197-ac18c2f3fd67"]
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": random.choice(API),
            "format": "json",
        })
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lon, lat

if __name__ == "__main__":
    addres = "Москва, Серебряническая набережная, 19"
    print(Parser().get_coordinates(addres))