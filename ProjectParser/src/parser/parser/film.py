from bs4 import BeautifulSoup
from datetime import datetime
from src.parser.models.film import Film


class ParserFilms:
    def __init__(self):
        pass

    def select_id_top_films(self, html_page):
        """
        Собирает со страници топ-фильмов все id фильмов
        :return: list of ids
        """
        soup = BeautifulSoup(html_page, "lxml")

        elements = soup.find_all("i", class_="movie-title__text filmList__item-title-link-popup link-info-movie-type-film")
        lst_id = [el["data-id"] for el in elements]
        return lst_id

    def select_info_of_film(self, html_page, id_actor) -> Film:
        """
        Достает из нынешне находяйщейся страницы всю информацию о фильме и создает объект Film
        :return: Film object
        """

        soup = BeautifulSoup(html_page, "lxml")

        name = self.select_name(soup)
        box_info = self.select_box_info(soup)
        country = self.select_value_info(box_info, 'a', "film-page__country-link")
        budget = self.select_value_info(box_info, 'span', "box-budget-tooltip")
        duration = self.select_duration(box_info)
        time_download = str(datetime.now().date())

        return Film(name, country, budget, duration, id_actor, time_download)

    def select_name(self, soup: BeautifulSoup) -> str:
        """
        Достает из объекта BeautifulSoup строку со значением наименования фильма
        :param soup: Объект BeautifulSoup
        :return: str
        """
        name = soup.find('h1', class_="film-page__title-text film-page__itemprop")
        return name.text

    def select_box_info(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Возвращает из переданной страницы поле с информацией о фильме
        :param soup: Объект BeautifulSoup
        :return: Объект BeautifulSoup
        """
        return soup.find('div', class_="film-page__infowrap")

    def select_value_info(self, soup: BeautifulSoup, tag_name: str, value: str) -> str or None:
        """
        Достает из объекта BeautifulSoup строку tag_name со значением class_=value, иначе возвращает None
        :param soup: Объект BeautifulSoup
        :return: str
        """
        duration = soup.find(tag_name, class_=value)
        if duration is not None:
            return duration.text
        else:
            return None

    def select_duration(self, soup: BeautifulSoup) -> str:
        """
        Достает из объекта BeautifulSoup строку со значением длительности фильма, иначе возвращает None
        :param soup: Объект BeautifulSoup
        :return: str
        """
        duration = soup.find_all('td', class_="data")[1]
        if duration is not None:
            return duration.text
        else:
            return None