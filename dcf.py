import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
##   _____ . _____    |                        ______  ._____
##   |     | |    \   |       /\     |\    |  /        |
##   |____ | | __ /   |      /  \    | \   | |         |
##   |     | |   \    |     /____\   |  \  | |         |_____
##   |     | |    \   |    /      \  |   \ | |         |
##   |     | |     \  |__ /        \ |    \|  \______  |_____
##   github.com/made-in-abyss
##   this is the dcf (screener)

def get_dcf(fcf,ori_g) ->float:
    wacc = 0.09
    g = ori_g
    latest_fcf = fcf.iloc[-1]
    pv = 0.0
    for i in range(1,11):
        shock = np.random.poisson(lam=0.25)
        if shock==1:
            g += 0.04
        elif shock>=2:
            g -= 0.07
        else:
            g = g * 0.75 + 0.03 * 0.25
        latest_fcf *= (g+1)
        pv += latest_fcf/(1+wacc)**i
    terminal_val = latest_fcf*(1.03)/(wacc-0.03)
    pv+= terminal_val/(1+wacc)**10
    return pv

def calc_dcf(data):
    try:
        fcf = data.cashflow.loc["Free Cash Flow"].dropna().sort_index()
    except:
        fcf = (data.cashflow.loc["Operating Cash Flow"] + data.cashflow.loc["Capital Expenditure"]).dropna().sort_index()
    g = (fcf - fcf.shift(1)) / fcf.shift(1).abs()
    g = g.median()
    g = float(np.clip(g, -0.25, 0.40))
    pv = []
    for i in range(0,1000):
        pv.append(get_dcf(fcf,g))
    return np.median(pv)

ticker_list = []
pv = []
ev = []
t_name = str(input("please input your asset names (do not mix stock with crypto): "))
t_name = t_name.split()
for v in t_name:
    print(f"fetching {v}")
    ticker_list.append(yf.Ticker(ticker=v))
N = len(ticker_list)
for i, v in enumerate(ticker_list):
    ret = calc_dcf(v)
    pv.append(ret)
    info = v.info
    shares = info.get("impliedSharesOutstanding") or info.get("sharesOutstanding")
    cash = info.get("totalCash") or 0
    debt = info.get("totalDebt") or 0
    price = info.get("currentPrice") or v.fast_info["lastPrice"]
    if not shares or not price:
        print(f"skipping {t_name[i]}: missing shares or price")
        continue
    fair_val = (ret +cash - debt) / shares
    print(f"{t_name[i]} | fair: ${fair_val} | now: ${price} | multiple: {fair_val/price}x")
