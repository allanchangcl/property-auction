import sys
import traceback
from datetime import date, datetime
import sqlite3
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

# pathdb = '/home/allanchangcl/webdev/pythona/myproperty/auction.sqlite'
pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/auction.sqlite'
# pathdb = '/root/Webdev/Pythona/Myproperty/auction.sqlite'

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS new_urls')
    c.execute('''
        CREATE TABLE IF NOT EXISTS new_urls(idx INTEGER PRIMARY KEY, created_at DATE, prop_url TEXT, area TEXT)
    ''')
    c.close()
    conn.close()

def new_urls():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute("SELECT * FROM urls A WHERE NOT EXISTS (SELECT * FROM auction B WHERE A.prop_url = B.prop_url)")

    property_url = c.fetchall()

    c.close()
    conn.close()

    for item in property_url:
        conn = sqlite3.connect(pathdb)
        c = conn.cursor()
        c.execute('INSERT INTO new_urls(created_at,prop_url,area) VALUES (?,?,?)', (item[1],item[2],item[3]))
        conn.commit()
        c.close()
        conn.close()

def main():
    tbl_setup()
    new_urls()

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