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
upbit.buy_market_order("KRW-DOGE", 80000)
avg = 0
balance = 0
avg, balance = check_bal()

# Auto Trade
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-DOGE")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_d_price = avg*0.99
            target_u_price = avg*1.01
            current_price = pyupbit.get_current_price("KRW-DOGE")
            if target_d_price > current_price:
                print("danger")
                krw = get_balance("KRW")
                if krw > 10000:
                    a_m = current_price*balance
                    b_m = 100000 - a_m
                    if b_m > 1000:
                        upbit.buy_market_order("KRW-DOGE", b_m)
                        avg, balance = check_bal()
                        print("buy")
            if target_u_price < current_price:
                print("chance")
                upbit.sell_market_order("KRW-DOGE", balance*0.01)
                avg, balance = check_bal()
                print("sell")
        else:
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)