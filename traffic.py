import requests
import time
import re
import traceback
import sys
import csv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

from random import randint
from lxml import etree
from lxml.cssselect import CSSSelector

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(executable_path = '/Applications/chromedriver', chrome_options=options)


#browser.get('https://www.tomtom.com/en_gb/traffic-index/')
browser.get('https://www.tomtom.com/en_gb/traffic-index/ranking/?country=AT,BE,BG,CZ,DK,EE,FI,FR,DE,GR,HU,IS,IE,IT,LV,LT,LU,NL,NO,PL,PT,RO,RU,SK,SI,ES,SE,CH,TR,UA,UK')
time.sleep(0.6)
city_names =browser.find_elements_by_xpath(".//td[@class='RankingTable__td RankingTable__td--city']/span[@class='RankingTable__city-name']")
 
cities = []
for i in range(len(city_names)):
    city = city_names[i].get_attribute("innerText")
    cities.append(city)

ofn = "scraping_tomtom.csv"
outFile = open(ofn, 'w', encoding='utf8')
outFile.write("city;congestion/2019;relative/2019;congestion;date\n")
outFile = open(ofn, 'a', encoding='utf8')

scraping_date= datetime.now()
d1 = scraping_date.strftime("%d/%m/%Y %H:%M")
search = browser.find_element_by_xpath(".//div[@class='NavbarSearch__modal-top']/input")
for j in range(len(city_names)):
    
    search.send_keys(cities[j])
    search.send_keys(Keys.ENTER)
    time.sleep(1.9)
    try:
        congestion_2019=browser.find_element_by_xpath(".//div[@class='CityLiveTraffic__delta']/div[@class='Delta Delta--green Delta--fixed-color']/span[@class='Delta__value']").get_attribute("innerText")
        congestion_now=browser.find_element_by_xpath(".//div[@class='live-number']").get_attribute("innerText")
        outRow = "%s;%s;less than 2019;%s;%s\n" % (cities[j], congestion_2019,  congestion_now, d1)
        outFile.write(outRow)
    except:
        congestion_2019=browser.find_element_by_xpath(".//div[@class='CityLiveTraffic__delta']/div[@class='Delta Delta--red Delta--fixed-color']/span[@class='Delta__value']").get_attribute("innerText")
        congestion_now=browser.find_element_by_xpath(".//div[@class='live-number']").get_attribute("innerText")
        outRow = "%s;%s;more than 2019;%s;%s\n" % (cities[j], congestion_2019,  congestion_now, d1)
        outFile.write(outRow)
    search = browser.find_element_by_xpath(".//div[@class='NavbarSearch__modal-top']/input")

browser.quit()
