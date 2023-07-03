from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.base import Base
from model.users.favourites import Favourites
from model.users.history import History
from model.users.tokens import Tokens
from model.users.user import User


class DBHelperUsers:
    def __init__(self):
        sqlite_database = "sqlite:///users.db"
        self.engine = create_engine(sqlite_database)#, echo=True)

    def create_db(self):
        Base.metadata.create_all(bind=self.engine)

class DBUsers:
    def __init__(self):
        self.engine = DBHelperUsers().engine

    def insert(self, user: User):
        with Session(autoflush=False, bind=self.engine) as db:
            db.add(user)
            db.commit()

    def get_user_by_name(self, name: str):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(User).filter(User.user_name == name).first()
            return result

    # def update(self, old_ad: Ad, new_ad: Ad):
    #     with Session(autoflush=False, bind=self.engine) as db:
    #         get_old_ad = db.query(Ad).filter(Ad.id == old_ad.id).first()
    #         if (get_old_ad != None):
    #             get_old_ad.price = new_ad.price
    #             get_old_ad.location = new_ad.location
    #             get_old_ad.description = new_ad.description
    #             get_old_ad.link = new_ad.link
    #             get_old_ad.title = new_ad.title
    #             get_old_ad.data_download = new_ad.data_download
    #             get_old_ad.magnitude = new_ad.magnitude
    #             db.commit()


DBHelperUsers().create_db()