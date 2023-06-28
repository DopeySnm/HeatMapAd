class Location:
    def __init__(self,
                coordinate_x: float,
                coordinate_y: float,
                city: str,
                street: str = None,
                house: str = None,
                number_flat: str = None):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.city = city
        self.street = street
        self.house = house
        self.number_flat = number_flat
