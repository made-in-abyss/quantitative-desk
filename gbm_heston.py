import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

##   _____ . _____    |                        ______  ._____
##   |     | |    \   |       /\     |\    |  /        |
##   |____ | | __ /   |      /  \    | \   | |         |
##   |     | |   \    |     /____\   |  \  | |         |_____
##   |     | |    \   |    /      \  |   \ | |         |
##   |     | |     \  |__ /        \ |    \|  \______  |_____
##   github.com/made-in-abyss
##   this is the mean-reverting vol GBM, by Heston


plt.title("WanderingVOl GBM Price Simulation")
plt.xlabel("Days")
plt.ylabel("Price ($)")
N=0
def ohlc(data): #this calculates asset's volatility with respect to o,h,l,c
    high = data["High"].to_numpy()
    low = data["Low"].to_numpy()
    open = data["Open"].to_numpy()
    close = data["Close"].to_numpy()
    daily_variance = 0.5*(np.log(high/low)**2)-0.3863*(np.log(close/open)**2)
    vol = np.sqrt(np.mean(daily_variance))
    return vol

def drift(data): #drift, log normal like the standard thing
    price1 = data["Close"].to_numpy()[0]
    price2 = data["Close"].to_numpy()[-1]
    return np.log(price2/price1)/(N-1)

def get_ret(uy,o):
    o = o*np.random.normal(loc=1.0,scale=0.05)
    shock = np.random.standard_t(df=4)
    return np.exp((uy- (o**2)/2) + o*shock)

def brownian(uy, o,s0,n): #run
    y = []
    for i in range(1,n+1):
        s0 = s0*get_ret(uy,o)
        y.append(s0)
    plt.plot(y)
    


print("welcome to gbm (geometric brownian motion) simulation.\nthe simulation will run off the last 30 days price data.")
t_name = str(input("input ticker: "))
n = int(input("how long would this simulation run for: "))
q = int(input("how many time would this simulation run: "))
ticker = yf.download(tickers=t_name,period="1mo",interval="1d",multi_level_index=False).dropna()
N = len(ticker["Close"].to_numpy())
o = ohlc(ticker)
uy = drift(ticker)
s0 = ticker["Close"].to_numpy()[-1]
print(f"volatility: {o}\ndrift (lognormal): {uy}\nlatest price: {s0}")
for i in range(0,q):
    brownian(uy,o,s0,n)
plt.show()