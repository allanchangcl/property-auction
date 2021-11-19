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
    c.execute('DROP TABLE IF EXISTS prices')
    c.execute('''
        CREATE TABLE IF NOT EXISTS prices(idx INTEGER, built_up INTEGER, reserved_price INTEGER, price_sqfoot INTEGER, price_range TEXT)
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
        prop_buildup = 0
        i = None
       
        for index, search in enumerate(details_info):
            if 'Built-Up :' in search:
                i = index
            else: 
                if 'Land Area :' in search:
                    i = index

        if i is not None:
            try:
                build_up_str = details_info[i]
                temp_data = [int(s) for s in build_up_str.split() if s.isdigit()]
                prop_buildup = temp_data[0] 
            except IndexError:
                try:
                    str = details_info[i]
                    prop_buildup = re.findall(r'\d+', str)
                    prop_buildup = int(prop_buildup[0]) * int(prop_buildup[1])
                except IndexError:
                    str = details_info[i]
                    prop_buildup = re.findall(r'\d+', str)
                    prop_buildup = int(prop_buildup[0])

        for index, search in enumerate(details_info):
            if 'Reserved Price :' in search:
                i = index
        try:
            price_str = details_info[i]
            temp_data = [int(s) for s in price_str.split() if s.isdigit()]
            prop_price = temp_data[0] 
        except IndexError:
            prop_price = 0

        c.execute('INSERT INTO prices(idx, built_up, reserved_price) VALUES (?,?,?)', (item[0], prop_buildup, prop_price))
        conn.commit()

    c.close()
    conn.close()    

def calc_sq_feet():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('''SELECT * FROM prices''')

    prices_array = c.fetchall()
    c.close()
    conn.close()

    conn = sqlite3.connect(pathdb)
    c = conn.cursor()

    for item in prices_array:
        if item[1] is not 0:
            price_per_sq = int(item[2] / item[1])

            # group_names = ['below 150', '150-250', '250-350', '350-500', '500-750', '750-1000', 'above 1000']
            # if price > 100 and price < 300:
            
            if price_per_sq > 0 and price_per_sq <= 150:
                price_range = '000-150'
            elif price_per_sq > 150 and price_per_sq <= 250:
                price_range = '150-250'
            elif price_per_sq > 250 and price_per_sq <= 350:
                price_range = '250-350'
            elif price_per_sq > 350 and price_per_sq <= 500:
                price_range = '350-500'
            elif price_per_sq > 500 and price_per_sq <= 750:
                price_range = '500-750'
            elif price_per_sq > 750 and price_per_sq <= 1000:
                price_range = '750-1000'
            elif price_per_sq > 1000:
                price_range = '1000-0000'

            c.execute('UPDATE prices SET price_sqfoot=?, price_range=? WHERE idx=?', (price_per_sq, price_range, item[0]))
        
        conn.commit()

    c.close()
    conn.close()

def main():
    tbl_setup()
    get_data()
    calc_sq_feet()

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