# %%
import requests
import json

class Secrets:
    def __init__(self, json_secrets) -> None:
        # I got a free token and secret key from the developer section in sentimentinvestor.com
        with open(json_secrets) as f:
                data = json.load(f)
        self.token = data['sentiment_token']
        self.secret_key = data['sentiment_key']

class Stock:
    def __init__(self, ticker) -> None:
        self.ticker = ticker

    def get_yf_data(self):
        all_data = requests.get(f"""https://query2.finance.yahoo.com/v10/finance/quoteSummary/
                                {self.ticker}?modules=assetProfile,balanceSheetHistory,
                                balanceSheetHistoryQuarterly,calendarEvents,cashflowStatementHistory,
                                cashflowStatementHistoryQuarterly,defaultKeyStatistics,earnings,
                                earningsHistory,earningsTrend,financialData,fundOwnership,
                                incomeStatementHistory,incomeStatementHistoryQuarterly,indexTrend,
                                industryTrend,insiderHolders,insiderTransactions,institutionOwnership,
                                majorDirectHolders,majorHoldersBreakdown,netSharePurchaseActivity,
                                price,quoteType,recommendationTrend,secFilings,sectorTrend,
                                summaryDetail,summaryProfile,symbol,upgradeDowngradeHistory,
                                fundProfile,topHoldings,fundPerformance""").json()
        return all_data if all_data["quoteSummary"]["result"] != None else None 
    
    def get_analysis(self, recommendation):

        strong_buy = recommendation["strongBuy"]
        buy = recommendation["buy"]
        hold = recommendation["hold"]
        underperform = recommendation["sell"]
        sell = recommendation["strongSell"]
        recommendation_num = strong_buy + buy + hold + underperform + sell
        if recommendation_num != 0:
            return (strong_buy + buy * 2 + hold * 3 + underperform * 4 + sell * 4) / recommendation_num
        else:
            return 5
    
# I got a free token and secret key from the developer section in sentimentinvestor.com
secrets = Secrets('config.json')
RHI_rank = requests.get("https://sentimentinvestor.com/api/v3/sort?limit=100&metric=RHI&token={0}&key={1}".format(secrets.token, secrets.secret_key)).json()
stock_list = []

for stock in RHI_rank:
    x = Stock(stock)
    data = x.get_yf_data()
    stock_cap = 0
    if data != None:
        
        try:
            analysis = x.get_analysis(data["quoteSummary"]["result"][0]["recommendationTrend"]["trend"][0])
            stock_cap = int(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["enterpriseValue"]["raw"])
            price = data['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
            if stock_cap < 1000000000 and stock_cap > 1 and analysis != None and price < 2:
                stock_list.append(stock["ticker"])
        except:
            pass
    
print(stock_list)