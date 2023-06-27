from city import City

class Ad:
    def __init__(self,
                 x: float,
                 y: float,
                 city: City,
                 data: str,
                 magnitude: float):
        self.city = city
        self.x = x
        self.y = y
        self.data = data
        self.magnitude = magnitude