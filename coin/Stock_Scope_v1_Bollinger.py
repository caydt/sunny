# 금융 데이터 모듈 로딩, 주식 그래프 그리기 관련 아래 Hello World님 블로그 참조
# https://blog.naver.com/okkam76/221570895384 #이동평균선 그리기 참조
# https://godoftyping.wordpress.com/2015/04/19/python-날짜-시간관련-모듈/
# https://stackoverflow.com/questions/14762181/adding-a-y-axis-label-to-secondary-y-axis-in-matplotlib
# 그래프 layer별 순서 정하기
# https://stackoverflow.com/questions/37246941/specifying-the-order-of-matplotlib-layers


# 데이터 사이언스에서 꼭 쓰는 기본 모듈 로딩 
import numpy as np
import pandas as pd

import os

from datetime import date
from dateutil.relativedelta import relativedelta
# new_date = old_date + relativedelta(years=1)

# 금융 데이터 불러오는 모듈
import FinanceDataReader as fdr

# 그래프 그리기, 한글 폰트 모듈
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc

# StockLab Data science 툴로 국내/해외 주식 그래프 그려보기
# v0.8: 가상화폐 그려보기 (Bitcoin: BTC/KRW, ETH/KRW)
# v0.7: KOSPI 지수 2nd 축에 그리기 (NCSOFT: 036570)
# v0.6: 6m, 1y, 3y 연속 그래프 그리기 (Kakao: 035720)
# v0.5: 주가 저가, 고가 표시 (LG화학: 051910, Tesla: TSLA)
# v0.4: 주가-거래량 단일 그래프, xticklabel 색표시 (Apple: AAPL)
# v0.3: 거래일, xtick 간격 조정, 2배 거래량 색표시 (Naver: 035420)
# v0.2: 이동평균선, Date 모듈 활용 (셀트리온: 068270)
# v0.1: 봉차트, 거래량 2개 subplot 구현 (삼성전자: 005930)


def main():

    # 한글 폰트 로딩
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = fm.FontProperties(fname=path).get_name()
    rc('font', family=font_name)

    today = date.today()
    # today.strftime('%Y-%m-%d')
    # print(today)

    # 90 (3 mon.), 180 (6m), 360 (1y), 720 (2y), ...
    # every_nth 활용 ~120 수준 간격 데이터 샘플링
    pPeriod = 90 #days 기준
    every_nth = 1
    if pPeriod >= 1800: # 62 months
        pMon = 62 
        every_nth = 10
        pStr = '5년'
    elif pPeriod >= 1440: # 48 months
        pMon = 48 
        every_nth = 8
        pStr = '4년'
    elif pPeriod >= 1080: # 36 months
        pMon = 36 
        every_nth = 6
        pStr = '3년'
    elif pPeriod >= 720: # 24 months
        pMon = 24 
        every_nth = 4
        pStr = '2년'
    elif pPeriod >= 360: # 12 months
        pMon = 12 
        every_nth = 2
        pStr = '1년'
    elif pPeriod >= 180: # 6 months
        pMon = 6
        pStr = '6개월'
    elif pPeriod >= 90: # 3 months
        pMon = 3
        pStr = '3개월'
    else:
        pMon = 2
        pStr = '2개월'
        
    # startDate for plotting, startDate+8mon. for 120 MA
    sDate = today - relativedelta(months=pMon)
    sDateMA = today - relativedelta(months=pMon+8)
    
    comCode = 'BTC/KRW' #비트코인 종목코드
    comName = '비트코인 (Bitcoin)'
    comCode = 'ETH/KRW' #비트코인 종목코드
    comName = '이더리움 (Ethereum)'
##    comCode = 'XRP/KRW' #비트코인 종목코드
##    comName = '리플 (Ripple)'
    # 거래소 종목
    comCode = '032350' 
    comName = '롯데관광개발'
    comCode = '008770' 
    comName = '호텔신라'
    comCode = '068270' 
    comName = '셀트리온'
    comCode = '042670' 
    comName = '두산인프라코어'

##    comCode = '032500' 
##    comName = '케이엠더블유'
##    comCode = '028300' 
##    comName = '에이치엘비'
    
    
    # 기간에 맞춘 주식 종목 주가 데이터 로딩
    COMdf = fdr.DataReader(comCode, sDateMA.strftime('%Y-%m-%d'))
    # COMdf = COMdf[::-1] # reverse ordering
    # KOSPIdf = fdr.DataReader('KS11', sDate.strftime('%Y-%m-%d'))
    print(COMdf)
    
    COMdf['moda'] = COMdf.index.strftime('%m.%d') # for x ticks
    COMdf = COMdf.reset_index()
    # print(COMdf)

    # 5일, 20일, 60일 종가 평균화 
    COMdf['ma5'] = COMdf['Close'].rolling(window=5).mean()
    COMdf['ma20'] = COMdf['Close'].rolling(window=20).mean()
    
    COMdf['ubb'] = COMdf['Close'].rolling(window=20).mean() + \
                   2.0 * COMdf['Close'].rolling(window=20).std()
    COMdf['lbb'] = COMdf['Close'].rolling(window=20).mean() - \
                   2.0 * COMdf['Close'].rolling(window=20).std()

    # 기간별 데이터만 추출
    COMdf = COMdf[COMdf['Date'] >= str(sDate)]
    COMdf = COMdf.reset_index(drop=True)
    # print(COMdf)
        
    # Sampling data for every nth step
    start = len(COMdf.index) % every_nth - 1
    if start < 0:
        start = every_nth - 1
    COMdf5 = COMdf[start::every_nth] # for every 5 day
    COMdf5.reset_index(drop=True, inplace=True)
    # print(COMdf5)
    
    # 그래프 그리기
    plt.figure(figsize=(12,8))
    
    pr_line = plt.subplot2grid((5,4), (0,0), rowspan=4, colspan=4)
    vol_bar = plt.subplot2grid((5,4), (4,0), rowspan=1, colspan=4)

    x_ym = np.arange(len(COMdf5.index))

    pr_line.bar(x_ym, height=COMdf5['ubb']-COMdf5['ma20'], \
        bottom = COMdf5['ma20'], width = 1, \
        color = 'moccasin', alpha=0.3)
    pr_line.bar(x_ym, height=COMdf5['lbb']-COMdf5['ma20'], \
        bottom = COMdf5['ma20'], width = 1, \
        color = 'moccasin', alpha=0.3)
    
    pr_line.plot(x_ym, COMdf5['ubb'], lw=0.5, ls='-', c = 'gold', zorder=1)
    pr_line.plot(x_ym, COMdf5['lbb'], lw=0.5, ls='-', c = 'gold', zorder=1)
    
    pr_line.plot(x_ym, COMdf5['ma5'], lw=1.0, ls='--', c = 'forestgreen', \
                 label='5일 이동평균선', zorder=5)
    pr_line.plot(x_ym, COMdf5['ma20'], lw=1.0, ls='--', c = 'black', \
                 label='20일 이동평균선', zorder=5)

    pr_line.bar(x_ym, height=COMdf5['Close']-COMdf5['Open'], \
        bottom = COMdf5['Open'], width = 0.9, \
        color = list(map(lambda c: 'tomato' if c > 0 else 'dodgerblue', \
                         COMdf5['Close']-COMdf5['Open'])), zorder=10)
    
    pr_line.vlines(x_ym, COMdf5['Low'], COMdf5['High'], \
        color = list(map(lambda c: 'tomato' if c > 0 else 'dodgerblue', \
                         COMdf5['Close']-COMdf5['Open'])), zorder=10)

##    pr_line.plot(x_ym, COMdf5['ma60'], lw=0.5, ls='--', c = 'magenta', \
##                 label='60일 이동평균선')
##    pr_line.plot(x_ym, COMdf5['ma120'], lw=0.7, ls='--', c = 'darkorange', \
##                 label='120일 이동평균선')
    pr_line.set_title(comName+' ('+comCode+') 가격 흐름 ('+pStr+')', fontsize=24)
    pr_line.title.set_position([.5, 1.02])
    pr_line.grid(axis='y')
    pr_line.set_xticks([])
    pr_line.ticklabel_format(axis='y', style='sci', scilimits=(3,3))
    pr_line.set_ylabel('주가 (천원)', fontsize=14)
    pr_line.legend(loc='best')
    pr_line.spines['bottom'].set_visible(False)

    # 저가 (Min), 고가 (Max) 찾기
    iMin = COMdf5['Low'].idxmin()
    strMin = "최저 " + f"{COMdf5['Low'][iMin]:,}원\n" + \
             f"({COMdf5['moda'][iMin]})"
    iMax = COMdf5['High'].idxmax()
    strMax = "최고 " + f"{COMdf5['High'][iMax]:,}원\n" + \
             f"({COMdf5['moda'][iMax]})"    
    # print('min,max: ', iMin, iMax)
    
    pr_line.text(x_ym[iMin]*1.01, COMdf5['Low'][iMin]*1.1, \
                 strMin, fontsize=10, color='b')
    pr_line.text(x_ym[iMax]*0.97, COMdf5['High'][iMax]*1.01, \
                 strMax, fontsize=10, color='r')
        
    avg_vol = COMdf5['Volume'].mean()
    avg_vol += avg_vol*0.5
##    color = list(map(lambda c: 'darkorange' \
##                     if c > avg_vol else 'limegreen', \
##                     COMdf5['Volume']))
    color = list(map(lambda c: 'coral' if c > 0 else \
                'cornflowerblue', COMdf5['Close']-COMdf5['Open']))

    color2 = list(map(lambda c: 'black' \
                     if c > avg_vol else 'black', \
                     COMdf5['Volume']))
    # print(color)
    
    vol_bar.bar(x_ym, COMdf5['Volume'], color=color, \
                width = 0.7, zorder=5, alpha=0.4)
    vol_bar.set_xticks(x_ym)
    vol_bar.set_xticklabels(COMdf5['moda'], rotation=30, fontsize=10)

    # xticklabel들을 color2 값으로 사용자 색 설정
    [t.set_color(i) for (i,t) in
         zip(color2, vol_bar.xaxis.get_ticklabels())]

    every_nth = 5
    start = len(x_ym) % every_nth - 1
    if start < 0:
        start = every_nth - 1
             
    for n, label in enumerate(vol_bar.xaxis.get_ticklabels()):
        #print('n: ', n, 'label', label)
        if (n - start) % every_nth != 0:
            label.set_visible(False)
            
    # vol_bar.locator_params(axis='x', nbins=30)
    vol_bar.ticklabel_format(axis='y', style='sci', scilimits=(6,6))
    vol_bar.set_ylabel('거래량 (x백만)', fontsize=12)
    vol_bar.spines['top'].set_visible(False)

    vol_bar.grid(b=None, color='w')
    # vol_bar.grid(axis='y')
    
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.grid(b=None)
    
    # plt.savefig(comName+pStr+'.png')

    plt.show()

    
# main 함수 로딩부
if __name__ == '__main__':
    main()
