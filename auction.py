import sys
import traceback
from datetime import date, datetime
import sqlite3
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import bs4
import re
import time, random

# pathdb = '/home/allanchangcl/webdev/pythona/myproperty/auction.sqlite'
pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/auction.sqlite'

location = [
    ['KL', 'Kuala Lumpur'],
    ['SE', 'Selangor'],
    ['PE', 'Penang'],
    ['PK', 'Perak']
]

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS auction')
    c.execute('''
        CREATE TABLE IF NOT EXISTS auction(idx INTEGER PRIMARY KEY, created_at DATE, prop_url TEXT, area TEXT, address_1 TEXT, address_2 TEXT, price TEXT, details_info TEXT, lat_long TEXT, latitude NUMERIC, longitude NUMERIC)
    ''')
    c.close()
    conn.close()

def get_property_details(property_url, area):
    # run headless
    display = Display(visible=0, size=(1024, 768))
    display.start()

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
                WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'details-info')]")))
                bsObj = bs4.BeautifulSoup(browser.page_source, 'lxml')
                break
            except TimeoutException:
                print('Trying ' + str(attempts) + ' attempts')
                browser.quit()
                time.sleep(random.uniform(3.4, 6.9))
                browser = webdriver.Chrome()
                browser.implicitly_wait(10)
                if attempts == 100:
                    print('Quit Trying URL ' + item[2])
                attempts += 1

        created_at = item[1]
        prop_url = item[2]
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
        
        # Geodata
        scripts  = bsObj.find_all('script')
        get_lat = re.compile('mapLat: ".+"')
        get_lon = re.compile('mapLon: ".+"')

        # initialize lat_raw_data and lon_raw_data incase not found - UnboundLocalError
        lat_raw_data = 'mapLat: "0"'
        lon_raw_data = 'mapLon: "0"'

        for script in scripts:
            data_search = get_lat.search(str(script.string))
            if data_search:
                lat_raw_data = data_search.group(0)

        for script in scripts:
            data_search = get_lon.search(str(script.string))
            if data_search:
                lon_raw_data = data_search.group(0)

        latitude = lat_raw_data[lat_raw_data.index("\"") + 1:lat_raw_data.rindex("\"")]
        longitude = lon_raw_data[lon_raw_data.index("\"") + 1:lon_raw_data.rindex("\"")]
        latitude_longitude = latitude + ", " + longitude

        # save to database
        conn = sqlite3.connect(pathdb)
        c = conn.cursor()
        c.execute('INSERT INTO auction(created_at, prop_url, area, address_1, address_2, price, details_info, lat_long, latitude, longitude) VALUES (?,?,?,?,?,?,?,?,?,?)', (created_at, prop_url, area, address_1, address_2, price, details_info, latitude_longitude, latitude, longitude,))
        conn.commit()
        c.close()
        conn.close()

        print('URL ' + str(index) + ' Completed')
        time.sleep(random.uniform(3.4, 6.9))
        counter += 1

    browser.quit()
    display.stop()

def get_property_details_task():
    for index, item in enumerate(location):
        conn = sqlite3.connect(pathdb)
        c = conn.cursor()
        c.execute("SELECT * FROM new_urls WHERE area=?", (item[0],))

        property_url = c.fetchall()
        
        c.close()
        conn.close()

        get_property_details(property_url, item[0])
        print('Property Type ' + item[1] + ' Done!')


def main():
    # tbl_setup()
    get_property_details_task()

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