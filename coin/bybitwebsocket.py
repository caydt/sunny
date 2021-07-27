################ bybit WebSocket example. 
import asyncio 
import websockets
import json

async def my_loop_WebSocket_bybit():
    async with websockets.client.Connect("wss://stream.bybit.com/realtime") as websocket:
        print("Connected to bybit WebSocket");
        await websocket.send('{"op":"subscribe","args":["trade.BTCUSD"]}');
        data_rcv_response = await websocket.recv(); 
        print("response for subscribe req. : " + data_rcv_response);

        while True:
            data_rcv_strjason = await websocket.recv(); 
            data_rcv_dict = json.loads(data_rcv_strjason); # convert to Pyhton type dict 
            data_trade_list = data_rcv_dict.get('data',0); 
            num_data_trade_list = len(data_trade_list); 
            print("Num List : " + str(num_data_trade_list));
            for data_trade_dict in data_trade_list : ## variable number of element(dictionary) in List per one packet. 
                print("timestamp : " + data_trade_dict.get('timestamp',0) 
                        + ", price : " + str(data_trade_dict.get('price',0))   
                        + ", size : " + str(data_trade_dict.get('size',0)) 
                        );
            

##### main exec 
my_loop = asyncio.get_event_loop();  
my_loop.run_until_complete(my_loop_WebSocket_bybit()); # loop for connect to WebSocket and receive data. 
my_loop.close();
