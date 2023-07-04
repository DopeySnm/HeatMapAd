from datetime import datetime
from bs4 import BeautifulSoup
from model.ad import Ad
from model.location import Location
from parsers.base import Parser
from model.description import Description


class ParserAvito(Parser):
    def select_ad(self, html_code) -> Ad:
        soup = BeautifulSoup(html_code, "lxml")
        title = self.select_title(soup)
        price = self.select_price(soup)
        link = self.select_link(soup)
        location = self.select_location(soup)
        magnitude = None
        data_download = str(datetime.now().date())
        description = self.select_description(soup)
        return Ad(title=title, price=price, link=link, location=location, magnitude=magnitude, data_download=data_download, description=description)


    def select_title(self, soup):
        title = soup.find("h3", class_="styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l-hruVE styles-module-ellipsis-LKWy3 styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-header-l-qvNIS")
        return self.check_value(title)

    def select_price(self, soup):
        price = soup.find("strong", class_ ="styles-module-root-LIAav")
        price = self.check_value(price)

        if price:
            price = price.split("&nbsp;")
            price = "".join(price)
            price = price[:-1:]
        return price

    def select_description(self, soup):
        description = soup.find("p", class_="styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA styles-module-ellipsis-LKWy3 stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-s-_c6vD styles-module-noAccent-nZxz7 styles-module-root_bottom-XgXHc styles-module-margin-bottom_6-nU1Wp")
        description = self.check_value(description)
        return Description(main_description=description)

    def select_link(self, soup):
        link = soup.find("a", class_="iva-item-sliderLink-uLz1v")
        link = "https://www.avito.ru" + link["href"]
        return link

    def select_location(self, soup) -> Location:
        adress = self.select_adress(soup)
        coordinate_x = None
        coordinate_y = None
        city = None
        district = None
        street = None
        house = None
        flat = None
        return adress

    def select_adress(self, soup):
        adress = soup.find("p", class_="styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-s-_c6vD")
        adress = self.check_value(adress)
        return adress