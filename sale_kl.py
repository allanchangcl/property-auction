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
from selenium.common.exceptions import WebDriverException
import bs4

import  time, random

# port = "8118"
# myProxy = "127.0.0.1:"+port
# proxy = Proxy({
#     'proxyType': ProxyType.MANUAL,
#     'httpProxy': myProxy,
#     'ftpProxy': myProxy,
#     'sslProxy': myProxy,
#     'noProxy': ''
# })

# pathdb = '/home/allanchangcl/webdev/pythona/myproperty/sale.sqlite'
pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/sale.sqlite'
site_url = 'http://scrape.this.site/'
search_area = 'KL'

# search_area_str1 = str("//select[@id='s_searchBoxState']/option[@value='")
# search_area_str3 = str("']")
# search_string = search_area_str1 + search_area + search_area_str3

property_type = [
    ['A', 'Apartment/Flat'],
    ['T', 'Terrace/Link/Townhouse'],
    ['B', 'Semi-D/Bungalow'],
    ['E', 'Condo/Serviced Residence']
]

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS urls')
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls(idx INTEGER PRIMARY KEY, created_at DATE, prop_url TEXT, area TEXT, prop_type TEXT)
    ''')
    c.close()
    conn.close()

def web_test():
    browser = webdriver.Firefox()
    browser.get("http://scrape.this.site/")
    print(browser.title)
    browser.quit()

def get_urls(browser, prop_type):
    created_at = date.today()

    conn = sqlite3.connect(pathdb)
    c = conn.cursor()

    page_no = 1

    while True:
        try:
            next_link = WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'simple-pagination')]//ul//li/a[contains(.,'Next')]")))
        except NoSuchElementException:
            next_link = None
        except TimeoutException:
            next_link = None

        bsObj = bs4.BeautifulSoup(browser.page_source, 'lxml')
        get_search = bsObj.find('ul',{'class':'search-results'})
        get_urls = get_search.find_all('h2',{'class':'title'})

        for item in get_urls:
            prop_url = site_url + item.a['href']
            c.execute('INSERT INTO urls(created_at,prop_url,area,prop_type) VALUES (?,?,?,?)', (created_at,prop_url,search_area,prop_type))
            conn.commit()

        if next_link is None:
            break
        else:
            print('Page ' + str(page_no) + ' Completed!')
            page_no += 1
            time.sleep(random.uniform(3.4, 6.9))
            try:
                next_link.click()
            except WebDriverException:
                iframe = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "PopUpFrame")))
                browser.switch_to_frame(iframe)
                # browser.find_element_by_xpath("//div[@class='close_btn']/a/img").click()
                WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='close_btn']/a/img"))).click()
                browser.switch_to_default_content()
                next_link.click()

    c.close()
    conn.close()

def get_url_task():
    for index, item in enumerate(property_type):
        browser = webdriver.Firefox()
        browser.implicitly_wait(10)
        # browser = webdriver.Firefox(proxy=proxy)
        browser.get(site_url)

        # close Facebook Popup
        WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'usrp-fb-btn') and text() = 'No']"))).click()

        # select sale tab
        browser.find_element_by_css_selector(".a-sale").click()

        # select search area
        search_area_str1 = str("//select[@id='s_searchBoxState']/option[@value='")
        search_area_str3 = str("']")
        search_string = search_area_str1 + search_area + search_area_str3
        browser.find_element_by_xpath(search_string).click()

        # select property type
        search_propertytype_str1 = str("//select[@id='s_searchBoxPropertyGroupType']/option[@value='")
        search_propertytype_str3 = str("']")
        search_propertytype_string = search_propertytype_str1 + item[0] + search_propertytype_str3
        browser.find_element_by_xpath(search_propertytype_string).click()

        # proceed with search
        browser.find_element_by_id("s_imgBtnSearch").click()

        get_urls(browser, item[1])
        browser.quit()
        print('Property Type ' + item[1] + ' Done!')

def main():
    # display = Display(visible=0, size=(800, 600))
    # display.start()
    # web_test()
    # tbl_setup()
    # get_urls()
    get_url_task()
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
