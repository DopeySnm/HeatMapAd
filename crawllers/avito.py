from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import traceback
from selenium.webdriver.common.by import By
from parsers.avito import ParserAvito
from crawllers.base import Crawller


class CrawllerAvito(Crawller):
    def __init__(self):
        self.useragent = UserAgent()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless=new')
        self.service = Service(r"/chromedriver/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.parser = ParserAvito()
        self.url = "https://www.avito.ru/chelyabinsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&f=ASgBAQICAUSSA8YQAUDKCMT~WIZZilmarAGYrAGWrAGUrAGIWYBZglmEWfzPMg&p=1"

    def scroll_page(self):
        SCROLL_PAUSE_TIME = 0.5
        self.waiting_for_element(15, By.CLASS_NAME, "iva-item-title-py3i_")

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def next_page(self):
        url_p = self.url.split("&")
        now_p = url_p[2][2::]
        url_p[2] = "p=" + str(int(now_p) + 1)
        self.url = "&".join(url_p)

    def start(self):
        try:
            lst_ads = []
            while True:
                self.add_useragent()
                self.driver.get(self.url)
                self.scroll_page()
                time.sleep(4)

                boxes = self.get_boxes_ads()
                for box in boxes:
                    ad = self.parser.select_ad(box.get_attribute("outerHTML"))
                    lst_ads.append(ad)
                #     break
                # break
                self.next_page()
        except Exception:
            print(traceback.format_exc())
        finally:
            print("Работа Краулера Авито окончена")
            self.exit()
            return lst_ads

    def get_boxes_ads(self):
        boxes = self.driver.find_elements("css selector", ".iva-item-root-_lk9K.photo-slider-slider-S15A_.iva-item-list-rfgcH.iva-item-redesign-rop6P.iva-item-responsive-_lbhG.items-item-My3ih.items-listItem-Gd1jN.js-catalog-item-enum")
        return boxes


if __name__ == "__main__":
    ctrl = CrawllerAvito()
    ctrl.start()