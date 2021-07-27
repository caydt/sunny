btc = pyupbit.get_ohlcv("kRW-BTC","minute1")
close = btc['close']

window20 = close.rolling(20)
ma20 = window20.mean()
last_ma20 = ma20[199]

std20 = window20.std()
last_st20 = std20[199]


bbu = last_ma20 + last_st20 * 2

print(bbu)
print(last_ma20)
