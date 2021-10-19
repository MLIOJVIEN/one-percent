import time
import pyupbit
import datetime

access = "MA2n1ZR300WwfNRc4lRNU2Ms5N4Zfm61FCdCYQ4T"
secret = "wxSkKu6UIPfTUSmqXTvvkI6xANIzoWJMxeNeAKZd"

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 시작시간 조회
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

# 잔고 정리
def check_bal():
    time.sleep(1)
    balances = upbit.get_balances()
    avg = float(balances[1].get('avg_buy_price'))
    balance = float(balances[1].get('balance'))
    return avg, balance

# 초기 구매
upbit.buy_market_order("KRW-DOGE", 500000)
avg = 0
balance = 0
trade_price = pyupbit.get_current_price("KRW-DOGE")
target_d_price = trade_price*0.99
target_u_price = trade_price*1.01
avg, balance = check_bal()

# Auto Trade
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-DOGE")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            current_price = pyupbit.get_current_price("KRW-DOGE")
            if target_d_price > current_price:
                print("danger")
                krw = upbit.get_balance("KRW")
                if krw > 10000:
                    a_m = current_price*balance
                    b_m = 500000 - a_m
                    if b_m > 5000:
                        upbit.buy_market_order("KRW-DOGE", b_m)
                        avg, balance = check_bal()
                        target_d_price = current_price*0.99
                        target_u_price = current_price*1.01
                        print("buy")
            elif target_u_price < current_price:
                print("chance")
                a_m = current_price*balance
                b_m = a_m - 500000
                stock = b_m/current_price
                if stock*current_price > 5000:
                    upbit.sell_market_order("KRW-DOGE", stock)
                    avg, balance = check_bal()
                    target_d_price = current_price*0.99
                    target_u_price = current_price*1.01
                    print("sell")
        else:
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)