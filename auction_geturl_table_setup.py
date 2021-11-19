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
from selenium.common.exceptions import WebDriverException
import bs4

import  time, random

# pathdb = '/home/allanchangcl/webdev/pythona/myproperty/auction.sqlite'
pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/auction.sqlite'
# pathdb = '/root/Webdev/Pythona/Myproperty/auction.sqlite'

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS urls')
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls(idx INTEGER PRIMARY KEY, created_at DATE, prop_url TEXT, area TEXT)
    ''')
    c.close()
    conn.close()

def main():
    tbl_setup()

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