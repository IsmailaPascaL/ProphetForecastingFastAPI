from timeit import timeit

import psycopg2
import pandas as pd
import os


database = os.getenv('YARTEK_DB')
user = os.getenv('YARTEK_DB_USER')
password = os.getenv('YARTEK_DB_PASSWORD')
host = os.getenv('YARTEK_DB_HOST')
port = os.getenv('YARTEK_DB_PORT')


def truncate():
    conn = psycopg2.connect(
        database=database, user=user, password=password, host=host, port=port
    )
    conn.autocommit = True
    cur = conn.cursor()
    query = ('''Truncate forecast''')
    cur.execute(query)

def get_all_data():
    conn = psycopg2.connect(
        database=database, user=user, password=password, host=host, port=port
    )
    conn.autocommit = True
    query = pd.read_sql_query('''Select * from sensordata''', conn)
    df = pd.DataFrame(query)
    df = df.drop("sensorid", axis=1)
    df = df.drop("heat_index", axis=1)
    df.reset_index(level=0, inplace=True)

    return df


def insert_data(df):
    df.to_csv('forecast.csv', index=False, header=False)
    conn = psycopg2.connect(
        database=database, user=user, password=password, host=host, port=port
    )
    cursor = conn.cursor()
    #copy_query= ("COPY forecast(date,temperature,humidity,heat_index,nh3_rate) FROM 'forecast.csv' DELIMITER ',' CSV HEADER")
    try:
        # for index, row in df.iterrows():
        #     cursor.execute(add_line, (row.ds, row.temperature, row.humidity, row.heat_index, row.nh3_rate))
        with open('forecast.csv', 'r') as f:
            cursor.copy_from(f, 'forecast', sep=',')
        conn.commit()
        cursor.close()
    except psycopg2.OperationalError as err:
        print(err)


def get_temperature_df(df):
    df_temperature = pd.DataFrame(df.loc[:, ['date', 'temperature']])
    df_temperature.rename(columns={"date": "ds", "temperature": "y"}, inplace=True)

    return df_temperature


def get_ammonia_df(df):
    df_temperature = pd.DataFrame(df.loc[:, ['date', 'nh3_rate']])
    df_temperature.rename(columns={"date": "ds", "nh3_rate": "y"}, inplace=True)

    return df_temperature


def get_humidity_df(df):
    df_temperature = pd.DataFrame(df.loc[:, ['date', 'humidity']])
    df_temperature.rename(columns={"date": "ds", "humidity": "y"}, inplace=True)

    return df_temperature




