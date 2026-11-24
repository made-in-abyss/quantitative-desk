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
##   this is the correlation matrix CVM

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


ticker_list = []
t_name = str(input("please input your asset names (do not mix stock with crypto): "))
t_name = t_name.split()
for v in t_name:
    print(f"fetching {v}")
    ticker_list.append(yf.download(tickers=v,period="1mo",interval="1d",multi_level_index=False).dropna())
N = len(ticker_list)
correlation_matrix = np.zeros((N, N))


print("begin calculating correl matrix.")
for i in range(0, N):
    for j in range(0, N):
        correlation_matrix[i][j] = get_correl( ticker_list[i], ticker_list[j] )

for i in range(0,N):
    print(correlation_matrix[i])
