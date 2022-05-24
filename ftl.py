"""

1. Stochastic Slow 14 dagar bryter har vart under 10 och sen bryter över 10.
2. OMX30 ska ha gjort samma.

Strategin ser ut som följande:
    StoS(14) = Stochastic Slow 14.
    KÖP:
    - StoS(14) bryter upp över 10 ifrån under 10.
    - StoS(14) för OMXS30 bryter upp över 10 idag, igår eller förrgår.

    EXIT:
    - Stänger över MA20.

"""
from API import borsdata_client as API
ins = API.BorsdataAPI(YOUR_API_KEY)
import requests
from datetime import date,timedelta

n = ins.get_instrument_stock_prices(1938)
OMX30 = ins.get_instrument_stock_prices(627)

def moving_average_20(stock, date):
    s = stock.loc[:date].tail(20)
    return s.close.sum() / 20

def stochastic_slow_14(stock, date):
    stock = stock.loc[stock.index == date]
    close = stock.close
    lowest = stock.low
    highest = stock.high
    return (close - lowest) / (highest - lowest) * 14

def check_for_buy(today, yesterday, day_before):
    if today.size > 0:
        if today > 10:
            return True
    if yesterday.size > 0:
        if yesterday > 10:
            return True
    if day_before.size >0:
        if day_before > 10:
            return True
        
def summarize():
    total_good_trades = 0
    for x in history:
        try:
            bought = history[x][0]
            sold = history[x][1]

            if sold > bought:
                total_good_trades += 1

            p = bought - sold
            percentage = p/bought
            print(f"Bought: {bought}, Sold: {sold}, Percentage: {percentage}")

        except IndexError:
            pass
    
    print(f"Total trades: {len(history)}, Positive Trades: {total_good_trades}")
    hr = round(total_good_trades/len(history)*100)
    print(f"Hitrate: {hr}% (ROUNDED)")
   
#BASERA SKITEN PÅ DATUM
if __name__ == "__main__":
    bought = False
    number_of_trades = 0
    history = {} 
    old = 0
    for shurda,a in enumerate(n.index):
        stock = stochastic_slow_14(n,a)

        if shurda > 3:
            yesterday = stochastic_slow_14(OMX30, a-timedelta(days=1))
            day_before_yesterday = stochastic_slow_14(OMX30, a-timedelta(days=2))

            if not bought:
                if old < 10:
                    if check_for_buy(stock.values, yesterday.values, day_before_yesterday.values):
                        bought = True
                        history[number_of_trades] = [n.loc[n.index == a].close.values]

        old = stock.values
        ma20 = moving_average_20(n, a)
        if bought:
            if n.loc[n.index == a].close.values > ma20:
                bought = False
                history[number_of_trades].append(n.loc[n.index == a].close.values)
                if history[number_of_trades][0] == history[number_of_trades][1]:
                    del history[number_of_trades]
                number_of_trades += 1

    summarize()
