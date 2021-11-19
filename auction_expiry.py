import sys
import traceback
from datetime import date, datetime
import sqlite3

# pathdb = '/home/allanchangcl/webdev/pythona/myproperty/auction.sqlite'
# pathdb = '/home/allanchangcl/webdev/laravel/okukikime/database/auction.sqlite'
pathdb = '/home/allanchangcl/Webdev/Pythona/Myproperty/auction.sqlite'
# pathdb = '/root/Webdev/Pythona/Myproperty/auction.sqlite'

def tbl_setup():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS dates')
    c.execute('''
        CREATE TABLE IF NOT EXISTS dates(idx INTEGER, post_date DATE, auction_date DATE, expired BOOL, updated_at DATE)
    ''')
    c.close()
    conn.close()

def get_dates():
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
        i = None
        auction_date = datetime.today()
       
        for index, search in enumerate(details_info):
            if 'Auction Date :' in search:
                i = index
        
        if i is not None:
            temp_auction_date = details_info[i][15:]
            auction_date = datetime.strptime(temp_auction_date, "%d/%m/%Y")
                
        for index, search in enumerate(details_info):
            if 'Posted Date :' in search:
                i = index
        
        temp_post_date = details_info[i][14:]
        # print(temp_post_date)
        # print(item[0])

        post_date = datetime.strptime(temp_post_date, "%d/%m/%Y")

        c.execute('INSERT INTO dates(idx, post_date, auction_date) VALUES (?,?,?)', (item[0], post_date, auction_date))
        conn.commit()

    c.close()
    conn.close()

def update_expired():
    conn = sqlite3.connect(pathdb)
    c = conn.cursor()
    c.execute('''SELECT * FROM dates''')

    dates_array = c.fetchall()

    c.close()
    conn.close()

    conn = sqlite3.connect(pathdb)
    c = conn.cursor()

    for item in dates_array:
        auction_date = item[2]
        today_date = datetime.today()
                
        # if date is today consider expired, helps with recs with no auction date
        if (auction_date > str(today_date)):
            expired = False
        else:
            expired = True
        
        c.execute('UPDATE dates SET expired=?, updated_at=? WHERE idx=?', (expired, today_date, item[0]))
        conn.commit()

    c.close()
    conn.close()

def main():
    tbl_setup()
    get_dates()
    update_expired()

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