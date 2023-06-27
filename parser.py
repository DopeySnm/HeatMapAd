from bs4 import BeautifulSoup
from model_ad import Ad

class Parser:
    def __init__(self):
        pass
    def select_info_about_apartment(self, html_page) -> Ad:
        soup = BeautifulSoup(html_page, "lxml")
        name = soup.find ("span", class_="title-info-title-text")
        price = soup.find("span", class_="priceCurrency")
        discription = soup.find("div", class_="style-item-description-html-qCwUL")
        type = soup.find("span", itemprop="name")
        #??
        link = soup.find("link", rel="canonical")
        city = self.select_city(soup)
        address = soup.find("span", class_="style-item-address__string-wt61A")
        return Ad(name, price, discription, type, link, city, address)


    def select_city(self, soup) -> str:
        tag_city = soup.find("span", class_="style-item-address__string-wt61A")
        if tag_city:
            city = tag_city.text
            c = (tag_city.split(",")[1])
            return c