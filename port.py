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


options = webdriver.ChromeOptions()
browser = webdriver.Chrome(executable_path = '/Applications/chromedriver', chrome_options=options)

ofn = "scraping_marine_traffic.csv"
outFile = open(ofn, 'a', encoding='utf8')
outFile.write("Scraping Time; Local Time; Port; Code; Vessels; Departures 24h; Arrivals 24h; Expected Arrivals \n")

#Delete *
browser.get('https://www.mar***ine***traf***fic.com/en/data/?asset_type=po*rts&columns=fla*g,port**name,unlo**code,pho**to,ves**sels_in_po**rt,ves**sels_departures,ves***sels_arr****ivals,ves***sels_exp***ected_arri***vals,lo***cal_ti***me,anch***orage,geo***graphical_ar***ea_one,geograp***hical_ar***ea_two,cover***age')
time.sleep(3)
buttons=browser.find_elements_by_xpath(".//div[@class='qc-cmp-ui-content']/div[@id='qcCmpButtons']/button")
print(len(buttons))
time.sleep(1)
buttons[1].click()
time.sleep(0.6)

page=browser.find_element_by_xpath('//*[@id="reporting_ag_grid"]/div/div[2]/div[3]/div/div/div/div/div[3]/div/p[2]').get_attribute("innerText")
page=int(page[3:5])
for i in range(page):
    scraping_date= datetime.now()
    d1 = scraping_date.strftime("%d/%m/%Y %H:%M:%S")
    ports = browser.find_elements_by_xpath('//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[1]/div/div')
    codes =browser.find_elements_by_xpath('//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div/div[1]')
    vessels_in_ports =browser.find_elements_by_xpath('//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div/div[3]')
    last24h_departures =browser.find_elements_by_xpath('//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div/div[4]')
    last24h_arrivals =browser.find_elements_by_xpath('//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div/div[5]')
    expected_arrivals =browser.find_elements_by_xpath('//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div/div[6]')
    local_times =browser.find_elements_by_xpath('//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div/div[7]')

    for j in range(len(ports)):
        port = ports[j].get_attribute("innerText")
        code = codes[j].get_attribute("innerText")
        vessels = vessels_in_ports[j].get_attribute("innerText")
        last24h_departure = last24h_departures[j].get_attribute("innerText")
        last24h_arrival = last24h_arrivals[j].get_attribute("innerText")
        expected_arrival = expected_arrivals[j].get_attribute("innerText")
        local_time = local_times[j].get_attribute("innerText")
        #print("Scraping Time: %s; Local Time: %s;  Port: %s (%s); Vessels: %s; Departures 24h %s; Arrival 24h %s; Expected %s" % (d1, local_time,  port, code, vessels, last24h_departure, last24h_arrival, expected_arrival))
        outRow = "%s;%s;%s;%s,%s;%s;%s;%s\n" % (d1, local_time,  port, code, vessels, last24h_departure, last24h_arrival, expected_arrival)
        outFile.write(outRow)
    if (i+1 < page):
        browser.find_element_by_xpath('//*[@id="reporting_ag_grid"]/div/div[2]/div[3]/div/div/div/div/div[3]/button[2]').click()
browser.quit()


