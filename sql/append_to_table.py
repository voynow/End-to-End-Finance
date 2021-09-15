import sys
sys.path.append("C:\\Users\\voyno\\Desktop\\finance\\")

import time
import db_utils

from datetime import datetime, timedelta
from data import data_utils

con, engine = db_utils.db_init()

c = con.cursor()

start = time.time()
df = data_utils.get_data(source='russell', start=datetime.now() - timedelta(days = 1), size=1000)
print(time.time() - start)

start = time.time()
df = data_utils.get_data(source='russell', start='2000-01-01', size=1000)
print(time.time() - start)
