import struct
import traceback

import requests
from bs4 import BeautifulSoup

class Organization:
    Name: str
    Address: str
    Type: str
    Head: str
    Phone: str
    Number: str
    Special: str

class Crawller:
    def start(self):
        a = requests.get('https://chel-edu.ru/organisations/')
        html = a.text
        bs = BeautifulSoup(html, 'xml')
        regions = []
        objects = []
        #looking for regions of city and appending links on them
        for region in bs.find('div', class_='fa_categories').findChildren('a'):
            regions.append(region['href'])
        for r in regions:
            n = r.split('?')
            l = n[0] + '?col=' + str(0) + '&' + n[1]
            objects.extend(self.extract_objects_from_region(r))
        print(len(objects))
        for obj in objects:
            print(obj)

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

    def parse_data(self, something):
        organizations = []
        for item in something:
            org = Organization()
            org.Name = item.find('a').text
            strong_elements = item.find_all('strong', class_='autor')
            for strong in strong_elements:
                next_sibling = strong.next_sibling
                if next_sibling and next_sibling.string:
                    info = next_sibling.string.strip()
                    if str(strong).__contains__('Местоположение'):
                        org.Address = info
                    elif str(strong).__contains__('Адрес'):
                        org.Address = info
                    elif str(strong).__contains__('Тип'):
                        org.Type = info
                    elif str(strong).__contains__('Директор'):
                        org.Head = info
                    elif str(strong).__contains__('Телефон'):
                        org.Number = info
                    print(info)
            organizations.append(org)
        return organizations

crawller = Crawller()
crawller.start()