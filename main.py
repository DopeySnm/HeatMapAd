from bs4 import BeautifulSoup as b
import requests
from model_ad import Ad

URL = 'https://www.avito.ru/chelyabinsk/kvartiry/2-k._kvartira_64m_25et._2669178512?guests=2'
r = requests.get(URL)
print(r.status_code)
soup = b(r.text, 'html.parser')
title = soup.find_all('span', "title-info-title-text","item-view/title-info")
y = [a.text for a in title]
print(y)
