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
##   this is the portfolio return, i really locked in on this one

def get_correl(data1,data2):
    ret_a = data1["Close"].pct_change().dropna()
    ret_b = data2["Close"].pct_change().dropna()
    mean_a = np.mean(ret_a)
    mean_b = np.mean(ret_b)
    a_cen = ret_a-mean_a
    b_cen = ret_b-mean_b
    up = sum(a_cen*b_cen)
    down = np.sqrt(sum((ret_a-mean_a)**2))*np.sqrt(sum((ret_b-mean_b)**2))
    cosine = up/down
    return cosine

def get_covar(data1,data2):
    ret_a = data1["Close"].pct_change().dropna()
    ret_b = data2["Close"].pct_change().dropna()
    mean_a = np.mean(ret_a)
    mean_b = np.mean(ret_b)
    a_cen = ret_a-mean_a
    b_cen = ret_b-mean_b
    up = sum(a_cen*b_cen)
    return up*252/(len(ret_a)-1)

def get_annual_ret(data1):
    ret_a = data1["Close"].pct_change().dropna()
    mean_a = np.mean(ret_a)
    return mean_a*252

weights = []
ret_list = []
best_weight = []
best_sharpe = 0.0
def dfs(idx, left):
    global best_weight,best_sharpe,ret_list,weights
    if idx ==N-1:
        weights[idx] = left
        port_variance = 0
        for i in range(0, N):
            for j in range(0, N):
                port_variance += weights[i]*weights[j]*covariance_matrix[i][j]

        port_return = sum(ret_list[i]*weights[i] for i in range(0,N))
        rs_rate = 0.06
        sharpe = (port_return-rs_rate)/np.sqrt(port_variance)
        if sharpe>best_sharpe:
            best_sharpe = sharpe
            best_weight = list(weights)
    else:
        for i in range(0,11): #step = 0.1
            if left<i*0.1:
                break
            weights[idx] = i*0.1
            dfs(idx+1,left-i*0.1)
    return

ticker_list = []
t_name = str(input("please input your asset names (do not mix stock with crypto): "))
t_name = t_name.split()
for v in t_name:
    print(f"fetching {v}")
    weights.append(0.0)
    ticker_list.append(yf.download(tickers=v,period="1y",interval="1d",multi_level_index=False).dropna())
N = len(ticker_list)
covariance_matrix = np.zeros((N, N))

for i in range(0, N):
    for j in range(0, N):
        covariance_matrix[i][j] = get_covar( ticker_list[i], ticker_list[j] )
for dt in ticker_list:
    ret_list.append(get_annual_ret(dt))


dfs(0,1.0)
print(f"FOUND THE BEST PORTFOLIO OF SHARPE: {best_sharpe}")
for i in range(0,N):
    print(f"{t_name[i]}'s weight: {best_weight[i]}")
