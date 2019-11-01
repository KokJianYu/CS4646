from util import get_data, plot_data 
import datetime as dt  	
import pandas as pd 
import matplotlib.pyplot as plt
from marketsim import compute_portvals_df

class Strategy():
    def testPolicy(self, symbol, sd, ed, sv):
        pass

    def getStrategyName(self):
        return "Please give a strategy name"

class TheoreticallyOptimalStrategy(Strategy):
    def testPolicy(self, symbol, sd, ed, sv):
        date_list = pd.date_range(sd, ed)
        data = get_data([symbol], date_list)[symbol]
        trade_df = pd.DataFrame(index=data.index, columns=[symbol])
        holdings_allowed = [-1000, 0 , 1000]
        current = 0
        for i in range(data.shape[0]-1):
            if data[i+1] > data[i]:
                trade_df.iloc[i] = holdings_allowed[2] - current
                current = holdings_allowed[2]
            elif data[i+1] < data[i]:
                trade_df.iloc[i] = holdings_allowed[0] - current
                current = holdings_allowed[0]
            else:
                trade_df.iloc[i] = holdings_allowed[1] - current
                current = holdings_allowed[1]

        trade_df.loc[data.index[-1]] = holdings_allowed[1]
        return trade_df
    
    def getStrategyName(self):
        return "TheoreticallyOptimalStrategy"

class BenchmarkStrategy(Strategy):
    def testPolicy(self, symbol, sd, ed, sv):
        date_list = pd.date_range(sd, ed)
        data = get_data([symbol], date_list)[symbol]
        trade_df = pd.DataFrame(index=data.index, columns=[symbol])
        trade_df.iloc[0] = 1000
        trade_df = trade_df.fillna(0)
        return trade_df

    def getStrategyName(self):
        return "BenchmarkStrategy"

def author():
    return jkok7

if __name__ == "__main__":
    df = TheoreticallyOptimalStrategy().testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2010,1,1), sv = 100000)
    portfolio = compute_portvals_df(df, "JPM", 100000, 0,0)
    portfolio.plot()
    #print(portfolio)
    plt.savefig("temp.png")