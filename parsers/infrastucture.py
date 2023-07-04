from datetime import datetime
from bs4 import BeautifulSoup
from models.location import Location
from parsers.base import Parser
from models.infrastructure import Infrastructure


class ParserInfrastucture(Parser):
    def select_infrastucture(self, html_code):
        soup = BeautifulSoup(html_code, "lxml")
        type = self.select_type(soup)
        title = self.select_title(soup)
        location = self.select_location(soup)
        date_download = datetime.now().date()
        return Infrastructure(type=type, title=title, location=location, date_download=date_download)

    def select_title(self, soup):
        title = soup.find("div", class_="similar-item__title").text
        title = title.split(".")
        title = title[1::]
        title = ".".join(title)

        return title

    def select_type(self, soup):
        type = soup.find("div", class_="similar-item__description")
        return self.check_value(type)

    def select_location(self, soup):
        full_address = soup.find("div", class_="similar-item__adrss-item").text

        city = "Челябинск"
        street = full_address.split(",")[0]
        house = full_address.split(",")[1]

        coordinates = self.get_coordinates(city+full_address)
        coordinate_x = coordinates[0]
        coordinate_y = coordinates[1]
        return Location(coordinate_x=coordinate_x, coordinate_y=coordinate_y, full_address=full_address, city=city, street=street, house=house)