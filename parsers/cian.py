from bs4 import BeautifulSoup
from datetime import datetime
from models.ad import Ad
from models.description import Description
from models.location import Location
from parsers.base import Parser
import re
import unicodedata
import requests

class ParserCian(Parser):
    def select_ad(self, html_page) -> Ad:
        """
        Функция собирает обьект объявления и возвращает его
        :param html_page: str
        :return: Ad
        """
        soup = BeautifulSoup(html_page, "lxml")
        title = self.select_title(soup)
        price = self.select_price(soup)
        link = self.select_link(soup)
        location = self.select_location(soup)
        magnitude = None
        date_download = datetime.now().date()
        description = self.select_description(soup)
        return Ad(title=title, price=price, link=link, location=location, magnitude=magnitude, date_download=date_download, description=description)

    def get_links_ads(self, html_code):
        soup = BeautifulSoup(html_code, "lxml")
        result_lst_links = []
        for name in soup.find_all('div', class_="_93444fe79c--content--lXy9G"):
            link_ad = name.find('a', class_="_93444fe79c--link--eoxce")['href']
            result_lst_links.append(link_ad)
        return "\n".join(result_lst_links)

    def select_location(self, soup):
        full_address = self.select_adress(soup)

        search_street = " ".join(full_address.split(", ")[2::])
        result_search = re.search(r"улица|ул\. ([\w\s]+)", search_street)
        if result_search:
            street = result_search.group(1)
        else:
            street = None

        city = full_address.split(", ")[1]

        if "жилой" not in full_address.lower().split(", ")[-1]:
            house = full_address.split(", ")[-1]
        else:
            house = None

        coordinates = self.get_coordinates(full_address)
        coordinate_x = coordinates[0]
        coordinate_y = coordinates[1]
        return Location(coordinate_x=coordinate_x, coordinate_y=coordinate_y, full_address=full_address, city=city, street=street, house=house)

    def get_coordinates(self, address):
        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": "9cfd6268-5f4f-4982-b912-676c37ec09dd",
            "format": "json",
        })
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lon, lat

    def select_adress(self,soup):
        box_adress = soup.find("div", class_="a10a3f92e9--header-information--w7fS9")
        adress = box_adress.find("div", {"data-name": "Geo"})
        adress = adress.find("span", itemprop="name")["content"]
        return adress

    def select_link(self, soup):
        link = soup.find("meta", property="og:url")["content"]
        return link

    def select_price(self, soup):
        price = soup.find("div", class_="a10a3f92e9--amount--ON6i1")
        price = self.check_value(price)
        if price:
            price = re.sub(r"\D", "", price)
        return price

    def select_title(self, soup):
        title = soup.find("h1", class_="a10a3f92e9--title--vlZwT")
        return self.check_value(title)

    def select_description(self, soup):
        main_description = self.select_main_description(soup)

        mini_info_boxes = self.select_mini_info(soup)

        if "Этаж" in mini_info_boxes:
            floor = mini_info_boxes["Этаж"]
            floor = re.findall(r'\d+', floor)[0]
        else:
            floor = None
        if "Отделка" in mini_info_boxes:
            repair = mini_info_boxes["Отделка"]
        else:
            repair = None
        if "Общая площадь" in mini_info_boxes:
            total_area = mini_info_boxes["Общая площадь"]
            total_area = total_area.replace(" м2", "").replace(",", ".")
        else:
            total_area = None

        box_about_flat = self.select_about_flat(soup)
        if "Тип жилья" in box_about_flat:
            housing_type = box_about_flat["Тип жилья"]
        else:
            housing_type = None
        if "Общая площадь" in box_about_flat:
            total_area = box_about_flat["Общая площадь"]
            total_area = total_area.replace(" м2", "").replace(",", ".")
        if "Жилая площадь" in box_about_flat:
            living_area = box_about_flat["Жилая площадь"]
            living_area = living_area.replace(" м2", "").replace(",", ".")
        else:
            living_area = None

        bathroom = None
        year_built = None

        return Description(main_description=main_description,total_area=total_area,floor=floor,living_area=living_area,housing_type=housing_type,bathroom=bathroom,repair=repair,year_built=year_built)

    def select_about_flat(self, soup):
        data = soup.find_all("div", class_="a10a3f92e9--group--K5ZqN")
        result_dir = {}
        for box in data:
            name_charactiristic = box.find("p",class_="a10a3f92e9--color_gray60_100--MlpSF a10a3f92e9--lineHeight_22px--bnKK9 a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__normal--xbqP6")
            name_charactiristic = self.check_value(name_charactiristic)
            name_charactiristic = unicodedata.normalize('NFKD', name_charactiristic)
            value_charactiristic = box.find("p", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_22px--bnKK9 a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__normal--xbqP6")
            value_charactiristic = self.check_value(value_charactiristic)
            value_charactiristic = unicodedata.normalize('NFKD', value_charactiristic)
            result_dir[name_charactiristic] = value_charactiristic
        return result_dir

    def select_mini_info(self, soup):
        """
        Функция собирает мини данные под фото объявления, можно обратиться к каждому виду характеристики по его названию
        :param soup: BeautifulSoup
        :return: dir
        """
        data = soup.find_all("div", class_="a10a3f92e9--item--Jp5Qv")
        result_dir = {}
        for box in data:
            name_charactiristic = box.find("span", "a10a3f92e9--color_gray60_100--MlpSF a10a3f92e9--lineHeight_4u--fix4Q a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_12px--EdtE5 a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__0--mdnqq")
            name_charactiristic = self.check_value(name_charactiristic)
            name_charactiristic = unicodedata.normalize('NFKD', name_charactiristic)
            value_charactiristic = box.find("span", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_6u--A1GMI a10a3f92e9--fontWeight_bold--ePDnv a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG")
            value_charactiristic = self.check_value(value_charactiristic)
            value_charactiristic = unicodedata.normalize('NFKD', value_charactiristic)
            result_dir[name_charactiristic] = value_charactiristic
        return result_dir

    def select_main_description(self, soup):
        """
        Функция достает главное описание объявления
        :param soup: BeautifulSoup object
        :return: str or None
        """
        descriprion = soup.find("span", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_6u--A1GMI a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__0--mdnqq a10a3f92e9--text_whiteSpace__pre-wrap--scZwb")
        return self.check_value(descriprion)

if __name__ == "__main__":
    s = "12345"
    print(s[2::])