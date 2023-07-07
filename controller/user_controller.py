from db.db_users.db_users_helper import DBHelperUsers
from model.users.favourites import Favourites
from model.users.history import History
from model.users.tokens import Tokens
from model.users.user import User

class UserController:
    def check_admin(self, id_telegram: int):
        return self.get_user_by_telegram_id(id_telegram).is_admin

    def update_tokens_user_by_id_telegram(self, count_tokens: int, id_telegram: int):
        DBHelperUsers().update_tokens_user_by_id_telegram(count_tokens=count_tokens, id_telegram=id_telegram)

    def get_list_user(self):
        pass

    def get_user_by_telegram_id(self, id_telegram: int) -> User:
        user: User = DBHelperUsers().get_user_by_id_telegram(id_telegram=id_telegram)
        user.count_token = DBHelperUsers().get_tokens_by_user_id(user_id=user.id).count_tokens
        user.list_favourites = DBHelperUsers().get_list_favourites_by_user_id(user_id=user.id)
        user.list_history = DBHelperUsers().get_list_history_by_user_id(user_id=user.id)
        return user

    def add_ad_in_history_user_by_id_telegram(self, id_telegram: int, lick_ad: str):
        user: User = DBHelperUsers().get_user_by_id_telegram(id_telegram=id_telegram)
        DBHelperUsers().insert_history(History(link_ad=lick_ad, user=user))

    def add_ad_in_favourites_user_by_id_telegram(self, id_telegram: int, lick_ad: str):
        user: User = DBHelperUsers().get_user_by_id_telegram(id_telegram=id_telegram)
        DBHelperUsers().insert_favourites(Favourites(link_ad=lick_ad, user=user))

    def save_new_user(self, user_name: str, is_admin: bool, id_telegram: int, count_tokens: int):
        user = User(user_name=user_name, is_admin=is_admin, id_telegram=id_telegram)
        DBHelperUsers().insert_tokens(Tokens(count_tokens=count_tokens, user=user))
        pass

    def create_db_users(self):
        DBHelperUsers().create_db()

# UserController().save_new_user(user_name="test1", is_admin=True, id_telegram=2, count_tokens=10)