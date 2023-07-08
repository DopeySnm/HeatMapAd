from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.base import Base
from models.users.favourites import Favourites
from models.users.history import History
from models.users.tokens import Tokens
from models.users.user import User

class DBHelperUsers:
    def __init__(self):
        sqlite_database = "sqlite:///../db/db_users/users.db"
        self.engine = create_engine(sqlite_database)#, echo=True)

    def create_db(self):
        Base.metadata.create_all(bind=self.engine)

    def insert_history(self, history: History):
        with Session(autoflush=False, bind=self.engine) as db:
            db.add(history)
            db.commit()

    def insert_favourites(self, favourites: Favourites):
        with Session(autoflush=False, bind=self.engine) as db:
            db.add(favourites)
            db.commit()

    def insert_tokens(self, tokens: Tokens):
        with Session(autoflush=False, bind=self.engine) as db:
            db.add(tokens)
            db.commit()

    def insert_user(self, user: User):
        with Session(autoflush=False, bind=self.engine) as db:
            db.add(user)
            db.commit()

    def get_list_user(self):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(User).all()
            return result

    def get_list_history_by_user_id(self, user_id: int):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(History).filter(History.user_id == user_id)
            return result

    def get_list_favourites_by_user_id(self, user_id: int):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(Favourites).filter(Favourites.user_id == user_id)
            return result

    def get_tokens_by_user_id(self, user_id: int):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(Tokens).filter(Tokens.user_id == user_id).first()
            return result

    def get_user_by_id_telegram(self, id_telegram: int):
        with Session(autoflush=False, bind=self.engine) as db:
            result = db.query(User).filter(User.id_telegram == id_telegram).first()
            return result

    def add_tokens_user_by_id_telegram(self, count_tokens: int, id_telegram: int):
        with Session(autoflush=False, bind=self.engine) as db:
            get_old_tokens = db.query(Tokens).join(User).filter(User.id_telegram == id_telegram).first()
            if (get_old_tokens != None):
                get_old_tokens.count_tokens += count_tokens
                db.commit()
