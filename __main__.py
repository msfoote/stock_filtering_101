# %%
import json
import requests
import pandas as pd
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr
import pandas_datareader.data as web
from dateutil.relativedelta import relativedelta
import time

# %%
def get_sent_invt_data(param, sentiment_token, sentiment_key):
    """
    This function obtains the top 100 stocks as measured by `param`. You
    can see the different paramters noted @
    https://sentimentinvestor.com/trending and you can read more about the apis
    available at https://sentimentinvestor.com/developer/docs-endpoints-parsed]

    Args:
        param (str): The parameter you want data for.  Currently I have tested
                        AHI, RHI, SGP, sentiment, reddit_comment_mentions.
                        These may be listed @ the /quote api page
                        @ https://sentimentinvestor.com/developer/docs-endpoints-parsed
        sentiment_token (str): The api token for the site
        sentiment_key (str): The api key for the site
    
    Returns:
        requests.response object: The response from the api call
    """
    # Define the URL for the api call
    url = f"https://sentimentinvestor.com/api/v3/sort?limit=100&metric={param}&token={sentiment_token}&key={sentiment_key}"
    # Call and get the response
    response = requests.get(url)
    return response
# %%
def get_av_quotes(ticker, apikey):
    # Define the URL for the api call
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={apikey}"
    # Call and get the response
    response = requests.get(url)
    return response
# %%
def main():
    # %%
    # Needed to dump json data into pandas
    yf.pdr_override()
    # Open configuration data
    with open('config.json') as f:
        data = json.load(f)
    sentiment_token = data['sentiment_token']
    sentiment_key = data['sentiment_key']
    av_api_key = data['av_api_key']
    
    # %%
    # Obtain the SGP data
    response = get_sent_invt_data('RHI', sentiment_token, sentiment_key)
    
    # If we got a response then dump the data into a JSON file
    if response.ok:
        # Define a name for the JSON file
        now = dt.datetime.now().strftime('%Y-%m-%d')
        top_sent_stock_fname = f'Top Sentiment Stocks as of {now}.json'
        # Dump the JSON data to the new file
        with open(top_sent_stock_fname, 'w') as json_file:
            json.dump(response.json(), json_file)

    # print(json.dumps(test, indent = 4, sort_keys=True))
    
    # %%
    # Read the data we just stored and put into a df
    with open(top_sent_stock_fname, 'w') as json_file:
        json.dump(response.json(), json_file)
    top_rhi_df = pd.read_json(top_sent_stock_fname).set_index('ticker')
    print(top_rhi_df)
    top_rhi_tickers = top_rhi_df.index.tolist()
    # top_rhi_tickers = ['BA']
    
    # %%
    ticker_df = pd.DataFrame()
    for ticker in top_rhi_tickers:
        stock_info = yf.Ticker(ticker)
        if len(stock_info.info) >= 2:
            print(ticker, len(stock_info.info))
            json_data = pd.DataFrame.from_dict(dict(zip(stock_info.info.keys(), [[x] for x in stock_info.info.values()])))
            json_data['ticker'] = ticker
            json_data = json_data.set_index('ticker')
            ticker_df = ticker_df.append(json_data)
            

    # %%
    for ticker in top_rhi_tickers[:1]:
        time.sleep(12.01)
        response = get_av_quotes(ticker,av_api_key)
        print(json.dumps(json.loads(response.text), indent = 4, sort_keys=True))
        print(ticker, response.status_code)
        json_data = pd.DataFrame.from_dict(json.loads(response.text),
                                           orient='index').set_index('01. symbol')
        json_data.style
        top_rhi_df = pd.merge(top_rhi_df,json_data,how='left', left_index=True, right_index=True)
        
        
    # print(json.dumps(msft.info, indent = 4, sort_keys=True))
    # print(msft.info)
    # %%
    # access each ticker using (example)
    start = (dt.datetime.now()-relativedelta(weeks=1)).strftime('%Y-%m-%d')
    data = pdr.get_data_yahoo("BA", start=start, end=now)
    # print(data)
    
    # print(df)
# %%
if __name__ == "__main__":
    main()
# %%
