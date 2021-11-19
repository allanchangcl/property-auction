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

# pathdb = '/home/allanchangcl/webdev/pythona/myproperty/auction.sqlite'
pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/sale.sqlite'
search_area = 'SE'

search_area_str1 = str("//select[@id='s_searchBoxState']/option[@value='")
search_area_str3 = str("']")
search_string = search_area_str1 + search_area + search_area_str3

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS urls')
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls(idx INTEGER PRIMARY KEY, created_at DATE, prop_url TEXT, area TEXT)
    ''')
    c.close()
    conn.close()

def web_test():
    browser = webdriver.Firefox()
    browser.get("http://scrape.this.site/")
    print(browser.title)
    browser.quit()

def get_urls():
    site_url = 'http://scrape.this.site/'
    browser = webdriver.Firefox()
    # browser = webdriver.Firefox(proxy=proxy)
    browser.get(site_url)
    # browser.maximize_window()
    created_at = date.today()

    conn = sqlite3.connect(pathdb)
    c = conn.cursor()

    # select auction tab
    browser.find_element_by_css_selector(".a-sale").click()
    # select area
    browser.find_element_by_xpath(search_string).click()
    # execute the search
    browser.find_element_by_id("s_imgBtnSearch").click()

    page_no = 1

    while True:
        try:
            next_link = WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'simple-pagination')]//ul//li/a[contains(.,'Next')]")))
        except NoSuchElementException:
            next_link = None
        except TimeoutException:
            next_link = None

        # close popups
        try:
            iframe = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "PopUpFrame")))
            time.sleep(random.uniform(3.4, 6.9))
            browser.switch_to_frame(iframe)
            browser.find_element_by_xpath("//div[@class='close_btn']/a/img").click()
            browser.switch_to_default_content()
        except NoSuchElementException:
            pass
        except TimeoutException:
            pass

        bsObj = bs4.BeautifulSoup(browser.page_source, 'lxml')
        get_search = bsObj.find('ul',{'class':'search-results'})
        get_urls = get_search.find_all('h2',{'class':'title'})

        for item in get_urls:
            prop_url = site_url + item.a['href']
            c.execute('INSERT INTO urls(created_at,prop_url,area) VALUES (?,?,?)', (created_at,prop_url,search_area))
            conn.commit()

        if next_link is None:
            break
        else:
            print('Page' + str(page_no) + 'Completed!')
            page_no += 1
            next_link.click()

    c.close()
    conn.close()
    browser.quit()

def main():
    # display = Display(visible=0, size=(800, 600))
    # display.start()
    # web_test()
    # tbl_setup()
    get_urls()
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
