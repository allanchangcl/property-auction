import sys
import traceback
import sqlite3
import re

pathdb = '/home/allanchangcl/webdev/pythona/myproperty/auction_0529.sqlite'

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS addresses')
    c.execute('''
        CREATE TABLE IF NOT EXISTS addresses(idx INTEGER, address TEXT, latitude FLOAT, longitude FLOAT)
    ''')
    c.close()
    conn.close()

def copy_db_address():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    temp_array = []

    c.execute('''SELECT * FROM auction''')
    address_data = c.fetchall()

    for item in address_data:
        temp_array.append(item)

    for item in temp_array:
        c.execute('INSERT INTO addresses(idx, address) VALUES (?,?)', (item[0], item[5].lstrip()))
        conn.commit()

    c.close()
    conn.close()

def clean_address_aucon():
   # remove AucOn
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    
    c.execute('''SELECT * FROM addresses''')
    address_data = c.fetchall()

    for item in address_data:
        old_address = item[1]
        new_str = re.sub(r"([^,]+)AucOn([^,]+)", "", old_address)
        new_address = re.sub(r",,", ",", new_str)
        c.execute('UPDATE addresses SET address=? WHERE idx=?', (new_address, item[0]))
        conn.commit()

    c.close()
    conn.close()

def clean_address_date():
    # remove Date
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()

    c.execute('''SELECT * FROM addresses''')
    address_data = c.fetchall()

    for item in address_data:
        old_address = item[1]
        new_str = re.sub(r"(?<=\,)(\s?Date.*?)(?=\,)", "", old_address)
        new_address = re.sub(r",,", ",", new_str)
        c.execute('UPDATE addresses SET address=? WHERE idx=?', (new_address, item[0]))
        conn.commit()

    c.close()
    conn.close()

def clean_address_month():
    # remove month
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()

    c.execute('''SELECT * FROM addresses''')
    address_data = c.fetchall()

    for item in address_data:
        old_address = item[1]
        new_str = re.sub(r"[^,]+Jun\b|[^,]+Jul\b", "", old_address)
        new_address = re.sub(r",,", ",", new_str)
        c.execute('UPDATE addresses SET address=? WHERE idx=?', (new_address, item[0]))
        conn.commit()

    c.close()
    conn.close()    


def main():
    tbl_setup()
    copy_db_address()
    clean_address_aucon()
    clean_address_date()
    clean_address_month()

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