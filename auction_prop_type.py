import sys
import traceback
import sqlite3
import re

# pathdb = '/home/allanchangcl/webdev/pythona/myproperty/auction.sqlite'
# pathdb = '/home/allanchangcl/webdev/laravel/okukikime/database/auction.sqlite'
pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/auction.sqlite'

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS types')
    c.execute('''
        CREATE TABLE IF NOT EXISTS types(idx INTEGER, prop_type TEXT)
    ''')
    c.close()
    conn.close()

def get_data():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('''SELECT * FROM auction''')

    auction_array = c.fetchall()
    c.close()
    conn.close()

    conn = sqlite3.connect(pathdb)
    c = conn.cursor()

    for item in auction_array:
        details_info = item[7].split(',')

        for index, search in enumerate(details_info):
            if 'Property Type: : ' in search:
                i = index

        tmp_str = details_info[i]
        prop_type = tmp_str.replace("Property Type: : ","",1)

        c.execute('INSERT INTO types(idx, prop_type) VALUES (?,?)', (item[0], prop_type))
        conn.commit()

    c.close()
    conn.close()

def main():
    tbl_setup()
    get_data()

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