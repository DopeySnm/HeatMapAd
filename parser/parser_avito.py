from datetime import datetime
from shlex import join

from bs4 import BeautifulSoup

from main import soup
from models.ad import Ad
from models.location import Location
from parser_i import Interface


class Parser_avito(Interface):

    def __init__(self):
        pass
    #def select_info_about_apartment(self, html_page) -> Ad:
    #    soup = BeautifulSoup(html_page, "lxml")
       # name = soup.find("span", class_="title-info-title-text")
      #  price = soup.find("span", class_="priceCurrency")
      #  discription = soup.find("div", class_="style-item-description-html-qCwUL")
      #  type_ = soup.find("span", itemprop="name")
      #  link = soup.find("link", rel="canonical")
       # city = self.select_city(soup)
       # address = soup.find("span", class_="style-item-address__string-wt61A")
       # return Ad(name, price, discription, type_, link, city, address)

    def select_info_about_apartment(self, html_page) -> Ad:
        title = self.select_values(self.select_title())
        price = self.select_values(self.select_price())
        link = self.select_values(self.select_link())
        location = self.select_values(self.select_info_about_location())
        magnitude = self.select_values(self.select_magnitude())
        data_download =self.select_values(self.select_data_download())
        description = self.select_values(self.select_discription_main())
        return Ad(title, price, link, location, magnitude, data_download, description)


    def select_title(self):
        title = soup.find("h3", class_="styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF "
                                        "styles-module-size_l-hruVE styles-module-ellipsis-LKWy3 "
                                        "styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq "
                                        "stylesMarningNormal-module-header-l-qvNIS").text
        return title
    def select_price(self):
        price = soup.find(class_ ="styles-module-root-LIAav").find("span").text
        p = price.split("<", [0])
        str = join(p)
        p1 = str.replace("&nbsp;")
        return p1

   # class ="styles-module-root-LIAav" > < span class ="" > 27 & nbsp;000 < !-- --> & nbsp;₽ < !-- --> & nbsp; < !-- -->в месяц < /span > < /strong >

    def select_description_main(self):
        discr = soup.find("p", class_="styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA "
                                     "styles-module-ellipsis-LKWy3 stylesMarningNormal-module-root-OSCNq "
                                     "stylesMarningNormal-module-paragraph-s-_c6vD styles-module-noAccent-nZxz7 "
                                     "styles-module-root_bottom-XgXHc styles-module-margin-bottom_6-nU1Wp")
        return discr.text

    def select_link(self):
        link = soup.find(class_="iva-item-sliderLink-uLz1v").find("href").text
        return link

    def select_total_area(self):
        title = soup.find("h3", class_="styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF "
                                       "styles-module-size_l-hruVE styles-module-ellipsis-LKWy3 "
                                       "styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq "
                                       "stylesMarningNormal-module-header-l-qvNIS").text
        t = title.split(",",[1])
        t1 = t.split("&",[0])
        return t1
    def select_floor(self):
        floor = soup.find("h3", class_="styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF "
                                        "styles-module-size_l-hruVE styles-module-ellipsis-LKWy3 "
                                        "styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq "
                                        "stylesMarningNormal-module-header-l-qvNIS").text
        p1 = floor.split(",", [3])
        p2 = p1.split("&nbsp;")
        p3 = p2.split("/")
        return p3[0]



    def select_data_download(self):
        data_download = soup.find("p", class_ ="styles-module-root-_KFFt styles-module-size_s-awPvv "
                                               "styles-module-size_s-_P6ZA stylesMarningNormal-module-root-OSCNq "
                                               "stylesMarningNormal-module-paragraph-s-_c6vD "
                                               "styles-module-noAccent-nZxz7").text
        new_date = datetime.date.fromisoformat(data_download)
        return new_date

    def select_info_about_location(self, html_page) -> Location:
        soup = BeautifulSoup(html_page, "lxml")
        street = self.select_values(self.select_street(soup))
        house = self.select_values(self.select_house(soup))
        region = self.select_values(self.select_region(soup))
        return Location(street, house, region)

    def select_street(self,soup) -> str:
        tag_street = soup.find(class_ ="styles-module-root-_KFFt styles-module-size_s-awPvv "
                                       "styles-module-size_s-_P6ZA stylesMarningNormal-module-root-OSCNq "
                                       "stylesMarningNormal-module-paragraph-s-_c6vD").find("span").text
        c = (tag_street.split(",")[0])
        return c

    def select_house(self, soup) -> str:

        tag_house = soup.find(class_ ="styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA "
                                      "stylesMarningNormal-module-root-OSCNq "
                                      "stylesMarningNormal-module-paragraph-s-_c6vD").find("span").text
        c = (tag_house.split(",")[1])
        return c

    def select_region(self, soup) -> str:
        tag_region = soup.find(class_ ="styles-module-root-_KFFt styles-module-size_s-awPvv "
                                       "styles-module-size_s-_P6ZA styles-module-ellipsis-LKWy3 "
                                       "styles-module-ellipsis_oneLine-NY089 stylesMarningNormal-module-root-OSCNq "
                                       "stylesMarningNormal-module-paragraph-s-_c6vD styles-module-root_top-HYzCt "
                                       "styles-module-margin-top_0-_usAN").find("span").text
        c = tag_region
        return c

    def select_values(self, soup: BeautifulSoup, tag: str, value_class: str) -> str or None:
        res = soup.find(tag, class_=value_class)
        if res is not None:
            return res.text
        return None

