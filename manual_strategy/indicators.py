from util import get_data, plot_data 
import datetime as dt  	
import pandas as pd 
import matplotlib.pyplot as plt

class Indicator():
    def __init__(self, data):
        self.data = data

    def calculate_helper_data(self):
        pass

    def plot_graph(self):
        pass

class MomentumIndicator(Indicator):
    def __init__(self, data, n=8):
        super().__init__(data)
        self.n = n

    def calculate_helper_data(self):
        num_days = self.data.shape[0]
        cols = ["Adjusted_Close", "Momentum"]
        self.helper_data = pd.DataFrame(index=self.data.index, columns=cols)
        self.helper_data.iloc[:,0] = self.data
        self.helper_data.iloc[:,1] = self.data.rolling(window=self.n).apply(lambda d: d[-1]/d[0] - 1, raw=False)
        return self.helper_data

    def plot_graph(self):
        f, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
        a0.plot(self.helper_data.iloc[:,0])
        a0.title.set_text("Adjusted Close")
        plt.setp(a0.xaxis.get_majorticklabels(), rotation=45)
        a1.plot(self.helper_data.iloc[:,1])
        a1.title.set_text("Momentum Indicator")
        a1.hlines(0, self.helper_data.index[0], self.helper_data.index[-1], linestyles="dotted")
        plt.setp(a1.xaxis.get_majorticklabels(), rotation=45)
        plt.legend()
        f.tight_layout()
        f.savefig("indicators/Momentum.png")	

class SMAIndicator(Indicator):
    def __init__(self, data, n=8):
        super().__init__(data)
        self.n = n

    def calculate_helper_data(self):
        num_days = self.data.shape[0]
        cols = ["Adjusted_Close", "SMA"]
        self.helper_data = pd.DataFrame(index=self.data.index, columns=cols)
        self.helper_data.iloc[:,0] = self.data
        self.helper_data.iloc[:,1] = self.data.rolling(window=self.n).mean()
        return self.helper_data

    def plot_graph(self):
        self.helper_data.plot()
        plt.title("Simple Moving Average Indicator")
        plt.savefig("indicators/SMA.png")	   
        plt.show()
        
class BollingerBandIndicator(Indicator):
    def __init__(self, data, n=20, k=2):
        super().__init__(data)
        self.n = n
        self.k = k
    
    def calculate_helper_data(self):
        num_days = self.data.shape[0]
        SMA = SMAIndicator(self.data, self.n).calculate_helper_data()
        cols = ["Adjusted_Close", "SMA", "bb_high", "bb_low"]
        self.helper_data = pd.DataFrame(index=self.data.index, columns=cols)
        self.helper_data.iloc[:,0:2] = SMA
        std = self.data.rolling(window=self.n).std()
        stdk = std * self.k
        self.helper_data.iloc[:,2] = self.helper_data.iloc[:,1] + stdk
        self.helper_data.iloc[:,3] = self.helper_data.iloc[:,1] - stdk
        return self.helper_data

    def plot_graph(self):
        self.helper_data.plot()
        plt.title("Bollinger Band Indicator")
        plt.savefig("indicators/BBI.png")	   
        plt.show()

class StochasticIndicator(Indicator):
    def __init__(self, data, n=14):
        # data need to contain high and low.
        super().__init__(data)
        self.n = n
    
    def calculate_helper_data(self):
        data = self.data.iloc[:,0]
        close = self.data.iloc[:,1]
        highest = self.data.iloc[:,2].rolling(window=self.n).max()
        lowest = self.data.iloc[:,3].rolling(window=self.n).min()
        osc = (close - lowest) / (highest - lowest) * 100
        #print(highest[-4], lowest[-4], self.data[-4])
        #print(osc)
        # num_days = self.data.shape[0]
        cols = ["Adjusted_Close", "Stochastic", "Fast Stochastic"]
        SMA_osc = SMAIndicator(osc, 3).calculate_helper_data()

        self.helper_data = pd.DataFrame(index=data.index, columns=cols)
        self.helper_data.iloc[:,0] = data
        self.helper_data.iloc[:,1] = osc
        self.helper_data.iloc[:,2] = SMA_osc.iloc[:,1]
        return self.helper_data

    def plot_graph(self):
        f, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
        a0.plot(self.helper_data.iloc[:,0])
        a0.title.set_text("Adjusted Close")
        plt.setp(a0.xaxis.get_majorticklabels(), rotation=45)
        a1.plot(self.helper_data.iloc[:,1], label="Stochastic")
        a1.plot(self.helper_data.iloc[:,2], label="Fast Stochastic")
        a1.hlines(80, self.helper_data.index[0], self.helper_data.index[-1], linestyles="dotted")
        a1.hlines(20, self.helper_data.index[0], self.helper_data.index[-1], linestyles="dotted")
        a1.title.set_text("Stochastic Indicator")
        plt.setp(a1.xaxis.get_majorticklabels(), rotation=45)
        plt.legend()
        f.tight_layout()
        f.savefig("indicators/SI.png")	   

def calculate(indicator: Indicator, visualize=False):
    helper_data = indicator.calculate_helper_data()
    if visualize:
        indicator.plot_graph()
    return helper_data

def normalize_data(data):
    return data / data[0]

def get_test_data():
    start_date = START_DATE
    end_date = END_DATE
    date_list = pd.date_range(start_date, end_date)
    datas = get_data([SYMBOL], date_list)[SYMBOL]
    datas = datas.fillna(method="ffill")
    datas = datas.fillna(method="bfill")
    datas = normalize_data(datas)
    return datas

def get_test_data_with_close_high_low():
    start_date = START_DATE
    end_date = END_DATE
    date_list = pd.date_range(start_date, end_date)
    d = get_data([SYMBOL], date_list)[SYMBOL]
    close = get_data([SYMBOL], date_list, colname="Close")[SYMBOL]
    high = get_data([SYMBOL], date_list, colname="High")[SYMBOL]
    low = get_data([SYMBOL], date_list, colname="Low")[SYMBOL]
    datas = pd.DataFrame(index=d.index, columns=["Adj Close", "Close", "High", "Low"])
    datas.iloc[:,0] = d
    datas.iloc[:,1] = close
    datas.iloc[:,2] = high
    datas.iloc[:,3] = low
    datas = datas.fillna(method="ffill")
    datas = datas.fillna(method="bfill")
    datas.iloc[:,0] = normalize_data(datas.iloc[:,0])
    return datas

def author():
    return "jkok7"

if __name__ == "__main__":
    START_DATE = dt.datetime(2008, 1, 1)
    END_DATE = dt.datetime(2010,1,1)
    SYMBOL = "JPM"
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()
    calculate(SMAIndicator(get_test_data()), True)
    calculate(MomentumIndicator(get_test_data()), True)
    calculate(BollingerBandIndicator(get_test_data()), True)
    calculate(StochasticIndicator(get_test_data_with_close_high_low()), True)