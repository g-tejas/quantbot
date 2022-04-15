import websocket
import json
from printy import printy

def on_open(ws):
    print("FTX websocket connection live 🔌")

    channel_data = {
        "op": "subscribe",
        "channel": 'trades',
        'market': 'btc-move-0407'
    }

    ws.send(json.dumps(channel_data))

def on_message(ws, message):
    print(message)
    # raw_msg = json.loads(message)
    # orders = raw_msg['data']
    # for order in orders:
    #     if order['side'] == 'buy':
    #         printy(f"BUY  | PRICE: {order['price']} | SIZE: {order['size']}", 'wB{n}')
    #     else:
    #         printy(f"SELL | PRICE: {order['price']} | SIZE: {order['size']}", 'wB{r}')

def on_close(ws):
    print("FTX websocket connection closed ❌")

socket = "wss://ftx.com/ws/"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()