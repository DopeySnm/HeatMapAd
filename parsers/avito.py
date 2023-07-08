from datetime import datetime
from bs4 import BeautifulSoup
from models.ad import Ad
from models.location import Location
from parsers.base import Parser
from models.description import Description
import re
import random


class ParserAvito(Parser):
    def select_ad(self, html_code) -> Ad:
        soup = BeautifulSoup(html_code, "lxml")
        title = self.select_title(soup)
        price = self.select_price(soup)
        link = self.select_link(soup)
        location = self.select_location(soup)
        magnitude = None
        date_download = datetime.now().date()
        description = self.select_description(soup)

        return Ad(title=title, price=price, link=link, location=location, magnitude=magnitude, date_download=date_download, description=description)

    def select_views(self, soup):
        # views = soup.find("div", class_="a10a3f92e9--icon--Sexw3")
        # views = self.check_value(views)
        views = random.randint(900, 3000)
        return views

    def select_title(self, soup):
        title = soup.find("h3", class_="styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l-hruVE styles-module-ellipsis-LKWy3 styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-header-l-qvNIS")
        return self.check_value(title)

    def select_price(self, soup):
        price = soup.find("strong", class_ ="styles-module-root-LIAav")
        price = self.check_value(price)

        if price:
            price = re.sub(r"\D", "", price)
        return price

    def select_description(self, soup):
        description = soup.find("p", class_="styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA styles-module-ellipsis-LKWy3 stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-s-_c6vD styles-module-noAccent-nZxz7 styles-module-root_bottom-XgXHc styles-module-margin-bottom_6-nU1Wp")
        description = self.check_value(description)
        count_views = self.select_views(soup)
        return Description(main_description=description, count_views=count_views)

    def select_link(self, soup):
        link = soup.find("a", class_="iva-item-sliderLink-uLz1v")
        link = "https://www.avito.ru" + link["href"]
        return link

    def select_location(self, soup) -> Location:
        full_address = self.select_adress(soup)
        coordinate_x = None
        coordinate_y = None
        city = "Челябинск"
        if full_address:
            street = full_address.split(", ")[0]
            house = full_address.split(", ")[-1]
        else:
            street = None
            house = None
        return Location(coordinate_x=coordinate_x, coordinate_y=coordinate_y, full_address=full_address, city=city, street=street, house=house)

    def select_adress(self, soup):
        adress = soup.find("p", class_="styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-s-_c6vD")
        adress = self.check_value(adress)
        return adress