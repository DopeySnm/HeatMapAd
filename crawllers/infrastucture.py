from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import traceback
from selenium.webdriver.common.by import By
from parsers.infrastucture import ParserInfrastucture
from crawllers.base import Crawller


class CrawllerInfrastructure(Crawller):
    def __init__(self):
        self.useragent = UserAgent()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless=new')
        self.service = Service(r"/chromedriver/chromedriver.exe")
        self.parser = ParserInfrastucture()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.url = "https://www.orgpage.ru/chelyabinsk/obrazovatelnye-uchrezhdeniya-i/"
        self.base_url = 'https://www.orgpage.ru/chelyabinsk/obrazovatelnye-uchrezhdeniya-i/'

    def scroll_page(self):
        SCROLL_PAUSE_TIME = 0.5
        self.waiting_for_element(15, By.CLASS_NAME, "catalog-header__title")

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def next_page(self):
        result = self.url.split('/')
        if (self.url == self.base_url):
            self.url = self.url + '2/'
        else:
            self.url = self.base_url + str(int(self.url.split('/')[-2]) + 1) + '/'

    def start(self):
        try:
            lst_orgs = []
            count = 0
            while True:
                self.add_useragent()
                self.driver.get(self.url)
                result = self.driver.page_source
                if 'Ошибка 404' in result:
                    break
                self.scroll_page()

                boxes = self.get_boxes_ads()
                for box in boxes:
                    org_built = self.parser.select_infrastucture(box.get_attribute("outerHTML"))
                    lst_orgs.append(org_built)
                    count += 1
                    if count == 130:
                        break
                if count == 130:
                    break
                self.next_page()
        except Exception:
            print(traceback.format_exc())
        finally:
            print("Работа Краулера Инфраструктуры окончена")
            self.exit()
            return lst_orgs

    def get_boxes_ads(self):
        boxes = self.driver.find_elements("css selector", ".similar-item__wrap")
        return boxes


if __name__ == "__main__":
    ctrl = CrawllerInfrastructure()
    ctrl.start()