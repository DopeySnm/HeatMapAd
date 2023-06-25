from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import traceback
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Parser:
    def get_links_ads(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        result_lst_links = []
        for name in soup.find_all('div', class_="iva-item-title-py3i_"):
            link_ad = name.find('a', class_="styles-module-root-QmppR styles-module-root_noVisited-aFA10")['href']
            result_lst_links.append("www.avito.ru" + link_ad)
        return "\n".join(result_lst_links)

class Crawller:
    def __init__(self):
        self.useragent = UserAgent()
        self.options = webdriver.ChromeOptions()
        self.service = Service(r"/chromedriver/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.parser = Parser()
        self.url = "https://www.avito.ru/chelyabinsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&f=ASgBAQICAUSSA8YQAUDKCMT~WIZZilmarAGYrAGWrAGUrAGIWYBZglmEWfzPMg&p=1"

    def get_actor(self, link: str):
        self.url = link
        data = self.driver.page_source
        #put parser method here -->  return parsermethod(data)

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

    def write_txt(self, text):
        with open("avito.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def start(self):
        try:
            while True:
                self.driver.get(self.url)

                self.scroll_page()

                links_ads = self.parser.get_links_ads(self.driver.page_source)
                # print(link_ad)
                self.write_txt(links_ads)
                # print("-" * 40)
                self.next_page()

                # print("*"*40)
                # break
        except Exception:
            print(traceback.format_exc())
        finally:
            print("Работа Краулера Авито окончена")
            return self.driver.page_source

    def __del__(self):
        self.driver.close()
        self.driver.quit()

ctrl = Crawller()
html = ctrl.start()

# url = "https://chelyabinsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=5048&room1=1&room2=1"
#
# options = webdriver.ChromeOptions()
# service = Service(r"/Chromedriver/chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=options)
# for i in range(50):
#     url_p = url.split("&")
#     now_p = url_p[3][2::]
#     url_p[3] = "p=" + str(int(now_p) + 1)
#     url = "&".join(url_p)
# driver.get(url)