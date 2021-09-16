import sys
sys.path.append("C:\\Users\\voyno\\Desktop\\finance\\")

import time
import db_utils

from datetime import datetime, timedelta
from data import data_utils

con, engine = db_utils.db_init()

c = con.cursor()

df = data_utils.get_data(source='russell', start=datetime.now() - timedelta(days = 6), size=2)

print(df.head())

con.close()
