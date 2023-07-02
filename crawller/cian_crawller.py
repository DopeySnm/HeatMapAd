from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import traceback
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Notice:
    title: str
    price: float
    description: str
    type: str
    area: float
    link: str
class Parser:
    def get_links_ads(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        result_lst_links = []
        for name in soup.find_all('div', class_="_93444fe79c--content--lXy9G"):
            link_ad = name.find('a', class_="_93444fe79c--link--eoxce")['href']
            result_lst_links.append(link_ad)
        return "\n".join(result_lst_links)


class Crawller:
    def __init__(self):
        self.useragent = UserAgent()
        self.options = webdriver.ChromeOptions()
        #self.options.add_argument("--headless=new")
        self.service = Service(r"/chromedriver/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.parser = Parser()
        self.url = "https://chelyabinsk.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=5048&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1"

    def get_notice(self, link: str) -> Notice:
        self.driver.get(link)
        data = self.driver.page_source
        soup = BeautifulSoup(data, "lxml")
        n = Notice()
        maindata = []
        #looking for type and area
        for div in soup.findAll('div', {'class': 'a10a3f92e9--item--qJhdR'}):
            d = div.find('p', class_='a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_22px--bnKK9 a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__normal--xbqP6').text
            maindata.append(d)
        #looking for description
        for div in soup.find_all('div', {'class': 'a10a3f92e9--content--TjQir'}):
            d = div.find('span', class_='a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_6u--A1GMI a10a3f92e9--fontWeight_normal--P9Ylg a10a3f92e9--fontSize_16px--RB9YW a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG a10a3f92e9--text_letterSpacing__0--mdnqq a10a3f92e9--text_whiteSpace__pre-wrap--scZwb')
            n.description = d.text
        #looking for price

        for div in soup.find_all('div', {'class': 'a10a3f92e9--amount--ON6i1'}):
            d = div.find('span', class_='a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_9u--qr919 a10a3f92e9--fontWeight_bold--ePDnv a10a3f92e9--fontSize_28px--xlUV0 a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG')
            n.price = int(d.text[:-1].replace('\xa0', ''))
        #if notice page contains title class
        if (data.__contains__('a10a3f92e9--title--FUlZg')):
            for div in soup.find_all('div', {'class': 'a10a3f92e9--title--FUlZg'}):
                d = div.find('h2',
                             class_='a10a3f92e9--color_black_100--kPHhJ a10a3f92e9--lineHeight_9u--qr919 a10a3f92e9--fontWeight_bold--ePDnv a10a3f92e9--fontSize_28px--xlUV0 a10a3f92e9--display_block--pDAEx a10a3f92e9--text--g9xAG')
                n.title = d.text
        else:
            for div in soup.find_all('div', {'class': 'a10a3f92e9--container--pWxZo'}):
                d = div.find('h1', class_='a10a3f92e9--title--vlZwT')
                n.title = d.text
        n.type = maindata[0]
        n.area = float(maindata[1].split()[0].replace(',', '.'))
        n.link = link
        return n

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

    def write_txt(self, text):
        with open("cian.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def start(self):
        try:
            while True:
                self.driver.get(self.url)

                self.scroll_page()
                links_ads = self.parser.get_links_ads(self.driver.page_source)
                for link in links_ads.split('\n'):
                    self.get_notice(link)
                self.next_page()

                # print("*"*40)
                # break
        except Exception:
            print(traceback.format_exc())
        finally:
            print("Работа Краулера Циан окончена")
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