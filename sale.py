import sys
import traceback
from datetime import date, datetime
import sqlite3
# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import bs4

import time, random

# pathdb = '/home/allanchangcl/webdev/pythona/myproperty/sale.sqlite'
pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/sale.sqlite'

property_type = [
    # ['A', 'Apartment/Flat'],
    ['T', 'Terrace/Link/Townhouse'],
    ['B', 'Semi-D/Bungalow'],
    ['E', 'Condo/Serviced Residence']
]

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS auction')
    c.execute('''
        CREATE TABLE IF NOT EXISTS auction(idx INTEGER PRIMARY KEY, created_at DATE, prop_url TEXT, prop_type TEXT, area TEXT, address_1 TEXT, address_2 TEXT, price TEXT, details_info TEXT)
    ''')
    c.close()
    conn.close()

def get_property_details(property_url,location):
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    
    split_task_random_blocks = random.randint(500, 800)
    counter = 0

    for index, item in enumerate(property_url):
        if (counter == split_task_random_blocks):
            print('Sleeping .....')
            time.sleep(random.randint(300,600))
            split_task_random_blocks = random.randint(500, 800)
            counter = 0
        
        attempts = 1
        while attempts < 100:
            try:
                browser.get(item[2])
                WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'details-info')]")))
                bsObj = bs4.BeautifulSoup(browser.page_source, 'lxml')
                break
            except TimeoutException:
                print('Trying ' + str(attempts) + ' attempts')
                if attempts == 100:
                    print('Quit Trying URL ' + item[2])
                    attempts += 1

        created_at = item[1]
        prop_url = item[2]
        area = location
        prop_type = item[4]
        address_1 = bsObj.find('div',{'class':'building-info-one'}).h1['title']
        address_2 = bsObj.find('div',{'class':'building-info-one'}).h2['title']
        price = bsObj.find('div',{'class':'building-info-two'}).h2.text

        # details-info
        details_info_array = []
        details_info_container = bsObj.find_all('ul', class_='infos')
        for item_ul in details_info_container:
            for item_li in item_ul.find_all('li'):
                details_info_array.append(item_li.text.replace(',', '').lstrip())

        details_info = ','.join(map(str, details_info_array))

        # save to database
        conn = sqlite3.connect(pathdb)
        c = conn.cursor()
        c.execute('INSERT INTO auction(created_at, prop_url, prop_type, area, address_1, address_2, price, details_info) VALUES (?,?,?,?,?,?,?,?)', (created_at, prop_url, prop_type, area, address_1, address_2, price, details_info))
        conn.commit()
        c.close()
        conn.close()

        print('URL ' + str(index) + ' Completed')
        time.sleep(random.uniform(3.4, 6.9))
        counter += 1

    browser.quit()

def get_property_details_task(location):
    for index, item in enumerate(property_type):
        conn = sqlite3.connect(pathdb)
        c = conn.cursor()
        c.execute("SELECT * FROM urls WHERE area=? AND prop_type=?", (location,item[1]))

        property_url = []
        for row in c:
            property_url.append(row)
        
        c.close()
        conn.close()

        get_property_details(property_url,location)
        print('Property Type ' + item[1] + ' Done!')

def main():
    # display = Display(visible=0, size=(800, 600))
    # display.start()
    # web_test()
    location = 'KL'
    get_property_details_task(location)
    # tbl_setup()
    # display.stop()

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        raise
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)