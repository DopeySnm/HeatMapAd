import time
import traceback
from geopy.geocoders import Photon
import requests
from bs4 import BeautifulSoup
from model.infrastructure import Infrastructure
from model.location import Location


class Crawller:
    def start(self):
        a = requests.get('https://chel-edu.ru/organisations/')
        html = a.text
        bs = BeautifulSoup(html, 'xml')
        regions = []
        objects = []
        parser = Parser()
        #looking for regions of city and appending links on them
        for region in bs.find('div', class_='fa_categories').findChildren('a'):
            regions.append(region['href'])
        for r in regions:
            n = r.split('?')
            l = n[0] + '?col=' + str(0) + '&' + n[1]
            objects.extend(parser.extract_objects_from_region(r))
        print(len(objects))
        for obj in objects:
            print(obj)
class Parser:
    def extract_objects_from_region(self, link: str):
        objects = []
        e = 0
        src = BeautifulSoup(requests.get(link).text, 'xml')
        try:
            while True:
                e += 1
                something = src.find_all('div', class_='item')
                end = src.find('div', class_='faq').findChildren('p')
                if len(end) != 0: raise Exception()
                objects.extend(self.parse_data(something))
                n = link.split('?')
                new_link = n[0] + '?col=' + str(e) + '&' + n[1]
                src = BeautifulSoup(requests.get(new_link).text, 'xml')
        except Exception:
            print(traceback.format_exc())
        return objects


    def get_coordinate(address: str) -> tuple:
        """
        В функцию постпает строка вида "Город, улица, дом", недопустима передача строки "Город, район, улица, дом" или "Город, район, жилой комплекс"
        :param adress: строка вида "Город, улица, дом"
        :return: tuple вида (долгота, широта)
        """
        geolocator = Photon()
        location = geolocator.geocode(address)
        time.sleep(1)
        print(location.latitude, location.longitude)
        return (location.latitude, location.longitude)

    def parse_address(self, addr):
        new_addr = addr.split(',')
        if new_addr[0] == 454136:
            e = 11
        result: str
        if new_addr.__len__() == 4:
            result = 'Челябинск' + ',' + new_addr[2] + ',' + new_addr[3]
        else:
            if (new_addr[1].__contains__('пр-т')): new_addr[1].replace('пр-т', 'проспект')
            result = 'Челябинск' + ',' + new_addr[1] + ',' + new_addr[2]
        return result

    def parse_data(self, data):
        organizations = []
        for item in data:
            title = item.find('a').text
            strong_elements = item.find_all('strong', class_='autor')
            for strong in strong_elements:
                next_sibling = strong.next_sibling
                if next_sibling and next_sibling.string:
                    info = next_sibling.string.strip()
                    if str(strong).__contains__('Местоположение'):
                        district = info
                    elif str(strong).__contains__('Адрес'):
                        addr = info
                    elif str(strong).__contains__('Тип'):
                        org_type = info
                    print(info)
            result = Parser().parse_address(addr)
            city = result[0]
            street = result[1]
            house = result[2]
            location = Location(Parser.get_coordinate(result), district, city, street, house)
            oranization = Infrastructure(title=title, type=org_type, location=location)
            organizations.append(oranization)
        return organizations

crawller = Crawller()
crawller.start()