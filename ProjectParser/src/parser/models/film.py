import re


class Film:
    def __init__(self, name_film: str, country: str or None, budget: str or None, duration: str, site_id: int, time_download: str):
        self.name_film = str(name_film)
        self.country = str(country)
        self.budget = self.convert_budget(budget)
        self.duration = self.convert_to_minutes(duration)
        self.site_id = site_id
        self.time_download = time_download

    def convert_budget(self, budget: str) -> int:
        """
        Функция конвертирует строку типа $63 000 000 в число 63000000
        :param budget:
        :return: int: число в долларах
        """
        if budget is not None:
            if "$" in budget:
                return self.convert_dollar(budget)
            elif "₽" in budget:
                return self.convert_ruble(budget)
            else:
                return int(re.sub(r'\D', '', budget))
        else:
            return None

    def convert_dollar(self, budget):
        number = int(re.sub(r'\D', '', budget))
        return number

    def convert_ruble(self, budget):
        number = int(re.sub(r'\D', '', budget))
        return round(number * 0.7)

    def convert_to_minutes(self, duration: str) -> int:
        """Поступает строка типа 2 ч 32 мин и возвращает число - количество минут"""
        lst_numbers = re.findall(r"\d+", duration)
        if len(lst_numbers) == 2:
            minutes = (int(lst_numbers[0]) * 60) + (int(lst_numbers[1]))
        elif len(lst_numbers) == 1:
            return int(lst_numbers[0])
        return int(minutes)

    def return_info(self) -> list:
        """
        Функция возвращает список с упорядоченной информацией: Название фильма, Страна, Бюджет, Длительность
        :return: list of information
        """
        return [self.name_film, self.country, self.budget, int(self.duration), self.site_id, self.time_download]

    def __str__(self):
        return f"Название фильма: {self.name_film}\nСтрана фильма: {self.country}\nБюджет фильма: {self.budget}\nДлительноть фильма: {self.duration}\nДата загрузки:{self.time_download}"