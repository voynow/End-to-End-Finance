import sys
import sqlite3

import numpy as np
import pandas as pd

# get data_utils from finance repo
sys.path.append("C:\\Users\\voyno\\Desktop\\finance\\")
import data_utils

# connect to database and create cursor
conn = sqlite3.connect("financial_data.db")
c = conn.cursor()


def create_table(table):

    # create table if table does not
    try:
        c.execute("""CREATE TABLE {} (
            Dt Date,
            Adj_Close real,
            Close real,
            High real,
            Low real,
            Open real,
            Volume int,
            Symbol text)""".format(table))

    # Remove table and create new one if already exists
    except sqlite3.OperationalError:
        c.execute("DROP TABLE price_history")
        create_table(table)


def load_yfinance_data():

    # get price data from yfinance api
    df = data_utils.get_data(source="russell")
    df.columns = [(feature.replace(" ", "_"), symbol) for feature, symbol in df.columns]

    return df


def insert_data(df, table):

    # iterate over unique symbols
    unique_symbols = np.unique([symbol for _, symbol in df.columns])
    for symbol in unique_symbols:

        # get data associated with symbol
        symbol_cols = df.columns.values[[symbol in col for col in df.columns]]
        symbol_df = df[symbol_cols]
        symbol_df.columns = [feature for feature, _ in symbol_df.columns]

        # create columns for Symbol, Dt
        symbol_repeated = [symbol for i in range(len(symbol_df))]
        symbol_df = symbol_df.assign(Symbol=symbol_repeated)
        symbol_df.index.rename("Dt", inplace=True)
        symbol_df.dropna(axis=0, inplace=True)

        # add data to price_history table
        symbol_df.to_sql(name=table, con=conn, if_exists='append', index=True)


def main():

    table_name = 'price_history'
    create_table(table_name)
    data = load_yfinance_data()
    insert_data(data, table_name)


main()
c.close()
