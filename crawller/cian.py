from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import traceback
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parsers.cian import ParserCian

class CrawllerCian:
    def __init__(self):
        self.useragent = UserAgent()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")
        self.service = Service(r"/chromedriver/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.parser = ParserCian()
        self.url = "https://chelyabinsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=5048&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1"

    def add_useragent(self):
        """
        Добавляет user-agent к драйверу
        :return: None
        """
        self.options.add_argument(f"user-agent={self.useragent.random}")

    def waiting_for_element(self, seconds: int, tag: By, value_tag: str):
        """
        Функция выполняет процесс ожидания элемента по заданным параметрам
        :param seconds: Сколько секунд ожидать
        :param tag: По какому тегу ожидать элемент(By.ID)
        :param value_tag: Значение тега
        :return: None
        """
        element = WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located((tag, value_tag)))

    def scroll_page(self):
        SCROLL_PAUSE_TIME = 0.5
        self.waiting_for_element(5, By.CLASS_NAME, "_93444fe79c--header--BEBpX")

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
        now_p = url_p[3][2::]
        url_p[3] = "p=" + str(int(now_p) + 1)
        self.url = "&".join(url_p)

    def forward_page(self, link):
        """
        Переходит на переданный url
        :param link: str
        :return: None
        """
        self.driver.get(link)
        time.sleep(3)


    def start(self):
        try:
            lst_ads = []
            while True:
                self.add_useragent()
                self.driver.get(self.url)

                self.scroll_page()
                links_ads = self.parser.get_links_ads(self.driver.page_source)
                for link in links_ads.split('\n'):
                    self.forward_page(link)
                    ad = self.parser.select_ad(self.driver.page_source)
                    lst_ads.append(ad)
                    # break
                break
                self.next_page()
        except Exception:
            print(traceback.format_exc())
        finally:
            print("Работа Краулера Циан окончена")
            self.exit()
            return lst_ads

    def exit(self):
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    ctrl = CrawllerCian()
    html = ctrl.start()