from cgitb import reset
from curses import raw
from datetime import datetime, timedelta

import yfinance as yf
import pandas as pd
from dagster import graph, op, ScheduleDefinition, DefaultScheduleStatus

from utils.config import get_environment_config
from utils.helper import make_job

@op
def retrieve_new_stock_market_data():
    # global finance data
    sp500 = yf.Ticker('^GSPC')
    vix = yf.Ticker('^VIX')
    vix3m = yf.Ticker('^VIX3M')
    acwi = yf.Ticker('ACWI')

    # Put/Call Ratios
    cboe_data = pd.read_html('https://markets.cboe.com/us/options/market_statistics/daily/')[0]
    cboe_data.columns = ['NAME', 'RATIO']
    
    # result DataFrame
    observed_date = (datetime.now() - timedelta(days=1)).date()
    indicators = ['sp500', 'acwi', 'vix', 'vix3m', 'total_pcr', 'index_pcr', 'equity_pcr', 'vix_pcr']
    result = {
        "observation_timestamp": [datetime(year=observed_date.year, 
                                        month=observed_date.month, 
                                        day=observed_date.day,
                                        hour=23,
                                        minute=59,
                                        second=59) for _ in indicators],
        "indicator": indicators,
        "value": [
                    float( sp500.info['previousClose'] ),
                    float( acwi.info['previousClose'] ),
                    float( vix.info['previousClose'] ),
                    float( vix3m.info['previousClose'] ),
                    float( cboe_data[ cboe_data.NAME == 'TOTAL PUT/CALL RATIO']['RATIO'].values[0] ),
                    float( cboe_data[ cboe_data.NAME == 'INDEX PUT/CALL RATIO']['RATIO'].values[0] ),
                    float( cboe_data[ cboe_data.NAME == 'EQUITY PUT/CALL RATIO']['RATIO'].values[0] ),
                    float( cboe_data[ cboe_data.NAME == 'CBOE VOLATILITY INDEX (VIX) PUT/CALL RATIO']['RATIO'].values[0] ),
                ]
    }
    return result

@op
def append_new_data_to_storage(data):
    data_path = get_environment_config()['raw_data_path'] + 'stock_indicators.csv'

    data = pd.DataFrame(data)
    try:
        existing = pd.read_csv(data_path)
        final = existing.append(data)
    except:
        final = data

    final.to_csv(data_path, index=False)

@graph
def retrieve_stock_market_indicators_job():
    append_new_data_to_storage(retrieve_new_stock_market_data())

retrieve_stock_market_indicators_job_schedule = ScheduleDefinition(
    job=make_job(retrieve_stock_market_indicators_job), cron_schedule="0 6 * * 2-6", default_status=DefaultScheduleStatus.RUNNING
)

def get_jobs():
    return [make_job(retrieve_stock_market_indicators_job)]

def get_scheduels():
    return [retrieve_stock_market_indicators_job_schedule]