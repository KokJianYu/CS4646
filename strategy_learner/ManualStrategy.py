from indicators import StochasticIndicator, BollingerBandIndicator, MomentumIndicator, get_test_data_with_close_high_low
from util import get_data, plot_data 
import datetime as dt  	
import pandas as pd 
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals_df


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
        return "Theoretically Optimal Strategy"

class BenchmarkStrategy(Strategy):
    def testPolicy(self, symbol, sd, ed, sv):
        date_list = pd.date_range(sd, ed)
        data = get_data([symbol], date_list)[symbol]
        trade_df = pd.DataFrame(index=data.index, columns=[symbol])
        trade_df.iloc[0] = 1000
        trade_df = trade_df.fillna(0)
        return trade_df

    def getStrategyName(self):
        return "Benchmark Strategy"


class ManualStrategy(Strategy):
    def testPolicy(self, symbol, sd, ed, sv):
        # Get data
        start_date = sd
        end_date = ed
        date_list = pd.date_range(start_date, end_date)
        d = get_data([symbol], date_list)[symbol]
        close = get_data([symbol], date_list, colname="Close")[symbol]
        high = get_data([symbol], date_list, colname="High")[symbol]
        low = get_data([symbol], date_list, colname="Low")[symbol]
        data = pd.DataFrame(index=d.index, columns=["Adj Close", "Close", "High", "Low"])
        data.iloc[:,0] = d
        data.iloc[:,1] = close
        data.iloc[:,2] = high
        data.iloc[:,3] = low
        data = data.fillna(method="ffill")
        data = data.fillna(method="bfill")
        #data.iloc[:,0] = normalize_data(data.iloc[:,0])

        # Create indicators
        si = StochasticIndicator(data, 14).calculate_helper_data()
        bbi = BollingerBandIndicator(data.iloc[:,0],20,2).calculate_helper_data()
        mi = MomentumIndicator(data.iloc[:,0], n=8).calculate_helper_data()

        MOMENTUM_BULLISH_THRESHOLD = 0.2
        MOMENTUM_BEARISH_THRESHOLD = -0.2
        STOCHASTIC_OVERBUY_THRESHOLD = 80
        STOCHASTIC_OVERSELL_THRESHOLD = 20

        trade_df = pd.DataFrame(index=data.index, columns=[symbol])
        current_holdings = 0
        action = 0
        for i in range(data.shape[0]):
            si_k_value = si.iloc[i, 1]
            si_d_value = si.iloc[i, 2]
            bbi_low = bbi.iloc[i, 3]
            bbi_mid = bbi.iloc[i, 1]
            bbi_high = bbi.iloc[i, 2]
            mi_value = mi.iloc[i, 1]
            current_price = d[i]

            if bbi_high <= current_price:
                if si_k_value > STOCHASTIC_OVERBUY_THRESHOLD:
                    action = -1

            if bbi_low >= current_price:
                if si_k_value < STOCHASTIC_OVERSELL_THRESHOLD:
                    action = 1

            if current_holdings == 1000:
                if current_price <= bbi_mid or mi_value < MOMENTUM_BEARISH_THRESHOLD:
                    action = 0
            if current_holdings == -1000:
                if current_price >= bbi_mid or mi_value > MOMENTUM_BULLISH_THRESHOLD:
                    action = 0

            # buy
            if action == 1:
                trade_df.iloc[i] = 1000 - current_holdings
                current_holdings = 1000
            # sell
            elif action == -1:
                trade_df.iloc[i] = -1000 - current_holdings
                current_holdings = -1000
            # do nothing
            elif action == 0:
                trade_df.iloc[i] = 0 - current_holdings
                current_holdings = 0
        return trade_df

    def getStrategyName(self):
        return "Manual Strategy"

def author():
    return "jkok7"

def generate_graphs():
    from marketsimcode import runSimulation
    runSimulation(ManualStrategy(), BenchmarkStrategy(), "manual_insample.png",True)
    runSimulation(ManualStrategy(), BenchmarkStrategy(), "manual_outofsample.png",True, False)

if __name__ == "__main__":
    generate_graphs()