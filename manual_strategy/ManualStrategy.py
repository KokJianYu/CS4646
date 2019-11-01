from TheoreticallyOptimalStrategy import Strategy
from indicators import StochasticIndicator, BollingerBandIndicator, MomentumIndicator, get_test_data_with_close_high_low
from util import get_data, plot_data 
import datetime as dt  	
import pandas as pd 
import matplotlib.pyplot as plt
from marketsim import compute_portvals_df


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
            si_value = si.iloc[i, 1]
            bbi_low = bbi.iloc[i, 3]
            bbi_mid = bbi.iloc[i, 1]
            bbi_high = bbi.iloc[i, 2]
            mi_value = mi.iloc[i, 1]
            current_price = d[i]

            if bbi_high <= current_price:
                if si_value > STOCHASTIC_OVERBUY_THRESHOLD:
                    action = -1

            if bbi_low >= current_price:
                if si_value < STOCHASTIC_OVERSELL_THRESHOLD:
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

if __name__ == "__main__":
    df = ManualStrategy().testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2010,1,1), sv = 100000)
    portfolio = compute_portvals_df(df, "JPM", 100000, 0,0)
    print(portfolio)
    portfolio.plot()
    #print(portfolio)
    plt.savefig("temp.png")