import time
import pyupbit
import datetime

access = "XxJPTN3oTu253a95FnWjsj1rAQsjC7JzyT27QpXY"
secret = "CWycoINMmCOEmI1dKMo3zR1rDRiuWMNY2uRpQP0u"


def get_target_price(ticker,k):
    df = (pyupbit.get_ohlcv(ticker, interval="minute5", count=3)) 
    df['stack'] = ((df['close'] - df['open'])/df['open'])*100
    if df.iloc[0]['stack'] <= k:
        count = 1
        if df.iloc[1]['stack'] <= k:
            count = 2
            if df.iloc[2]['stack'] <= k:
                count = 3
    else :
        count = 0
    # df['count'] = df['stack'].apply(lambda x: +1 if x< k else 0 )
    # df['decision'] = df['count'].apply(lambda x:'buy' if x==1 else'')
    if count == 3:
        target_price = (df.iloc[0]['close'] + df.iloc[0]['open'])/2
    else : 
        target_price = 9999999999
    return target_price

def get_buy_point(ticker,k):
    df = (pyupbit.get_ohlcv(ticker, interval="minute5", count=3))
    df['stack'] = ((df['close'] - df['open'])/df['open'])*100
    if df.iloc[0]['stack'] <= k:
        count = 1
        if df.iloc[1]['stack'] <= k:
            count = 2
            if df.iloc[2]['stack'] <= k:
                count = 3
    else :
        count = 0
    buy_point = 0
    if count == 3 :
        buy_point = df.iloc[2]['close']
    return buy_point

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0 

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit("XxJPTN3oTu253a95FnWjsj1rAQsjC7JzyT27QpXY", "CWycoINMmCOEmI1dKMo3zR1rDRiuWMNY2uRpQP0u")
print("autotrade start")

while True:
    try:
        buy_point = get_buy_point("KRW-BTC",-0.22)
        current_price = get_current_price("KRW-BTC")
        target_price = get_target_price("KRW-BTC",-0.22)
        trade = 0
        if buy_point>=current_price:
            krw = get_balance("KRW")
            if trade == 0:
                upbit.buy_market_order("KRW-BTC", 10000)
                buy_point = 0
                trade = 1
                bp = current_price
                print("Buy at",bp)
        if trade == 1:
            btc = get_balance("BTC")
            if target_price <= current_price:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                trade == 0    
                sp = current_price
                print("sell at", sp)
                print("earn rate is",(bp/sp)*100)
            elif ((current_price-buy_point)/buy_point)*100 <-0.8:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                trade == 0
                sp = current_price
                print("sell at", sp)
                print("earn rate is",(bp/sp)*100)
        time.sleep(1)       
    except Exception as e:
        print(e)
        time.sleep(1)
