from bs4 import BeautifulSoup

from main import soup
from model.ad import Ad
from parser_i import Interface


class Parser_cyan(Interface):
    def select_info_discription(self, html_page) -> Ds:
        return Ds()



    def select_info_about_apartment(self, html_page) -> Ad:
        return Ad()
    @property
    def select_title(self):
        title = soup.find("h1", class_="a10a3f92e9--title--vlZwT")
        return title

    @property
    def select_price(self):
        price = soup.find("span", class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_9u--qr919 a10a3f92e9--fontWeight_bold--ePDnv a10a3f92e9--fontSize_28px--xlUV0 a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG")
        return price

    @property
    def select_discription(self):
        discription = soup.find("span",class_="a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_6u--A1GMI a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__0--mdnqq a10a3f92e9--text_whiteSpace__pre-wrap--scZwb")
        return discription

    @property
    def select_link(self):
        link= soup.find("meta", property = "og:url")
        return link

    def select_values_under_main_name(self, soup: BeautifulSoup, tag: str, value_class: str) -> str or None:
        res = soup.find(tag, class_=value_class)
        if res is not None:
            return res.text
        return None
