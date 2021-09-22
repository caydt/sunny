"""

생존형퀀트의 경제적자유. https://blog.naver.com/starfox119

2021.09.16

1. 완료 /// 코인별 시가총액 매주 갱신할 것.(수동)

2. 시가 총액 대비 거래대금 비교를 통하여 급등 예측 해볼 것

3. orderbook 코드를 통하여 매도잔량 매수잔량을 거래대금으로 환산하고 비교비율 구할 것

4. 매도잔량 거래대금 환산하여 슬리피지 방지대책 세울 것

5. 진입 시점의 20이평을 예상손절가로 잡을 것. 예상손절가의 마이너스 수익률 계산

6. 예상손절가에 해당하는 수익률 도달 시, 안전마진 확보를 위해 50% 매도

7. 볼밴폭 계산하여 지나치게 고점에서는 오히려 진입하지 않도록 조치


"""

#########################################################################
# 업비트 로그인
#########################################################################
import pyupbit						
# 업비트에서 필요한 값들을 불러오기 위해 필요한 모듈

import time	
# 시간을 기록하기 위해 필요한 모듈

access = "9iTK0V8wx8E63BxCmSii08gHZ0xzrBJWNkKPKGHk"												
secret = "OFQb4bQti4SQlhksbDvifJfRxTbtDaj9KcnlrFXh"	                            
upbit  = pyupbit.Upbit(access, secret)                                           
# 업비트에서 자료를 불러오기 위해 로그인하기 위한 코드입니다. 


#########################################################################
# 텔레그램 연결
#########################################################################
import telegram     
# 텔레그램으로 알림을 보내기 위해 필요한 모듈

                                                           
tlgm_token = '2016380701:AAF8xdsjzppwa-72KSLBUYAHcbel4lhP7v0'                   
tlgm_id    = '1059240009'                                                         
bot        = telegram.Bot(token = tlgm_token)                                         
# updates = bot.getUpdates()                                                   
bot.sendMessage(chat_id = tlgm_id, text = 'Sunrise')                        
# 프로그램 시작 시 텔레그램으로 Sunrise라는 메세지를 보냅니다. 


#########################################################################
# 기타 모듈
#########################################################################
import pandas as pd
# 데이터프레임을 생성하기 위한 모듈

import openpyxl
# 문제 발생 시 데이터값을 확인하기 위해 엑셀로 변환해주는 작업을 위해 필요한 모듈
# operation_df.to_excel('check.xlsx')




#########################################################################
# 변수 초기값
#########################################################################
start_time = time.strftime('%H:%M:%S')
# 최초 프로그램 실행 시간을 기록하는 코드입니다. 


weight = 1000000
# 매수조건 충족 시 투입되는 금액. 단위:원

#total_weight = 10000000     # 보유 중인 총 원화. 추후 복리적용 옵션에 활용예정
#weight = total_weight / 2   # 캘리비율 적용 시켜서 전체 보유금의 50%만 투입. 분할매수 분할매도 도입완료

current_price = 0
# 현재 가격을 저장하기 위한 변수

margin = 0
# 현재 수익률을 저장하기 위한 변수

profit_or_loss = 0
# 손익 계산을 위한 변수1

compare_to_abp = 0
# 손익 계산을 위한 변수2

profit = 0
# 수익 저장을 위한 변수

loss = 0
# 손실 저장을 위한 변수

lap = -1
# 추후에 코인 리스트를 갱신하기 위한 변수. 적용 예정



#########################################################################
# 전체 코인 티커 조회
#########################################################################
# tickers = ['KRW-LOOM']
# 특정 코인을 선택하여 실행하기 위한 리스트


tickers = pyupbit.get_tickers(fiat = "KRW")
# 원화 코인 전체를 불러오는 코드. 리스트 형식
'''  
tickers.remove("KRW-ETH")  
tickers.remove("KRW-ADA") 
tickers.remove("KRW-EOS") 
tickers.remove("KRW-XRP") 
tickers.remove("KRW-LTC") 
tickers.remove("KRW-DOT") 
tickers.remove("KRW-DOGE") 
tickers.remove("KRW-VET") 
tickers.remove("KRW-NEO") 
tickers.remove("KRW-BTG") 
tickers.remove("KRW-ETC") 
tickers.remove("KRW-TRX") 
# 위에서 불러온 원화 전체 코인리스트에서 메이저급 코인들 제외하는 코드

'''
# 현재 프로그램 설정은 알트코인들의 펌핑을 포착하는 것에 중점을 두고 있기 때문에
# 시총이 높거나, 메이저급으로 분류되는 코인들은 리스트에서 제외시켰습니다.
# 필요에 따라 추가 또는 삭제하여 진행 가능합니다. 

trading_list = ['KRW-BTC']
# 추후 코인리스트를 갱신할 때 필요한 코드입니다. 





#########################################################################
# 별도 데이터프레임 관리
#########################################################################
operation_df = pd.DataFrame(columns = ['ticker',
                                       'market_cap',
                                       'get_in',
                                       'get_out',
                                       
                                       'in_time',
                                       'out_time',
                                       
                                       'resist_line',
                                       'support_line'])

operation_df['ticker'] = tickers
operation_df.fillna(0, inplace=True) 

# 차트 데이터를 불러오면 ticker_df라는 데이터프레임에 값이 로딩됩니다.
# 하지만 반복문이기 때문에 매번 불러올 때마다 데이터값이 갱신되어서 특정값을 기록할 수 없습니다.
# 그 문제를 해결하기 위해서 코인별로 별도의 데이터프레임을 생성해주는 코드입니다.
# 위의 operation_df 데이터프레임에는 각 코인별로 특정값을 입력시켜서 트레이딩에 활용할 수 있습니다. 




#########################################################################
# 코인별 시가총액. 매주 갱신할 것
#########################################################################

# 시가 총액 대비 거래대금 비교를 통한 상승 예측을 위한 자료
# 전체 원화 코인의 시가총액을 수동으로 입력해야 할 듯
# 단위는 억원
'''
operation_df.loc[(operation_df.ticker == 'KRW-BTC'),    'market_cap'] = 10640670
operation_df.loc[(operation_df.ticker == 'KRW-ETH'),    'market_cap'] = 5003958
operation_df.loc[(operation_df.ticker == 'KRW-ADA'),    'market_cap'] = 939039
operation_df.loc[(operation_df.ticker == 'KRW-XRP'),    'market_cap'] = 613470
operation_df.loc[(operation_df.ticker == 'KRW-DOT'),    'market_cap'] = 414853
operation_df.loc[(operation_df.ticker == 'KRW-DOGE'),   'market_cap'] = 377185
operation_df.loc[(operation_df.ticker == 'KRW-LINK'),   'market_cap'] = 166486
operation_df.loc[(operation_df.ticker == 'KRW-LTC'),    'market_cap'] = 151279
operation_df.loc[(operation_df.ticker == 'KRW-BCH'),    'market_cap'] = 141591
operation_df.loc[(operation_df.ticker == 'KRW-TRX'),    'market_cap'] = 98370
operation_df.loc[(operation_df.ticker == 'KRW-XLM'),    'market_cap'] = 94385
operation_df.loc[(operation_df.ticker == 'KRW-VET'),    'market_cap'] = 90995
operation_df.loc[(operation_df.ticker == 'KRW-ETC'),    'market_cap'] = 90253
operation_df.loc[(operation_df.ticker == 'KRW-ATOM'),   'market_cap'] = 85589
operation_df.loc[(operation_df.ticker == 'KRW-THETA'),  'market_cap'] = 79919
operation_df.loc[(operation_df.ticker == 'KRW-XTZ'),    'market_cap'] = 68328
operation_df.loc[(operation_df.ticker == 'KRW-EOS'),    'market_cap'] = 57510
operation_df.loc[(operation_df.ticker == 'KRW-BCHA'),   'market_cap'] = 57259
operation_df.loc[(operation_df.ticker == 'KRW-CRO'),    'market_cap'] = 56333
operation_df.loc[(operation_df.ticker == 'KRW-HBAR'),   'market_cap'] = 55302
operation_df.loc[(operation_df.ticker == 'KRW-IOTA'),   'market_cap'] = 51503
operation_df.loc[(operation_df.ticker == 'KRW-AXS'),    'market_cap'] = 49404
operation_df.loc[(operation_df.ticker == 'KRW-NEO'),    'market_cap'] = 43171
operation_df.loc[(operation_df.ticker == 'KRW-WAVES'),  'market_cap'] = 40403
operation_df.loc[(operation_df.ticker == 'KRW-BSV'),    'market_cap'] = 35095
operation_df.loc[(operation_df.ticker == 'KRW-BTT'),    'market_cap'] = 31777
operation_df.loc[(operation_df.ticker == 'KRW-CHZ'),    'market_cap'] = 24083
operation_df.loc[(operation_df.ticker == 'KRW-STX'),    'market_cap'] = 22306
operation_df.loc[(operation_df.ticker == 'KRW-XEM'),    'market_cap'] = 20001
operation_df.loc[(operation_df.ticker == 'KRW-TFUEL'),  'market_cap'] = 19861
operation_df.loc[(operation_df.ticker == 'KRW-MANA'),   'market_cap'] = 18197
operation_df.loc[(operation_df.ticker == 'KRW-ICX'),    'market_cap'] = 16929
operation_df.loc[(operation_df.ticker == 'KRW-ENJ'),    'market_cap'] = 16866
operation_df.loc[(operation_df.ticker == 'KRW-IOST'),   'market_cap'] = 15992
operation_df.loc[(operation_df.ticker == 'KRW-ZIL'),    'market_cap'] = 15640
operation_df.loc[(operation_df.ticker == 'KRW-QTUM'),   'market_cap'] = 14875
operation_df.loc[(operation_df.ticker == 'KRW-OMG'),    'market_cap'] = 14619
operation_df.loc[(operation_df.ticker == 'KRW-FLOW'),   'market_cap'] = 14368
operation_df.loc[(operation_df.ticker == 'KRW-BTG'),    'market_cap'] = 14170
operation_df.loc[(operation_df.ticker == 'KRW-BAT'),    'market_cap'] = 13855
operation_df.loc[(operation_df.ticker == 'KRW-SC'),     'market_cap'] = 11079
operation_df.loc[(operation_df.ticker == 'KRW-ONT'),    'market_cap'] = 10677
operation_df.loc[(operation_df.ticker == 'KRW-ANKR'),   'market_cap'] = 9029
operation_df.loc[(operation_df.ticker == 'KRW-SAND'),   'market_cap'] = 8439
operation_df.loc[(operation_df.ticker == 'KRW-KAVA'),   'market_cap'] = 6918
operation_df.loc[(operation_df.ticker == 'KRW-SRM'),    'market_cap'] = 6238
operation_df.loc[(operation_df.ticker == 'KRW-SXP'),    'market_cap'] = 6130
operation_df.loc[(operation_df.ticker == 'KRW-GLM'),    'market_cap'] = 6089
operation_df.loc[(operation_df.ticker == 'KRW-WAXP'),   'market_cap'] = 5928
operation_df.loc[(operation_df.ticker == 'KRW-LSK'),    'market_cap'] = 5773
operation_df.loc[(operation_df.ticker == 'KRW-STORJ'),  'market_cap'] = 5382
operation_df.loc[(operation_df.ticker == 'KRW-POLY'),   'market_cap'] = 5080
operation_df.loc[(operation_df.ticker == 'KRW-PUNDIX'), 'market_cap'] = 4843
operation_df.loc[(operation_df.ticker == 'KRW-MED'),    'market_cap'] = 4337
operation_df.loc[(operation_df.ticker == 'KRW-ARDR'),   'market_cap'] = 4744
operation_df.loc[(operation_df.ticker == 'KRW-ELF'),    'market_cap'] = 4684
operation_df.loc[(operation_df.ticker == 'KRW-CVC'),    'market_cap'] = 4316
operation_df.loc[(operation_df.ticker == 'KRW-STRAX'),  'market_cap'] = 4210
operation_df.loc[(operation_df.ticker == 'KRW-STMX'),   'market_cap'] = 4072
operation_df.loc[(operation_df.ticker == 'KRW-SNT'),    'market_cap'] = 3996
operation_df.loc[(operation_df.ticker == 'KRW-KNC'),    'market_cap'] = 3899
operation_df.loc[(operation_df.ticker == 'KRW-ORBS'),   'market_cap'] = 3741
operation_df.loc[(operation_df.ticker == 'KRW-ONG'),    'market_cap'] = 3478
operation_df.loc[(operation_df.ticker == 'KRW-HIVE'),   'market_cap'] = 3477
operation_df.loc[(operation_df.ticker == 'KRW-REP'),    'market_cap'] = 3412
operation_df.loc[(operation_df.ticker == 'KRW-ARK'),    'market_cap'] = 3307
operation_df.loc[(operation_df.ticker == 'KRW-STEEM'),  'market_cap'] = 2927
operation_df.loc[(operation_df.ticker == 'KRW-DAWN'),   'market_cap'] = 2763
operation_df.loc[(operation_df.ticker == 'KRW-MTL'),    'market_cap'] = 2665
operation_df.loc[(operation_df.ticker == 'KRW-JST'),    'market_cap'] = 2637
operation_df.loc[(operation_df.ticker == 'KRW-PLA'),    'market_cap'] = 2560
operation_df.loc[(operation_df.ticker == 'KRW-MVL'),    'market_cap'] = 2513
operation_df.loc[(operation_df.ticker == 'KRW-POWR'),   'market_cap'] = 2247
operation_df.loc[(operation_df.ticker == 'KRW-STRK'),   'market_cap'] = 2060
operation_df.loc[(operation_df.ticker == 'KRW-IQ'),     'market_cap'] = 1975
operation_df.loc[(operation_df.ticker == 'KRW-BORA'),   'market_cap'] = 1927
operation_df.loc[(operation_df.ticker == 'KRW-SSX'),    'market_cap'] = 1918
operation_df.loc[(operation_df.ticker == 'KRW-DKA'),    'market_cap'] = 1884
operation_df.loc[(operation_df.ticker == 'KRW-QKC'),    'market_cap'] = 1788
operation_df.loc[(operation_df.ticker == 'KRW-META'),   'market_cap'] = 1705
operation_df.loc[(operation_df.ticker == 'KRW-MFT'),    'market_cap'] = 1475
operation_df.loc[(operation_df.ticker == 'KRW-LOOM'),   'market_cap'] = 1319
operation_df.loc[(operation_df.ticker == 'KRW-GAS'),    'market_cap'] = 1191
operation_df.loc[(operation_df.ticker == 'KRW-TT'),     'market_cap'] = 1190
operation_df.loc[(operation_df.ticker == 'KRW-CRE'),    'market_cap'] = 1146
operation_df.loc[(operation_df.ticker == 'KRW-MLK'),    'market_cap'] = 1118
operation_df.loc[(operation_df.ticker == 'KRW-UPP'),    'market_cap'] = 1101
operation_df.loc[(operation_df.ticker == 'KRW-AERGO'),  'market_cap'] = 1096
operation_df.loc[(operation_df.ticker == 'KRW-HUNT'),   'market_cap'] = 983
operation_df.loc[(operation_df.ticker == 'KRW-GRS'),    'market_cap'] = 930
operation_df.loc[(operation_df.ticker == 'KRW-HUM'),    'market_cap'] = 913
operation_df.loc[(operation_df.ticker == 'KRW-STPT'),   'market_cap'] = 870
operation_df.loc[(operation_df.ticker == 'KRW-RFR'),    'market_cap'] = 860
operation_df.loc[(operation_df.ticker == 'KRW-AQT'),    'market_cap'] = 833
operation_df.loc[(operation_df.ticker == 'KRW-SBD'),    'market_cap'] = 817
operation_df.loc[(operation_df.ticker == 'KRW-FCT2'),   'market_cap'] = 743
operation_df.loc[(operation_df.ticker == 'KRW-MOC'),    'market_cap'] = 701
operation_df.loc[(operation_df.ticker == 'KRW-MBL'),    'market_cap'] = 491
operation_df.loc[(operation_df.ticker == 'KRW-AHT'),    'market_cap'] = 470
operation_df.loc[(operation_df.ticker == 'KRW-TON'),    'market_cap'] = 293
operation_df.loc[(operation_df.ticker == 'KRW-CBK'),    'market_cap'] = 137
operation_df.loc[(operation_df.ticker == 'KRW-ZRX'),    'market_cap'] = 100
'''





#########################################################################
# 성질급한 포모를 위한 설정
#########################################################################
#operation_df.loc[(operation_df.ticker == "KRW-LTC"), 'buy_trigger'] = 1

# 횡보를 피하기 위해서, 그리고 고점에서 진입하는 경우를 피하기 위해서
# 최초 프로그램 실행 후 얼마간은 매수가 진행되지 않을 수 있습니다.
# trading, trading_cut, buy_trigger와 같은 값들이 갱신이 되어야 하기 때문입니다.
# 확실한 타이밍이 보이거나, 테스트용으로 바로 매수가 일어나도록 하고 싶을 경우에는
# 위의 코드에 해당 티커명을 입력하고, 다시 실행시키면 됩니다. 







#########################################################################
# 반복문 시작
#########################################################################
while True : 
     for ticker in tickers :
        
        ######################################################################
        # 반복문 내부 변수
        ###################################################################### 
        current_second = int(time.strftime("%S"))
        # 현재 시간(초)를 저장하는 변수. 추후 코인 리스트 갱신에 사용됩니다. 미적용
        
        current_price  = pyupbit.get_current_price(ticker)
        # 업비트에서 현재 가격을 불러옵니다.
        
        abp            = upbit.get_avg_buy_price(ticker)
        # 업비트에서 매수평단가를 불러옵니다. 
        
        ticker_balance = upbit.get_balance(ticker)
        # 업비트에서 해당 코인의 잔고를 불러옵니다. 단위: 갯수
        
        krw_balance    = upbit.get_balance("KRW")
        # 업비트에서 원화 잔고를 불러옵니다. 단위: 원
        
        market_cap     = float(operation_df.loc[(operation_df.ticker == ticker),      'market_cap'])
        get_in         = float(operation_df.loc[(operation_df.ticker == ticker),          'get_in'])
        get_out        = float(operation_df.loc[(operation_df.ticker == ticker),         'get_out'])    
          
        resist_line    = float(operation_df.loc[(operation_df.ticker == ticker),     'resist_line'])
        support_line   = float(operation_df.loc[(operation_df.ticker == ticker),    'support_line'])   
                
        in_time        = float(operation_df.loc[(operation_df.ticker == ticker),         'in_time'])
        out_time       = float(operation_df.loc[(operation_df.ticker == ticker),        'out_time'])
        # 별도 데이터프레임에 값을 저장하고 불러오기 위한 변수 설정
                      
        
        
        ######################################################################
        # 잔고 없을 시 수익률 초기화
        ###################################################################### 
        if abp == 0 :
        # 만약 매수 평단가가 0이라면, 
            margin = 0
            # 현재 수익률은 0으로 처리
            
            operation_df.loc[(operation_df.ticker == ticker),      'max_margin'] = 0
            # 기록된 최대수익률 0으로 갱신
            
            operation_df.loc[(operation_df.ticker == ticker),   'profit_margin'] = 0
            # 기록된 익절수익률 0으로 갱신
            
            operation_df.loc[(operation_df.ticker == ticker),        'loss_cut'] = 0
            # 기록된 로스컷 0으로 갱신
                
            
            
        ######################################################################
        # 수익률 계산
        ###################################################################### 
        if ticker_balance > 0 :
        # 만약 코인 잔고가 0보다 크다면, 
            try:  
                margin = (current_price - abp)/abp
                # 현재 수익률은 (현재가 - 매수평단가)/매수평단가
                
            except ZeroDivisionError:
                print("ZeroDivision")
                # 0으로 나뉘지지 않기 때문에 입력한 에러방지용 코드
                
        
        ######################################################################
        #                                                                    # 
        #                                                                    #
        #                             CHART DATA                             #
        #                                                                    #
        #                                                                    #
        ######################################################################
        
        
        ######################################################################
        # 차트데이터 가져오기
        ######################################################################
        ticker_df   = pyupbit.get_ohlcv(ticker, "minute3") 
        open_price  = ticker_df[  'open']
        high_price  = ticker_df[  'high']
        low_price   = ticker_df[   'low']
        close_price = ticker_df[ 'close']
        volume      = ticker_df['volume']
        # 차트에서 시가, 고가, 저가, 종가, 거래량을 불러옵니다. 
        
        
        ######################################################################
        # 거래량 이동평균 구하기
        ###################################################################### 
        vma180     = ticker_df['vma180'] = volume.rolling(180).mean()
        # 180 거래량 이동평균을 구합니다. 
                
        vma180_p   = str(round(vma180[-2]*current_price/100000000))
        # 180 거래량 이동평균을 구하여 현재가가와 곱한다음 억으로 나눕니다. 억 단위 거래대금 
        
        volume_p   = str(round(volume[-1]*current_price/100000000))
        # 현재 거래량을 현재가와 곱한다음 억으로 나눕니다. 억 단위 거래대금 
        
        volume_sum = ((volume[-1] + volume[-2] + volume[-3])*current_price) / 100000000
        # 3분봉의 3봉간(약 10분)의 거래량을 현재가로 곱하여 거래대금으로 환산. 나누기 천만원.   

        
        ######################################################################
        # 이동평균 구하기
        ###################################################################### 
        ma2  = ticker_df[ 'ma2'] =  close_price.rolling(2).mean()
        # 2 이동평균을 구합니다. 
        
        ma20 = ticker_df['ma20'] = close_price.rolling(20).mean()
        # 20 이동평균을 구합니다.            
            
        
        ######################################################################
        # 볼린저 밴드 구하기  
        ######################################################################
        std20 = ticker_df['std20'] = close_price.rolling(20).std()
        bu20  = ticker_df[ 'bu20'] = ticker_df['ma20'] + ticker_df['std20'] * 1.8
        bd20  = ticker_df[ 'bd20'] = ticker_df['ma20'] - ticker_df['std20'] * 1.8 
        bolinger_height = abs(bu20[-1] - bd20[-1])   # 이거 중요!!!!!!!!!!!!
        
        
        ######################################################################
        # PRICE CHANNEL 상한선, 하한선, 중앙선 구하기
        ######################################################################   
        max_high_7 = ticker_df[  'max_high_7'] = high_price.rolling(7, axis = 0 ).max()  
        min_low_7  = ticker_df[   'min_low_7'] = low_price.rolling(7, axis = 0).min() 
        middle_7   = ticker_df[    'middle_7'] = (max_high_7 + min_low_7) / 2
        # 1분봉의 돈치안채널 20을 구합니다. 
        
        max_high_20 = ticker_df['max_high_20'] = high_price.rolling(20, axis = 0 ).max() 
        min_low_20  = ticker_df[ 'min_low_20'] = low_price.rolling(20, axis = 0).min() 
        # 3분봉의 돈치안채널 20을 구합니다. 
        
        max_high_69 = ticker_df['max_high_69'] = high_price.rolling(69, axis = 0 ).max()    
        min_low_69  = ticker_df[ 'min_low_69'] = low_price.rolling(69, axis = 0).min() 
        # 10분봉의 돈치안채널 20을 구합니다. 
        
        
        
        ######################################################################
        #                                                                    # 
        #                                                                    #
        #                              TRIGGERS                              #
        #                                                                    #
        #                                                                    #
        ######################################################################                                    
                        
        ######################################################################
        # support_line 갱신
        ######################################################################
        if (min_low_69[-1] > min_low_69[-2] ) :
            operation_df.loc[(operation_df.ticker == ticker),    'support_line'] = min_low_69[-1]
                
        
        ######################################################################
        # resist_line 갱신
        ######################################################################
        if resist_line == 0 :
            operation_df.loc[(operation_df.ticker == ticker),     'resist_line'] = max_high_69[-1]
            
        if (min_low_69[-1] < min_low_69[-2] ) :
            operation_df.loc[(operation_df.ticker == ticker),     'resist_line'] = max_high_7[-1]
            
        
        ######################################################################
        # 갱신된 값 적용
        ######################################################################
        
        market_cap     = float(operation_df.loc[(operation_df.ticker == ticker),      'market_cap'])
        get_in         = float(operation_df.loc[(operation_df.ticker == ticker),          'get_in'])
        get_out        = float(operation_df.loc[(operation_df.ticker == ticker),         'get_out'])     
          
        resist_line    = float(operation_df.loc[(operation_df.ticker == ticker),     'resist_line'])
        support_line   = float(operation_df.loc[(operation_df.ticker == ticker),    'support_line'])   
                
        in_time        = float(operation_df.loc[(operation_df.ticker == ticker),         'in_time'])
        out_time       = float(operation_df.loc[(operation_df.ticker == ticker),        'out_time'])
        # 별도 데이터프레임에 위에서 적용된 갱신값들 최종 갱신
        
        
        ######################################################################
        #                                                                    # 
        #                                                                    #
        #                           TRADING CONDITION                        #
        #                                                                    #
        #                                                                    #
        ######################################################################
                                  
        ######################################################################
        # 매도 1. min_low_69[-1] < min_low_69[-2]                                              
        ######################################################################
        # 조건
        if ((ticker_balance * current_price) > 5000 and
            min_low_69[-1] < min_low_69[-2]) :
            # 현재가가 로스컷보다 작거나 같다면
            operation_df.loc[(operation_df.ticker == ticker),          'get_in'] = 0
            operation_df.loc[(operation_df.ticker == ticker),         'get_out'] = 1
            operation_df.loc[(operation_df.ticker == ticker),     'resist_line'] = max_high_7[-1]
            operation_df.loc[(operation_df.ticker == ticker),        'out_time'] = time.time()
            
                        
            print(ticker, ' min_low_69[-1] < min_low_69[-2]')
            print('##############################')
                
            bot.sendMessage(chat_id = tlgm_id, text = 
                            '\n코인: '+ticker+
                            '\n조건: get_out 신호'  + 
                            '\n현재가: ' + str(round(current_price,2)))
            # 텔레그램 메세지에 필요한 정보들을 송출합니다. 
        
                  
        
        ######################################################################
        # 매수1. 전고점 돌파  
        ######################################################################
        # 조건
        if ((ticker_balance * current_price) < 5000 and
            get_in == 0) :
            if (max_high_69[-1] > max_high_69[-2] or 
                ma2[-1] > resist_line ) : 
                operation_df.loc[(operation_df.ticker == ticker),      'get_in'] = 1
                operation_df.loc[(operation_df.ticker == ticker),     'in_time'] = time.time()
                # 현재 시간을 in_time에 저장. 유동적 거래량 이평 생성에 활용
                
                # 텔레그램 알림
                bot.sendMessage(chat_id = tlgm_id, text = 
                                '\n코인: '+ticker+
                                '\n조건: get_in 신호' + 
                                '\n현재가: ' + str(round(current_price,2)))            
                
                
                        
            
        
        ######################################################################
        #                                                                    # 
        #                                                                    #
        #                                 print                              #
        #                                                                    #
        #                                                                    #
        ######################################################################
        
        
        ######################################################################
        # 정규 출력
        ###################################################################### 
        print(time.strftime('%H:%M:%S'), "", 
              "", ticker.ljust(10),
              " get_in:", get_in,
              " get_out", get_out)
        
        if ticker == "KRW-BTC" :
            print("----------------------------------------------------")
            
            
        
        ######################################################################
        # 0.5초 간격으로 티커별 현황조회
        ######################################################################  
        time.sleep(0.5)
        
        
        
        '''
        #########################################################################
        # 특정 시간 설정 예시
        #########################################################################
        #current_time = time.strftime("%H:%M")
        #start_time = "23:00"
        #end_time = "04:00"
                
        #if (current_time >= start_time) and (current_time <= end_time) : 
        #    stop_time = 1
        #else : 
        #    stop_time = 0
        
        
        #########################################################################
        # 거래량 체크 타이머
        #########################################################################
        current_time_minute = time.strftime("%M")
        ma180_check_start = "55"
        ma180_check_end = "59"
        if current_time_minute >= ma180_check_start and current_time_minute <= ma180_check_end :
            ma180_check = 1
        else :
            ma180_check = 0
            
           
                        
        ######################################################################
        # 특정 시간 도달 시 전체 코인 검색 시작
        ###################################################################### 
        if ma180_check == 1 :
            tickers = pyupbit.get_tickers(fiat = "KRW")
        
        if ma180_check == 1 :
            if ma60[199] > ma180[199] :
                if ticker not in crypto_commando :
                    crypto_commando.append(ticker)
        
            else :
                if ticker_balance * current_price > 5000 :
                    if ticker not in crypto_commando :
                        crypto_commando.append(ticker)
                    
                if ticker_balance * current_price <= 5000 :
                    if ticker in crypto_commando :
                        crypto_commando.remove(ticker)
        '''
                
        
        '''
        #########################################################################
        #########################################################################
        # 
        # Crypto Commander의 핵심 기능. 텔레그램 주문 처리
        # 
        #########################################################################
        #########################################################################
        
        #########################################################################
        # 텔레그램을 통해서 매도 주문 처리하기 .. 특정 코인 매도
        #########################################################################  
        telegram_id = bot.getUpdates()[-1].message.chat.id                      # 마지막 메세지 보낸 사람 ID확인
        telegram_message = bot.getUpdates()[-1].message.text                    # 마지막 메세지 확인        
        if telegram_id == 1059240009 : 
            if 'KRW' in telegram_message :                                      # 텔레그램에 KRW라는 텍스트가 있다면, 
                ticker = telegram_message                                       # 메세지는 티커가 되고
                ticker_balance = upbit.get_balance(ticker)                      # 티커 잔고 확인 후에
                sell_record0 = upbit.sell_market_order(ticker, ticker_balance)  # 전량매도
                winners.append(ticker)                                          # 상승 중 매도했으므로 winners에 포함    
                duplication_remove = set(winners)                               # 중복되는 경우가 있어서 중복된 티커는 삭제
                winners = list(duplication_remove)                              # 삭제 후 리스트 형태로 재정리
                
        
                
        
        '''
        '''
        if current_second > 58 :
            telegram_id = bot.getUpdates()[-1].message.chat.id                      # 마지막 메세지 보낸 사람 ID확인
            telegram_message = bot.getUpdates()[-1].message.text
            if telegram_id == 1059240009 : 
                if 'KRW' in telegram_message :     
                    print("OKAY")
                else :
                    print('nothing')
        '''
                
        
