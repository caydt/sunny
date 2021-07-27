import pandas as pd
import datetime
import requests
import pandas as pd
import time
import webbrowser
import numpy

a = 1

while True:
    url = "https://api.upbit.com/v1/candles/minutes/5"
    
    querystring = {"market":"KRW-BTC","count":"100"}
    
    response = requests.request("GET", url, params=querystring)
    
    data = response.json()
    
    df = pd.DataFrame(data)
    
    df=df['trade_price'].iloc[::-1]
    

    
    if a==1:
        url = "https://www.binance.com/kr/register?ref=X1401JUS"
        webbrowser.open(url)

        url = "https://bit.ly/3oWaIXG"
        webbrowser.open(url)

        url = "https://www.xn-----bt9ig0b31lcsga13i850awk2a6pg.com/"
        webbrowser.open(url)
        a=2    
    

    unit=2
    
    band1=unit*numpy.std(df[len(df)-20:len(df)])
    
    bb_center=numpy.mean(df[len(df)-20:len(df)])
    
    band_high=bb_center+band1
    
    band_low=bb_center-band1   

        

    print('볼린저밴드 상단: ', round(band_high,2))
    print('볼린저밴드 하단: ', round(band_low,2))
    print('')
    time.sleep(1)
