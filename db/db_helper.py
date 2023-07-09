import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.base import Base
from models.description import Description
from models.location import Location
from models.ad import Ad
from models.infrastructure import Infrastructure

class DBHelper:
    def __init__(self):
        sqlite_database = f"sqlite:///../db/ads.db"
        self.engine = create_engine(sqlite_database,)#, echo=True)

    def create_db(self):
        Base.metadata.create_all(bind=self.engine)

    # 55.154, 61.4291, "Челябинск"

    def insert_city(self, coordinate_x: float, coordinate_y: float, city: str):
        location = Location(coordinate_x=coordinate_x, coordinate_y=coordinate_y, city=city, street="center", full_address=city+" center")
        with Session(autoflush=False, bind=self.engine) as db:
            db.add(location)
            db.commit()

    def get_list_city(self):
        with Session(autoflush=False, bind=self.engine) as db:
            result_ads = db.query(Location).filter(Location.street == "center")
            db.close()
        return result_ads

    def get_city_center(self, city: str):
        with Session(autoflush=False, bind=self.engine) as db:
            result_ads = db.query(Location).filter(Location.street == "center" and Location.city == city).first()
            db.close()
        return result_ads

    def insert(self, ad: Ad = None, infrastructure: Infrastructure = None):
        if ad != None and infrastructure != None:
            with Session(autoflush=False, bind=self.engine) as db:
                db.add(ad)
                db.add(infrastructure)
                db.commit()
        elif not ad == None:
            with Session(autoflush=False, bind=self.engine) as db:
                db.add(ad)
                db.commit()
        elif not infrastructure == None:
            with Session(autoflush=False, bind=self.engine) as db:
                db.add(infrastructure)
                db.commit()
        else:
            pass

    def get_ads_by_city(self, city: str):
        with Session(autoflush=False, bind=self.engine) as db:
            result_ads = db.query(Ad).join(Location).filter(Location.city == city)
            db.close()
        return result_ads

    def get_description_values(self):
        with Session(autoflush=False, bind=self.engine) as db:
            res = {"housing_type": list(set([i[0] for i in db.query(Description.housing_type).group_by(Description.housing_type).all()])),
                    "repair": list(set([i[0] for i in db.query(Description.repair).group_by(Description.housing_type).all()]))}
            db.close()
        return res

    def get_ad_by_id(self, id: int):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(Ad).filter(Ad.id == id).first()
            return result

    def get_infrastructure_by_city(self, city: str):
        with Session(autoflush=False, bind=self.engine) as db:
            result_infrastructure = db.query(Infrastructure).join(Location).filter(Location.city == city)
            db.close()
        return result_infrastructure

    def get_infrastructure_by_id(self, id: int):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(Infrastructure).filter(Infrastructure.id == id).first()
            return result

    # def update_infrastructure(self, old_infrastructure: Infrastructure, new_infrastructure: Infrastructure):
    #     with Session(autoflush=False, bind=self.engine) as db:
    #         get_old_infrastructure = db.query(Infrastructure).filter(Infrastructure.id == old_infrastructure.id).first()
    #         if (get_old_infrastructure != None):
    #             get_old_infrastructure.title = new_infrastructure.title
    #             get_old_infrastructure.type = new_infrastructure.type
    #             get_old_infrastructure.location = new_infrastructure.location
    #             get_old_infrastructure.data_download = new_infrastructure.data_download
    #             db.commit()
    #
    # def update_ad(self, old_ad: Ad, new_ad: Ad):
    #     with Session(autoflush=False, bind=self.engine) as db:
    #         get_old_ad = db.query(Ad).filter(Ad.location_id == old_ad.id).first()
    #         if (get_old_ad != None):
    #             get_old_ad.price = new_ad.price
    #             get_old_ad.location = new_ad.location
    #             get_old_ad.description = new_ad.description
    #             get_old_ad.link = new_ad.link
    #             get_old_ad.title = new_ad.title
    #             get_old_ad.data_download = new_ad.data_download
    #             get_old_ad.magnitude = new_ad.magnitude
    #             db.commit()


# DBHelper().insert_city(55.154, 61.4291, "Челябинск")


# def ad_test_data():
#     location = Location(coordinate_x=51, coordinate_y=52, city="Челябинск", district="ЧТЗ", street="Улица", house="1", flat="1")
#
#     infrastructure = Infrastructure(type="Садик", title="Садик №2", location=location, data_download=datetime.date.today())
#
#     location = Location(coordinate_x=54, coordinate_y=54, city="Челябинск", district="ЧТЗ", street="Улица", house="1",
#                         flat="1")
#
#     description = Description(main_description="описание", total_area=10, floor=2000, year_built=2000, living_area="хз",
#                               housing_type="да", bathroom="нет", repair="хз")
#
#     ad = Ad(price=50000, link="Ссылка", title="Квартира 2", magnitude=0.5, data_download=datetime.date.today(),
#             location=location, description=description)
#
#     DBHelper().insert(ad, infrastructure)
#
# if __name__ == "__main__":
#     print(DBHelper().get_description_values())