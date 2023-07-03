from db.db_helper import DBHelper


class DownloadController:
    def __init__(self):
        self.list_ads = []
        self.list_infrastructures = []

    def save(self):
        for ad in self.list_ads:
            DBHelper().insert(ad)

        for infrastructure in self.list_infrastructures:
            DBHelper().insert(infrastructure)
