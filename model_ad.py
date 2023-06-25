class Ad:
    def __init__(self,
                 title: str,
                 price: float,
                 discription: str,
                 type: str,
                 area: float,
                 link: str,
                 city: str,
                 address: str):
        self.title = title
        self.price = price
        self.discription = discription
        self.type = type
        self.area = area
        self.link = link
        self.city = city
        self.address = address

    def __str__(self):
        return f"Заголовок: {self.title}\nЦена: {self.price}\nОписание: {self.discription}\nТип жилья: {self.type}\nПлощадь: {self.area}\nСсылка на объявление: {self.link}\nГород: {self.city}\nАдрес: {self.address}"