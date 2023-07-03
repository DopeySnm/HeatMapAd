from dataclasses import replace
from shlex import join

from bs4 import BeautifulSoup

from main import soup
from model.ad import Ad
from model.description import Description
from model.location import Location
from parser_i import Interface


def select_values_under():
    pass


class Parser_cyan(Interface):
    def select_info_discription(self, html_page) -> Description:
        main_description = self.select_values_under(self.select_description_main())
        total_area = self.select_values(self.select_total_area())
        floor = self.select_values(self.select_floor)
        year_built = self.select_values(self.select_year_built)
        living_area = self.select_values(self.select_living_area)
        housing_type = None
        bathroom = self.select_values(self.delect_bathroom)
        repair = self.select_values(self.select_repair)
        return Description(main_description, total_area, floor, year_built, living_area, housing_type, bathroom, repair)

    def select_info_about_apartment(self, html_page) -> Ad:
        title = self.select_values(self.select_title())
        price = self.select_values(self.select_price())
        link = self.select_values(self.select_link())
        location = self.select_values(self.select_info_about_location())
        magnitude = self.select_values(self.select_magnitude())
        data_download = self.select_values(self.select_data_download())
        description = self.select_values(self.select_discription_main())
        return Ad(title, price, link, location, magnitude, data_download, description)

    def select_info_about_location(self, html_page) -> Location:
        soup = BeautifulSoup(html_page, "lxml")
        l = soup.findAll("a", class_="a10a3f92e9--address--SMU25")
        district = l[2]
        street = l[3]
        house = l[4]
        return Location(street, house, district)


    @property
    def select_title(self):
        title = soup.find("h1", class_="a10a3f92e9--title--vlZwT")
        return title

    @property
    def select_price(self):
        price = soup.find("span", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_9u--qr919 "
                                         "a10a3f92e9--fontWeight_bold--ePDnv a10a3f92e9--fontSize_28px--xlUV0 "
                                         "a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG").text
        str = join(price)
        p = str.replace("&nbsp;")
        a = p.find('₽')
        return a

    @property
    def select_description_main(self):
        description = soup.find("span", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_6u--A1GMI "
                                               "a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW "
                                               "a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG "
                                               "a10a3f92e9--text_letterSpacing__0--mdnqq "
                                               "a10a3f92e9--text_whiteSpace__pre-wrap--scZwb").text
        return description

    @property
    def select_link(self):
        link = soup.find("meta", property="og:url")
        return link

    def select_total_area(self):
        total_area = soup.find_all("p", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_22px--bnKK9 "
                                               "a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW "
                                               "a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG "
                                               "a10a3f92e9--text_letterSpacing__normal--xbqP6")
        return total_area[0]

    def select_living_area(self):
        living_area = soup.find("p", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_22px--bnKK9 "
                                            "a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW "
                                            "a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG "
                                            "a10a3f92e9--text_letterSpacing__normal--xbqP6")
        return living_area[1]

    def select_year_built(self):
        year_built = soup.find_all("p", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_22px--bnKK9 "
                                               "a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW "
                                               "a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG "
                                               "a10a3f92e9--text_letterSpacing__normal--xbqP6")
        return year_built[0]

    def select_floor(self):
        floor = soup.find_all("span", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_6u--A1GMI "
                                             "a10a3f92e9--fontWeight_bold--ePDnv a10a3f92e9--fontSize_16px--RB9YW "
                                             "a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG")
        return floor[3]

    def delect_bathroom(self):
        bathroom = soup.find_all("p", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_22px--bnKK9 "
                                             "a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW "
                                             "a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG "
                                             "a10a3f92e9--text_letterSpacing__normal--xbqP6")
        return bathroom[5]

    def select_repair(self):
        repair = soup.find_all("p", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_22px--bnKK9 "
                                             "a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW "
                                             "a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG "
                                             "a10a3f92e9--text_letterSpacing__normal--xbqP6")
        return repair[8]


    def select_values(self, soup: BeautifulSoup, tag: str, value_class: str) -> str or None:
        res = soup.find(tag, class_=value_class)
        if res is not None:
            return res.text
        return None
