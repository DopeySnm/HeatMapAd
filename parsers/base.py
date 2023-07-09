import requests


class Parser:
    def check_value(self, value):
        if value:
            return value.text
        else:
            return None

    def get_coordinates(self, address):
        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": "2a03383b-8ee7-424e-9a47-629074b0c438",
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