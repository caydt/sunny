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

tlgm_token = '1916811134:AAEn2wp-Y1cQBT61y2xxU3-neZUIlr0k0m4'
tlgm_id = '1059240009'
bot = telegram.Bot(token = tlgm_token)
updates = bot.getUpdates()
bot.sendMessage(chat_id = tlgm_id, text = 'Alt Sniper')

#########################################################################
# 변수 초기값
#########################################################################
abp = 0
current_price = 0
margin = 0

#########################################################################
# 전체 코인 티커 조회
#########################################################################

tickers = pyupbit.get_tickers(fiat = "KRW")


#########################################################################
# 반복문 시작
#########################################################################

while True : 
    for ticker in tickers :
        #########################################################################
        # 매수평단가, 수익률 매번 갱신
        ######################################################################### 
        abp = upbit.get_avg_buy_price(ticker)         
        current_price = pyupbit.get_current_price(ticker)

        if abp > 0 :
            margin = (current_price - abp)/abp
        
        if abp == 0 :
            margin = 0
                
        if ticker == "KRW-BTC" :
            print("START")
        
        #########################################################################
        # 티커별 시고저종가 및 거래량 확인. 1분봉. 100봉 
        #########################################################################    
        ticker_df = pyupbit.get_ohlcv(ticker, "minute1", 100)
        ticker_df["tall"] = ticker_df["close"] - ticker_df["open"]
        o = ticker_df['open']
        h = ticker_df['high']
        l = ticker_df['low']
        c = ticker_df['close']
        v = ticker_df['volume']
        t = ticker_df["tall"]
        vp =ticker_df['value']
        
        #########################################################################
        # 2분 봉 전까지의 Price channel 상한선 확인(전저점 확인)
        #########################################################################
        sh = h.iloc[1:97]
        mh = sh.max(axis = 0)
        
        sl = l.iloc[1:97]
        ml = sl.min(axis = 0)
           
        v_98 = v[98]        
        t_98 = t[98]
        h_98 = t[98]
        vp_98 = vp[98]
        
        v_99 = v[99]
        t_99 = t[99]
        h_99 = h[99]
        vp_99 = vp[99]
        
        max_v = v.max(axis = 0)
        max_t = t.max(axis = 0)
        
                
        #########################################################################
        # 출력 지점
        #########################################################################
        if v_98 == max_v and t_98 == max_t and t_99 > 0 :
            print('\033[31m',time.strftime('%m-%d %H:%M:%S'),ticker,"   ", round(abp),round(margin,4),"///",round(v_98),":",round(max_v),"///",round(t_98),":",round(max_t),'\033[0m')
            bot.sendMessage(chat_id = tlgm_id, text = +
                            ('TC : '+str(ticker)+" 1",
                            'CP : '+str(current_price),
                            '1TP : '+str(current_price*1.001),
                            '2TP : '+str(current_price*1.01),
                            '3TP : '+str(current_price*1.02),
                            '4TP : '+str(current_price*1.03),
                            'FTP : '+str(current_price*1.035),
                            'VOL :'+str(v_98),
                            'VOLP :'+str(v_99),
                            'VAL :'+str(vp_98),
                            'VALP :'+str(vp_99),sep=="\n"))
        
        if v_98 == max_v and t_98 == max_t and t_99 > 0 and v > 2 * v_100 :
            print('\033[31m',time.strftime('%m-%d %H:%M:%S'),ticker,"   ", round(abp),round(margin,4),"///",round(v_98),":",round(max_v),"///",round(t_98),":",round(max_t),'\033[0m')
            bot.sendMessage(chat_id = tlgm_id, text = 
                           ('TC : '+str(ticker)+" 1V",
                            'CP : '+str(current_price),
                            '1TP : '+str(current_price*1.001),
                            '2TP : '+str(current_price*1.01),
                            '3TP : '+str(current_price*1.02),
                            '4TP : '+str(current_price*1.03),
                            'FTP : '+str(current_price*1.035),
                            'VOL :'+str(v_98),
                            'VOLP :'+str(v_99),
                            'VAL :'+str(vp_98),
                            'VALP :'+str(vp_99),sep=='\n'))
            
        if t_99 > mh-ml :
            print('\033[31m',time.strftime('%m-%d %H:%M:%S'),ticker,"   ", round(abp),round(margin,4),"///",round(v_99),":",round(max_v),"///",round(t_99),":",round(max_t),'\033[0m')
            bot.sendMessage(chat_id = tlgm_id, text = 
                            ('TC : '+str(ticker)+" 2",
                            'CP : '+str(current_price),
                            '1TP : '+str(current_price*1.001),
                            '2TP : '+str(current_price*1.01),
                            '3TP : '+str(current_price*1.02),
                            '4TP : '+str(current_price*1.03),
                            'FTP : '+str(current_price*1.035),
                            'VOL :'+str(v_98),
                            'VOLP :'+str(v_99),
                            'VAL :'+str(vp_98),
                            'VALP :'+str(vp_99),sep=='\n'))
            
        if t_99 > mh-ml and 2 * v_100 :
            print('\033[31m',time.strftime('%m-%d %H:%M:%S'),ticker,"   ", round(abp),round(margin,4),"///",round(v_99),":",round(max_v),"///",round(t_99),":",round(max_t),'\033[0m')
            bot.sendMessage(chat_id = tlgm_id, text = 
                            ('TC : '+str(ticker)+" 2V",
                            'CP : '+str(current_price),
                            '1TP : '+str(current_price*1.001),
                            '2TP : '+str(current_price*1.01),
                            '3TP : '+str(current_price*1.02),
                            '4TP : '+str(current_price*1.03),
                            'FTP : '+str(current_price*1.035),
                            'VOL :'+str(v_98),
                            'VOLP :'+str(v_99),
                            'VAL :'+str(vp_98),
                            'VALP :'+str(vp_99),sep=='\n'))
        
        else :
            print(time.strftime('%m-%d %H:%M:%S'),ticker,"   ",round(abp),round(margin,4),"///",round(v_98),":",round(max_v),"///",round(t_98),":",round(max_t))
        
        #########################################################################
        # 0.1초 간격으로 티커별 현황조회
        #########################################################################    
        
        time.sleep(0.5)
