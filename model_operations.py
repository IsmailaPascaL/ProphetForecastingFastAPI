import json
import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
import data_manip_functions as dmf


def get_temperature_model():
    with open('temperature_model.json', 'r') as fin:
        m = model_from_json(json.load(fin))

    return m


def save_temperature_model(m):
    with open('temperature_model.json', 'w') as fout:
        json.dump(model_to_json(m), fout)


def get_ammonia_model():
    with open('ammonia_model.json', 'r') as fin:
        m = model_from_json(json.load(fin))

    return m


def save_ammonia_model(m):
    with open('temperature_model.json', 'w') as fout:
        json.dump(model_to_json(m), fout)


def get_humidity_model():
    with open('humidity_model.json', 'r') as fin:
        m = model_from_json(json.load(fin))

    return m


def save_humidity_model(m):
    with open('humidity_model.json', 'w') as fout:
        json.dump(model_to_json(m), fout)


def temperature_forecasting():

    m = get_temperature_model()
    future = m.make_future_dataframe(periods=131400, freq='1min')
    forecast = m.predict(future)
    temperature_forecast = pd.DataFrame(forecast.loc[:, ['ds', 'yhat']])
    temperature_forecast.rename(columns={"yhat": "temperature"}, inplace=True)


    return temperature_forecast

def humidity_forecasting():

    m = get_humidity_model()
    future = m.make_future_dataframe(periods=131400, freq='1min')
    forecast = m.predict(future)
    humidity_forecast = pd.DataFrame(forecast.loc[:, ['ds', 'yhat']])
    humidity_forecast.rename(columns={"yhat":"humidity"}, inplace=True)

    return humidity_forecast

def ammonia_forecasting():

    m = get_ammonia_model()
    future = m.make_future_dataframe(periods=131400, freq='1min')
    forecast = m.predict(future)
    ammonia_forecast = pd.DataFrame(forecast.loc[:, ['ds', 'yhat']])
    ammonia_forecast.rename(columns={"yhat": "nh3_rate"}, inplace=True)

    return ammonia_forecast

def update_temperature_model():

    df = dmf.get_temperature_df(dmf.get_all_data())
    m = Prophet().fit(df)
    save_temperature_model(m)

    return('Temperature Model Updated')

def update_humidity_model():

    df = dmf.get_humidity_df(dmf.get_all_data())
    m = Prophet().fit(df)
    save_humidity_model(m)

    return('Humidity Model Updated')

def update_ammonia_model():

    df = dmf.get_ammonia_df(dmf.get_all_data())
    m = Prophet().fit(df)
    save_ammonia_model(m)

    return('Ammonia Model Updated')