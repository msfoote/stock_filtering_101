# %%
import json
import requests
import pandas as pd
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr
from dateutil.relativedelta import relativedelta

# %%
def main():
    yf.pdr_override()
    with open('config.json') as f:
        data = json.load(f)
    
    sentiment_token = data['sentiment_token']
    sentiment_key = data['sentiment_key']
    param = 'SGP'
    sent_invest_url = f"https://sentimentinvestor.com/api/v3/sort?limit=100&metric={param}&token={sentiment_token}&key={sentiment_key}"
    
    response = requests.get(sent_invest_url)
    # print(response.status_code)
    # test = response.json()
    # print(json.dumps(test, indent = 4, sort_keys=True))
    
    now = dt.datetime.now().strftime('%Y-%m-%d')
    top_sent_stock_fname = f'Top Sentiment Stocks as of {now}.json'
    with open(top_sent_stock_fname, 'w') as json_file:
        json.dump(response.json(), json_file)
    df = pd.read_json(top_sent_stock_fname)
    
    msft = yf.Ticker("BA")
    print(json.dumps(msft.info, indent = 4, sort_keys=True))
    # print(msft.info)
    # ^ returns a named tuple of Ticker objects

    # access each ticker using (example)
    start = (dt.datetime.now()-relativedelta(weeks=1)).strftime('%Y-%m-%d')
    data = pdr.get_data_yahoo("BA", start=start, end=now)
    print(data)
    # print(df)
# %%
if __name__ == "__main__":
    main()
# %%
