import asyncio
import json
import websockets
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
from collections import deque
##   _____ . _____    |                        ______  ._____
##   |     | |    \   |       /\     |\    |  /        |
##   |____ | | __ /   |      /  \    | \   | |         |
##   |     | |   \    |     /____\   |  \  | |         |_____
##   |     | |    \   |    /      \  |   \ | |         |
##   |     | |     \  |__ /        \ |    \|  \______  |_____
##   github.com/made-in-abyss
##   what does this do:
##   market is driven by orders, not price. therefore, OBI is used to see if the bid and ask
##   orders are imbalance (hence the name order book imbalance).
##   this is used with other things to predict sub-second price.

ask_map = {}
bid_map = {}
obi_window = deque(maxlen=600)
ema_obi = 0.000

def calc_obi() -> float:
    global ask_map, bid_map
    ask_price = sorted(ask_map.keys())
    bid_price = sorted(bid_map.keys(),reverse=True)
    mlen = min(int(len(ask_map)),int(len(bid_map)))
    mlen = min(mlen,5)
    if (mlen == 0):
        return -100.0
    
    v_ask = sum(ask_map[v] for v in ask_price[:mlen])
    v_bid = sum(bid_map[v] for v in bid_price[:mlen])
    return (v_bid-v_ask)/(v_ask+v_bid)

async def watch_stream():
    global label,ema_obi
    url = f"wss://stream.binance.com:9443/ws/{ticker}@depth@100ms"
    print("connecting")
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            for item in data["b"]:
                bid_map[float(item[0])] = float(item[1])
                if float(item[1]) == 0:
                    del bid_map[float(item[0])]
        
            for item in data["a"]:
                ask_map[float(item[0])] = float(item[1])
                if float(item[1]) == 0:
                    del ask_map[float(item[0])]
            obi = calc_obi()
            obi_window.append(obi)
            ma_obi = sum(obi_window)/len(obi_window)
            ema_obi = ema_obi*(2/600) + obi
            label.config(text=f"Order Block Imbalance [{ticker}]\nOBI: {str(obi)}\nMA_OBI: {str(ma_obi)}\nEMA_OBI: {str(ema_obi)}")
            root.update()

ticker = str(input("welcome to order block imbalance indicator.\nplease input your asset (find it on binance): "))
root = tk.Tk()
root.title("Order Block Imbalance")
label = tk.Label(root, text="Order Block Imbalance\nOBI: 0.000\nMA_OBI: 0.000\nEMA_OBI: 0.000", font=("Arial", 32, "bold"))
label.pack(padx=30, pady=20)

asyncio.run(watch_stream())