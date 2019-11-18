"""  		   	  			  	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			  	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			  	 		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
Template code for CS 4646/7646  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			  	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			  	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			  	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			  	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			  	 		  		  		    	 		 		   		 		  
or edited.  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
We do grant permission to share solutions privately with non-students such  		   	  			  	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			  	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			  	 		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
-----do not edit anything above this line---  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
Student Name: Kok Jian Yu (replace with your name)  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jkok7 (replace with your User ID)  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903550380 (replace with your GT ID)  		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import util as ut  
import numpy as np		   	  			  	 		  		  		    	 		 		   		 		  
import random  		   
from indicators import MomentumIndicator, BollingerBandIndicator, StochasticIndicator 			  	 		  		  		    	 		 		   		 		  
from QLearner import QLearner

# For profiling. TODO: Remove before submission
import time
# t0 = time.clock()
# t1 = time.clock()

# total = t1-t0

class StrategyLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # constructor  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			  	 		  		  		    	 		 		   		 		  
        self.impact = impact  		   	  			  	 		  		  		    	 		 		   		 		  

    def set_hyper_params(self, alpha=0.001, gamma=0.9, rar=0.99, radr=0.999):
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr


    # this method should create a QLearner, and train it for trading  		   	  			  	 		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
        # add your code to do learning here  
        # get data
        data = self.getData(sd, ed, symbol)
        
        # get indicator data
        indicator_m = MomentumIndicator(data.iloc[:,0], n=8).calculate_helper_data()
        indicator_bb = BollingerBandIndicator(data.iloc[:,0],20,2).calculate_helper_data()
        indicator_s = StochasticIndicator(data, 14).calculate_helper_data()
        
        # Get bins
        self.bin_momentum = pd.qcut(indicator_m.iloc[:,1], 4, retbins=True, duplicates="drop")[1]
        self.bin_bollinger = pd.qcut(indicator_bb.iloc[:,1] - indicator_bb.iloc[:,3], 4, retbins=True, duplicates="drop")[1]
        self.bin_stochastic = pd.qcut(indicator_s.iloc[:,1], 4, retbins=True, duplicates="drop")[1]
        self.bin_price = pd.qcut(data.iloc[:,0].diff(periods=1), 3, retbins=True, duplicates="drop")[1]

        momentums = np.digitize(indicator_m.iloc[:,1], self.bin_momentum)
        bb_diffs = np.digitize(indicator_bb.iloc[:,1] - indicator_bb.iloc[:,3], self.bin_bollinger)
        stochastics = np.digitize(indicator_s.iloc[:,1], self.bin_stochastic)
        price_features = np.digitize(data.iloc[:,0].diff(), self.bin_price)
        # initialize learner
        num_states = self.getTotalNumberOfStates()
        # self.learner = QLearner(num_states=num_states, \
        #                     num_actions = 3, \
        #                     alpha = 0.02, \
        #                     gamma = 0.9, \
        #                     rar = 0.99, \
        #                     radr = 0.999, \
        #                     dyna = 0, \
        #                     verbose = False)
        self.learner = QLearner(num_states=num_states, \
                    num_actions = 3, \
                    alpha = self.alpha, \
                    gamma = self.gamma, \
                    rar = self.rar, \
                    radr = self.radr, \
                    dyna = 0, \
                    verbose = False)

        # loop day by day
        # create variables for loop
        date_list = data.index 
        iter = 0
        max_iter = 30
        prev_ret = float("-inf")
        d = data.iloc[:,0]
        while iter <= max_iter:
            print(f"iter:{iter}")

            portfolio = pd.DataFrame(np.zeros((len(date_list), 1)), index = date_list)
            stock_shares = 0
            balance = sv
            total_value = sv
            commission = 0
            holdings = 0 # -1 for short, 0 for cash, 1 for long
            current_num_stocks = 0
            order = 0
            for i,day in enumerate(date_list): 
                
                current_strtime = day.strftime('%Y-%m-%d') 
                # TODO: update state and reward accordingly
                if i == 0:
                    price_feature = 0
                else:
                    price_feature = price_features[i]

            
                holdings = current_num_stocks // 1000
                #state = self.convertFeaturesToState(price_feature, indicator_m.loc[current_strtime], indicator_bb.loc[current_strtime], indicator_s.loc[current_strtime], holdings)
                state = self.convertFeaturesToState(price_feature, momentums[i], bb_diffs[i], stochastics[i], holdings)
                reward = self.calculateReward(total_value, order)
                # Get action
                action = self.learner.query(state, reward) - 1
                order = 0
                if holdings != action:
                    # long
                    if action == 1:
                        order = 1000 - current_num_stocks
                        current_num_stocks = 1000
                    # short
                    elif action == -1:
                        order = -1000 - current_num_stocks
                        current_num_stocks = -1000
                    # do nothing
                    elif action == 0:
                        order = 0 - current_num_stocks
                        current_num_stocks = 0
                # If there are order
                if order != 0:
                    
                    # get order details
                    order_num_of_shares = order
                    current_symbol_price = data.loc[current_strtime].iloc[0]
                    
                    balance += -1 * order_num_of_shares * current_symbol_price
                    stock_shares += order_num_of_shares
                    # Minus commission
                    if order_num_of_shares != 0:
                        balance -= commission
                    # Minus impact
                    balance -= order_num_of_shares * current_symbol_price * self.impact

                # Update portfolio with balance and current stock worth
                stock_value = data.loc[current_strtime].iloc[0] * stock_shares
                total_value = balance + stock_value

                portfolio.loc[current_strtime] = total_value


                
            current_ret = (portfolio.iloc[-1] / portfolio.iloc[0]).iloc[0]
            print(current_ret)
            # TODO: Add logic to stop training if current_ret not increasing.
            # if abs(prev_ret - (current_ret)) < 1e-3 and self.learner.epsilon < 0.05:
                # break
                # self.best_q_table = self.learner.q_table.copy()
                # print("save best")

            prev_ret = current_ret
            iter += 1	  		
        #self.learner.q_table = self.best_q_table
        # # example usage of the old backward compatible util function  		   	  			  	 		  		  		    	 		 		   		 		  
        # syms=[symbol]  		   	  			  	 		  		  		    	 		 		   		 		  
        # dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
        # prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        # prices = prices_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
        # prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
        # if self.verbose: print(prices)  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
        # # example use with new colname  		   	  			  	 		  		  		    	 		 		   		 		  
        # volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        # volume = volume_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
        # volume_SPY = volume_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
        # if self.verbose: print(volume)  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # this method should use the existing policy and test it against new data  		   	  			  	 		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
        # here we build a fake set of trades  		   	  			  	 		  		  		    	 		 		   		 		  
        # your code should return the same sort of data  		   	  			  	 		  		  		    	 		 		   		 		  
        # dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
        # prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades = prices_all[[symbol,]]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[:,:] = 0 # set them all to nothing  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[0,:] = 1000 # add a BUY at the start  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[40,:] = -1000 # add a SELL  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[41,:] = 1000 # add a BUY  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[60,:] = -2000 # go short from long  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[61,:] = 2000 # go long from short  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[-1,:] = -1000 #exit on the last day  		   


        data = self.getData(sd, ed, symbol)

        # get indicator data
        indicator_m = MomentumIndicator(data.iloc[:,0], n=8).calculate_helper_data()
        indicator_bb = BollingerBandIndicator(data.iloc[:,0],20,2).calculate_helper_data()
        indicator_s = StochasticIndicator(data, 14).calculate_helper_data()

        momentums = np.digitize(indicator_m.iloc[:,1], self.bin_momentum)
        bb_diffs = np.digitize(indicator_bb.iloc[:,1] - indicator_bb.iloc[:,3], self.bin_bollinger)
        stochastics = np.digitize(indicator_s.iloc[:,1], self.bin_stochastic)
        price_features = np.digitize(data.iloc[:,0].diff(), self.bin_price)

        trade_df = pd.DataFrame(index=data.index, columns=[symbol])
        current_holdings = 0
        action = 0
        d = data.iloc[:, 0]
        for i in range(data.shape[0]):
            if i == 0:
                price_feature = 0
            else:
                price_feature = price_features[i]

            #state = self.convertFeaturesToState(price_feature, indicator_m.iloc[i],indicator_bb.iloc[i],indicator_s.iloc[i],current_holdings // 1000)
            state = self.convertFeaturesToState(price_feature, momentums[i],bb_diffs[i],stochastics[i],current_holdings // 1000)
            action = self.learner.querysetstate(state) - 1
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
        # return trade_df
        if self.verbose: print(type(trade_df)) # it better be a DataFrame!  		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(trade_df)  		   	  			  	 		  		  		    	 		 		   		 		  
        #if self.verbose: print(prices_all)  		   	  			  	 		  		  		    	 		 		   		 		  
        return trade_df

    def getTotalNumberOfStates(self):
        return 1875

    # stochastic -> Value from 0-100
    # bollinger -> 3 Values. SMA + 2*STD, SMA and SMA - 2*STD
    # momentum -> value around -0.5 to 0.5
    # holding -> -1, 0 or 1
    # Col 0 is always adjusted close
    # Features starts from col 1
    def convertFeaturesToState(self, price, momentum, bollinger, stochastic, holding):  		   	  			  	 		  		  		    	 		 		   		 		  
        if np.isnan(momentum) or np.isnan(bollinger) or np.isnan(stochastic) or momentum == len(self.bin_momentum) or bollinger == len(self.bin_bollinger) or stochastic == len(self.bin_stochastic):
            return 0
        # price = min(-2, price)
        # price = max(2, price)
        # price += 2
        # momentum = int((momentum[1] + 1)/2 * 5) # 0 to 5
        # stochastic = int(stochastic[1] / 100 * 5) # 0 to 5
        holding += 1 # 3 possible value
        #print(bollinger[1] - bollinger[3])
        # bb_1 = int(max(5, (bollinger[1] - bollinger[3]) / 2))
        # momentum = np.digitize([momentum[1]], self.bin_momentum)
        # stochastic = np.digitize([stochastic[1]], self.bin_bollinger)
        # bb_1 = np.digitize([bollinger[1] - bollinger[3]], self.bin_stochastic)
        return momentum + stochastic*5 + bollinger*25 + holding*125 + price*375
        #return momentum*150 + bb_1*25+ holding*5 + price
        #print(price, momentum, bollinger, stochastic, holding)

    def calculateReward(self, total_value, prev_day_order):
        try :
            return_val = (total_value - self.prev_total_value)
            self.prev_total_value = total_value
            return return_val - prev_day_order*self.impact
        except AttributeError:
            self.prev_total_value = total_value

        return 0
    
    def getData(self, start_date, end_date, symbol):
        date_list = pd.date_range(start_date, end_date)
        d = ut.get_data([symbol], date_list)[symbol]
        close = ut.get_data([symbol], date_list, colname="Close")[symbol]
        high = ut.get_data([symbol], date_list, colname="High")[symbol]
        low = ut.get_data([symbol], date_list, colname="Low")[symbol]
        data = pd.DataFrame(index=d.index, columns=["Adj Close", "Close", "High", "Low"])
        data.iloc[:,0] = d
        data.iloc[:,1] = close
        data.iloc[:,2] = high
        data.iloc[:,3] = low
        data = data.fillna(method="ffill")
        data = data.fillna(method="bfill")
        return data
    
    # This method is to fulfill inheritance requirement for strategy
    def getStrategyName(self):
        return "Q Learning Strategy"


# Code below to generate graphs
def generate_graphs():
    from marketsim import runSimulation
    from ManualStrategy import ManualStrategy, BenchmarkStrategy
    alpha = [3, 1, 0.3, 0.1, 0.01, 0.03 , 0.001, 0.003, 0.0001, 0.0003] 
    gamma = [0.99, 0.9, 0.8, 0.7]
    rar = [0.8, 0.9, 0.99, 0.999]
    radr = [0.8, 0.9, 0.99, 0.999]
    best_params_in = []
    best_params_out = []
    best_in = 0
    best_out = 0
    for a in alpha:
        for g in gamma:
            for r in rar:
                for r2 in radr:
                    avg_in_pv1 = 0
                    avg_in_pv2 = 0
                    avg_out_pv1 = 0
                    avg_out_pv2 = 0
                    for i in range(5):
                        learner = StrategyLearner()
                        learner.set_hyper_params(a, g, r, r2)
                        train_learner(learner)
                        in_pv1, in_pv2 = runSimulation(ManualStrategy(), learner, "manual_insample.png",True)
                        out_pv1, out_pv2 = runSimulation(ManualStrategy(), learner, "manual_outofsample.png",True, False)
                        avg_in_pv1 += in_pv1 / 5
                        avg_in_pv2 += in_pv2 / 5
                        avg_out_pv1 += out_pv1 / 5
                        avg_out_pv2 += out_pv2 / 5

                    with open("output.txt", "a+") as f:
                        f.write(f"Hyper Params: alpha={a} gamma={g} rar={r} radr={r2}\n")
                        f.write(f"In Sample: Manual:{avg_in_pv1} Learner:{avg_in_pv2}\n")
                        f.write(f"Out Sample: Manual:{avg_out_pv1} Learner:{avg_out_pv2}\n")
                        f.write(f"\n")
                    if best_in < avg_in_pv2:
                        best_in = avg_in_pv2
                        best_params_in = [a, g, r, r2]
                    if best_out < avg_out_pv2:
                        best_out = avg_out_pv2
                        best_params_out = [a, g, r, r2]
    
    print("Best Parameters:")
    print("In Sample")
    print(f"Alpha:{best_params_in[0]} Gamma:{best_params_in[1]} rar:{best_params_in[2]} radr:{best_params_in[3]}")
    print("Out Sample")
    print(f"Alpha:{best_params_out[0]} Gamma:{best_params_out[1]} rar:{best_params_out[2]} radr:{best_params_out[3]}")
                        

def train_learner(qlearner):
    symbol = "JPM"
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)  			  	 		  		  		    	 		 		   		 		  
    qlearner.addEvidence(symbol, start_date, end_date, 100000)
    
if __name__=="__main__":  
    generate_graphs()		 
    print("One does not simply think up a strategy")  		   	  			  	 		  		  		    	 		 		   		 		  
