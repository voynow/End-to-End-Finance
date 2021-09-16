import sys
sys.path.append("C:\\Users\\voyno\\Desktop\\finance\\")

import time
import db_utils

from datetime import datetime, timedelta, timezone
from data import data_utils

con, engine = db_utils.db_init()

q = "SELECT distinct dt from price_history order by dt desc limit 1;"

# create cursor
c = con.cursor()

# execute query for last date in price_history
c.execute(q)

# get date value
t = c.fetchone()[0]
date_string = f'{t.year}-{t.month}-{t.day}'
print(date_string)
print(t)


# pull data using date as starting point
new_data = data_utils.get_data(
    source='russell',
    size=10,  # this will change to be all data
    start=date_string)

# close connection
con.close()
