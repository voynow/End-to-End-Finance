import sys
sys.path.append("C:\\Users\\voyno\\Desktop\\finance\\")

import numpy as np
import pandas as pd

import db_utils
from data import data_utils

con, engine = db_utils.db_init()

# create cursor
c = con.cursor()


def load_yfinance_data():

    # get data from yfinance api
    df = data_utils.get_data(source='russell', interval='1h')

    return df


def insert_data(df, table_name):

    # iter over unique symbols
    first_df = True
    symbols = np.unique([symbol for feature, symbol in df.columns])
    for symbol in symbols:

        # get data associated with symbol
        symbol_df = df.xs(symbol, level=1, drop_level=True, axis=1)

        # create columns for Symbol, Dt
        symbol_repeated = [symbol for i in range(len(symbol_df))]
        symbol_df = symbol_df.assign(Symbol=symbol_repeated)
        symbol_df.index.rename("dt", inplace=True)
        symbol_df.fillna(-1)
        symbol_df.rename({"Adj Close": "adj_close"}, axis=1, inplace=True)
        symbol_df.columns = [col.lower() for col in symbol_df.columns]

        # if first df, create price_history table
        if first_df:
            symbol_df.to_sql(table_name, con=engine, if_exists='replace', index=True)
            first_df = False
            continue

        # add data to price_history table
        symbol_df.to_sql(table_name, con=engine, if_exists='append', index=True)


def main():

    table_name = "price_history"

    data = load_yfinance_data()
    insert_data(data, table_name)


main()
con.close()
