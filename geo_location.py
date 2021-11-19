import sys
import traceback
from datetime import date, datetime
import sqlite3
from geopy.geocoders import GoogleV3
import time, random

pathdb = '/home/allanchangcl/webdev/pythona/myproperty/auction_0529.sqlite'
# pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/auction.sqlite'

conn = sqlite3.connect(pathdb)
c = conn.cursor()
c.execute('''SELECT addresses.idx, addresses.address FROM addresses JOIN dates ON addresses.idx=dates.idx WHERE dates.expired = 0''')
address_data = c.fetchall()
c.close()
conn.close()

def tbl_setup():
    # lat long column at addresses table. setup in clean_db_address.py
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS geos')
    c.execute('''
        CREATE TABLE IF NOT EXISTS geos(address TEXT, latitude FLOAT, longitude FLOAT)
    ''')
    c.close()
    conn.close()

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def get_latlong():
    # get only the address column
    address_only_col_array = []
    for item in address_data:
        address_only_col_array.append(item[1]) 

    # remove duplicates
    unique_address_array = remove_duplicates(address_only_col_array)

    # init goggle map api
    g = GoogleV3(api_key="yourgoogleapikey")

    conn = sqlite3.connect(pathdb)
    c = conn.cursor()

    # count = 0

    for item in unique_address_array:
        # if count < 10:
        #     count += 1
        # else:
        #     break
        
        if len(item) > 20:
            location = g.geocode(item, timeout=10)
            if location is not None:
                c.execute('INSERT INTO geos(address, latitude, longitude) VALUES (?,?,?)', (item, location.latitude, location.longitude))
            else:
                c.execute('INSERT INTO geos(address, latitude, longitude) VALUES (?,?,?)', (item, None, None))
            conn.commit()
            time.sleep(1)

    c.close()
    conn.close()
    
# def update_address_db():
#     conn = sqlite3.connect(pathdb)
#     c = conn.cursor()

#     for item in address_data:
#         for geo_item in address_data_geo:
#             if item[1] == geo_item[0]:
#                 c.execute('UPDATE addresses SET latitude=?, longitude=? WHERE idx=?', (geo_item[1],geo_item[2], item[0]))
#                 conn.commit()

#     c.close()
#     conn.close()

def main():
    tbl_setup()
    # get_address_data()
    get_latlong()
    # update_address_db()

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
