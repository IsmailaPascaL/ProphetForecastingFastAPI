
import data_manip_functions as dmf
from fastapi import FastAPI
import pandas as pd
import heatindex as h
import model_operations as mo

app = FastAPI()

@app.get("/forecast")
def forecasting():

    forecast_temperature = mo.temperature_forecasting()
    forecast_humidity = mo.humidity_forecasting()
    forecast_ammonia = mo.ammonia_forecasting()
    forecast = pd.merge(forecast_temperature, forecast_humidity, left_on='ds', right_on='ds')
    forecast['heat_index'] = h.heatindex(forecast['temperature'], forecast['humidity'])
    forecast = pd.merge(forecast, forecast_ammonia, left_on='ds', right_on='ds')
    dmf.truncate()
    dmf.insert_data(forecast)

    return ('New Forecast added')


@app.get("/modelupdate")
def update_models():
    mo.update_temperature_model()
    mo.update_humidity_model()
    mo.update_ammonia_model()

    return('Models updated')
