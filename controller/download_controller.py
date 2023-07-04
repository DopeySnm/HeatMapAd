from db.db_helper import DBHelper
from crawller.avito import CrawllerAvito
from crawller.cian import CrawllerCian

class DownloadController:
    def __init__(self):
        self.list_ads = []
        self.list_infrastructures = []
        self.crawller_cian = CrawllerCian()
        self.crawller_avito = CrawllerAvito()

        self.create_database()

    def create_database(self):
        DBHelper().create_db()

    def save(self):
        for ad in self.list_ads:
            DBHelper().insert(ad)

        for infrastructure in self.list_infrastructures:
            DBHelper().insert(infrastructure)

    def start_parse(self):
        try:
            # lst_ads_avito = self.crawller_avito.start()
            # self.list_ads += lst_ads_avito

            lst_ads_cian = self.crawller_cian.start()
            self.list_ads += lst_ads_cian
        except Exception as ex:
            print(ex)
        finally:
            self.save()


if __name__ == '__main__':
    ctrl = DownloadController()
    ctrl.start_parse()
