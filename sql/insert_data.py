import sys
sys.path.append("C:\\Users\\voyno\\Desktop\\finance\\")

import psycopg2
from sqlalchemy import create_engine

import numpy as np
import pandas as pd

from data import data_utils
from config import get_password


# retrieve password
password = get_password()

# create sqlalchemy engine
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/financial_data')

# Connect to postgres financial_data database
con = psycopg2.connect(
            host="localhost",
            database="financial_data",
            user='postgres',
            password=f'{password}')

# create cursor
c = con.cursor()


def load_yfinance_data():

    # get data from yfinance api
    df = data_utils.get_data(source='russell', size=100, interval='1h')

    return df


def insert_data(df):

    # iter over unique symbols
    first_df = True
    symbols = np.unique([symbol for feature, symbol in df.columns])
    for symbol in symbols:

        # get data associated with symbol
        symbol_df = df.xs(symbol, level=1, drop_level=True, axis=1)

        # create columns for Symbol, Dt
        symbol_repeated = [symbol for i in range(len(symbol_df))]
        symbol_df = symbol_df.assign(Symbol=symbol_repeated)
        symbol_df.index.rename("Dt", inplace=True)
        symbol_df.dropna(axis=0, inplace=True)
        symbol_df.rename({"Adj Close": "Adj_Close"}, axis=1, inplace=True)

        # if first df, create price_history table
        if first_df:
            symbol_df.to_sql('test', con=engine, if_exists='replace', index=True)
            first_df = False

        # add data to price_history table
        symbol_df.to_sql('test', con=engine, if_exists='append', index=True)


def main():

    data = load_yfinance_data()
    insert_data(data)


main()
con.close()
