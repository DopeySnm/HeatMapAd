import dateutil.utils
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.base import Base
from model.location import Location
from model.description import Description
from model.ad import Ad
from model.infrastructure import Infrastructure

# class DBLocation:
#     def __init__(self):
#         self.engine = DBHelper().engine
#
#     def insert(self, location: Location):
#         with Session(autoflush=False, bind=self.engine) as db:
#             db.add(location)
#             db.commit()
#
#     def get_location_by_id(self, id: int):
#         with Session(autoflush=False, bind=self.engine) as db:
#             result = db.query(Location).filter(Location.id == id).first()
#             return result
#
#     def update(self, old_location: Location, new_location: Location):
#         with Session(autoflush=False, bind=self.engine) as db:
#             get_old_location = db.query(Location).filter(Location.id == old_location.id).first()
#             if (get_old_location != None):
#                 get_old_location.coordinate_x = new_location.coordinate_x
#                 get_old_location.coordinate_y = new_location.coordinate_y
#                 get_old_location.city = new_location.city
#                 get_old_location.district = new_location.district
#                 get_old_location.street = new_location.street
#                 get_old_location.house = new_location.house
#                 get_old_location.flat = new_location.flat
#                 db.commit()

class DBAd:
    def __init__(self):
        self.engine = DBHelper().engine

    def insert(self, ad: Ad):
        with Session(autoflush=False, bind=self.engine) as db:
            db.add(ad)
            db.commit()

    def get_ads_by_city(self, city: str):
        with Session(autoflush=False, bind=self.engine) as db:
            result_ads = db.query(Ad).join(Location).filter(Location.city == city)
            db.close()
        return result_ads

    def get_ad_by_id(self, id: int):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(Ad).filter(Ad.id == id).first()
            return result

    def update(self, old_ad: Ad, new_ad: Ad):
        with Session(autoflush=False, bind=self.engine) as db:
            get_old_ad = db.query(Ad).filter(Ad.location_id == old_ad.id).first()
            if (get_old_ad != None):
                get_old_ad.price = new_ad.price
                get_old_ad.location = new_ad.location
                get_old_ad.description = new_ad.description
                get_old_ad.link = new_ad.link
                get_old_ad.title = new_ad.title
                get_old_ad.data_download = new_ad.data_download
                get_old_ad.magnitude = new_ad.magnitude
                db.commit()

# class DBDescription:
#     def __init__(self):
#         self.engine = DBHelper().engine
#
#     def insert(self, description: Description):
#         with Session(autoflush=False, bind=self.engine) as db:
#             db.add(description)
#             db.commit()
#
#     def get_by_id(self, id: int):
#         with Session(autoflush=False, bind=self.engine) as db:
#             result = db.query(Description).filter(Description.id == id).first()
#             return result
#
#     def update(self, old_description: Description, new_description: Description):
#         with Session(autoflush=False, bind=self.engine) as db:
#             get_old_description = db.query(Description).filter(Description.id == old_description.id).first()
#             if (get_old_description != None):
#                 get_old_description.main_description = new_description.main_description
#                 get_old_description.total_area = new_description.total_area
#                 get_old_description.floor = new_description.floor
#                 get_old_description.year_built = new_description.year_built
#                 get_old_description.living_area = new_description.living_area
#                 get_old_description.housing_type = new_description.housing_type
#                 get_old_description.bathroom = new_description.bathroom
#                 get_old_description.repair = new_description.repair
#                 db.commit()

class DBInfrastructure:
    def __init__(self):
        self.engine = DBHelper().engine

    def insert(self, infrastructure: Infrastructure):
        with Session(autoflush=False, bind=self.engine) as db:
            db.add(infrastructure)
            db.commit()

    def get_infrastructure_by_id(self, id: int):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(Infrastructure).filter(Infrastructure.id == id).first()
            return result

    def update(self, old_infrastructure: Infrastructure, new_infrastructure: Infrastructure):
        with Session(autoflush=False, bind=self.engine) as db:
            get_old_infrastructure = db.query(Infrastructure).filter(Infrastructure.id == old_infrastructure.id).first()
            if (get_old_infrastructure != None):
                get_old_infrastructure.title = new_infrastructure.title
                get_old_infrastructure.type = new_infrastructure.type
                get_old_infrastructure.location = new_infrastructure.location
                get_old_infrastructure.data_download = new_infrastructure.data_download
                db.commit()

class DBHelper:
    def __init__(self):
        sqlite_database = "sqlite:///ads.db"
        self.engine = create_engine(sqlite_database)#, echo=True)

    def create_db(self):
        Base.metadata.create_all(bind=self.engine)

def test():
    # DBHelper().create_db()

    location = Location(coordinate_x=54, coordinate_y=54, city="Челябинск", district="ЧТЗ", street="Улица", house="1",
                        flat="1")

    description = Description(main_description="описание", total_area=10, floor=2000, year_built=2000, living_area="хз",
                              housing_type="да", bathroom="нет", repair="хз")

    ad = Ad(price=50000, link="Ссылка", title="Квартира 2", magnitude=0.5, data_download=dateutil.utils.today(),
            location=location, description=description)

    DBAd().insert(ad)



result = DBAd().get_ads_by_city("Челябинск")

for i in result:
    print(i.title + i.location.city)