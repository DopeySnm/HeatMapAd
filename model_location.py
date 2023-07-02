class Location:
    def __init__(self,
                coordinate_x: float,
                coordinate_y: float,
                street: str = None,
                house: str = None,
                region: str = None):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.street = street
        self.house = house
        self.region = region

    def __str__(self):
        return f"Улица: {self.street}\nДом: {self.house}\nРайон: {self.region}"
