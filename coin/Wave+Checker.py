# -*- coding: utf-8 -*-
"""

생존형퀀트의 경제적자유. https://blog.naver.com/starfox119

"""

 #########################################################################
 # 업비트 로그인
 #########################################################################
import pyupbit						
import time	
access = "9iTK0V8wx8E63BxCmSii08gHZ0xzrBJWNkKPKGHk"												
secret = "OFQb4bQti4SQlhksbDvifJfRxTbtDaj9KcnlrFXh"	
upbit = pyupbit.Upbit(access, secret)	

#########################################################################
# 텔레그램 연결
#########################################################################
import telegram
tlgm_token = '1772750536:AAFHXUrrcXi15DnUyJ99ZEb5WwqOaZIOE6A'
tlgm_id = '1059240009'                                                          
bot = telegram.Bot(token = tlgm_token)                                          
updates = bot.getUpdates()                                                      
bot.sendMessage(chat_id = tlgm_id, text = 'Wave Checker')                   

#########################################################################
# 변수 초기값
#########################################################################
abp = 0                                                                                    
current_price = 0                                                                      

#########################################################################
# 전체 코인 티커 조회
#########################################################################
tickers = pyupbit.get_tickers(fiat = "KRW")

#########################################################################
# 종류별 코인 목록
#########################################################################
wave = []

#########################################################################
# 반복문 시작
#########################################################################
while True : 
    
    for ticker in tickers :
        
        current_price = pyupbit.get_current_price(ticker)                                                               
        
        #########################################################################
        # 데이타 추출1. 
        #########################################################################
        ticker_df_m1 = pyupbit.get_ohlcv(ticker, "minute10")                   
        o_m1 = ticker_df_m1['open']
        h_m1 = ticker_df_m1['high']   
        l_m1 = ticker_df_m1['low']                                   
        c_m1 = ticker_df_m1['close']                                                    
        v_m1 = ticker_df_m1['volume']
                
        o_m1_199 = o_m1[199]        
        h_m1_199 = h_m1[199]
        l_m1_199 = l_m1[199]
        c_m1_199 = c_m1[199]
        c_m1_198 = c_m1[198]
                
        m1_high_180_199 = h_m1.iloc[180:199]                                     
        m1_high_180_198 = h_m1.iloc[180:198]
        m1_high_180_197 = h_m1.iloc[180:197]                                    
        
        m1_max_high_180_199 = m1_high_180_199.max(axis = 0)                     
        m1_max_high_180_198 = m1_high_180_198.max(axis = 0)                     
                        
        window20_m1 = c_m1.rolling(20)                                          
        ma20_m1 = window20_m1.mean()
        ma20_m1_199 = ma20_m1[199]                                              
        ma20_m1_198 = ma20_m1[198] 
        ma20_m1_197 = ma20_m1[197]
                                        
        ma20_m1_trend_199 = ma20_m1_199 - ma20_m1_198                          
        ma20_m1_trend_198 = ma20_m1_198 - ma20_m1_197
                
        window60_m1 = c_m1.rolling(60)                                          
        ma60_m1 = window60_m1.mean()
        ma60_m1_199 = ma60_m1[199]  
        ma60_m1_198 = ma60_m1[198] 
        ma60_m1_197 = ma60_m1[197] 
        
        ma60_m1_trend_199 = ma60_m1_199 - ma60_m1_198 
        ma60_m1_trend_198 = ma60_m1_198 - ma60_m1_197
                                                          
        #########################################################################
        # 출력 지점
        #########################################################################        
        print(time.strftime('%m-%d %H:%M:%S'),ticker)      
        
        #########################################################################
        # 매도1. 추세 추종 + 눌림목 + 전고점 돌파
        #########################################################################  
        if ma20_m1_trend_198 > 0 and ma60_m1_trend_198 > 0 :
            if current_price > ma20_m1_199 and current_price < m1_max_high_180_198 :
                if ticker in wave :                     
                    print(ticker, "Wave")
                    
                else: 
                    bot.sendMessage(chat_id = tlgm_id, text = ticker+' Perfect Wave') 
                    wave.append(ticker)                  
        
        #########################################################################
        # 매도1. 데드크로스
        #########################################################################  
        if ticker in wave :
            if current_price < ma60_m1_199 :
                bot.sendMessage(chat_id = tlgm_id, text = ticker+' Wave End') 
                wave.remove(ticker)
                          
        #########################################################################
        # 0.1초 간격으로 티커별 현황조회
        #########################################################################          
        time.sleep(0.1)
        
