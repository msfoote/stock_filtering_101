# %%
import requests
import json

# I got a free token and secret key from the developer section in sentimentinvestor.com
with open('config.json') as f:
        data = json.load(f)
token = data['sentiment_token']
secret_key = data['sentiment_key']
RHI_rank = requests.get("https://sentimentinvestor.com/api/v3/sort?limit=100&metric=RHI&token={0}&key={1}".format(token, secret_key)).json()
def get_analysis(recommendation):

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
stock_list = []

for stock in RHI_rank:
    yf_json = requests.get("https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}?modules=recommendationTrend".format(stock["ticker"])).json()
    stock_cap_json = requests.get("https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}?modules=defaultKeyStatistics".format(stock["ticker"])).json()
    all_data = requests.get("https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}?modules=assetProfile,balanceSheetHistory,balanceSheetHistoryQuarterly,calendarEvents,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,earnings,earningsHistory,earningsTrend,financialData,fundOwnership,incomeStatementHistory,incomeStatementHistoryQuarterly,indexTrend,industryTrend,insiderHolders,insiderTransactions,institutionOwnership,majorDirectHolders,majorHoldersBreakdown,netSharePurchaseActivity,price,quoteType,recommendationTrend,secFilings,sectorTrend,summaryDetail,summaryProfile,symbol,upgradeDowngradeHistory,fundProfile,topHoldings,fundPerformance".format(stock["ticker"])).json()
    stock_cap = 0
    if yf_json["quoteSummary"]["result"] != None:
        
        try:
            analysis = get_analysis(yf_json["quoteSummary"]["result"][0]["recommendationTrend"]["trend"][0])
            stock_cap = int(stock_cap_json["quoteSummary"]["result"][0]["defaultKeyStatistics"]["enterpriseValue"]["raw"])
            price = all_data['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
            if stock_cap < 1000000000 and stock_cap > 1 and analysis != None and price < 2:
                stock_list.append(stock["ticker"])
        except:
            pass
    
print(stock_list)