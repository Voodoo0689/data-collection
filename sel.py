import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import time
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['data']
mvideo = db.mvideo

chrome_options = Options()
chrome_options.add_argument("--window-size=1248,1248")

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.get('https://www.mvideo.ru/')
elem = driver.find_element_by_xpath("//body")


for i in range(2):
    elem.send_keys(Keys.PAGE_DOWN)
time.sleep(3)
elem = driver.find_element_by_xpath('//div[@data-holder="#loadSubMultiGalleryblock8552369"]/a[@class = "next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right"]')


while 'disable' not in elem.get_attribute('class'):
    time.sleep(3)
    driver.implicitly_wait(10)
    driver.execute_script("arguments[0].click()", elem)

news = driver.find_elements_by_xpath('//div[@class = "gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul/li[@class = "gallery-list-item"]')

for new in news:
    new_dict = {}
    url = new.find_element_by_tag_name('a').get_attribute('href')
    title = new.find_element_by_tag_name('a').get_attribute('data-track-label')
    price = float(json.loads(new.find_element_by_tag_name('a').get_attribute('data-product-info'))['productPriceLocal'])

    new_dict['url'] = url
    new_dict['title'] = title
    new_dict['price'] = price

    mvideo.update_one({'url': url}, {'$set': new_dict})



