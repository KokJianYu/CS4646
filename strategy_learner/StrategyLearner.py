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

class StrategyLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # constructor  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			  	 		  		  		    	 		 		   		 		  
        self.impact = impact  		   	  			  	 		  		  		    	 		 		   		 		  


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
        price_diff = data.iloc[:,0].diff()
        momentums = np.digitize(indicator_m.iloc[:,1], self.bin_momentum)
        bb_diffs = np.digitize(indicator_bb.iloc[:,1] - indicator_bb.iloc[:,3], self.bin_bollinger)
        stochastics = np.digitize(indicator_s.iloc[:,1], self.bin_stochastic)
        price_features = np.digitize(price_diff, self.bin_price)

        # Set first 20 input to -1 as the algo requires 20 days to get started due to rolling window for bollinger band.
        momentums[:20] = -1
        bb_diffs[:20] = -1
        stochastics[:20] = -1
        price_features[:20] = -1
        # initialize learner
        num_states = self.getTotalNumberOfStates()
        self.learner = QLearner(num_states=num_states, \
                            num_actions = 3, \
                            alpha = 0.05, \
                            gamma = 0.9, \
                            rar = 0.99, \
                            radr = 0.999, \
                            dyna = 0, \
                            verbose = False)

        # loop day by day
        # create variables for loop
        date_list = data.index 
        iter = 0
        max_iter = 25
        while iter <= max_iter:
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
                        balance -= abs(order_num_of_shares) * current_symbol_price * self.impact

                # Update portfolio with balance and current stock worth
                stock_value = data.loc[current_strtime].iloc[0] * stock_shares
                total_value = balance + stock_value

                portfolio.loc[current_strtime] = total_value

            # current_ret = (portfolio.iloc[-1] / portfolio.iloc[0]).iloc[0]
            iter += 1	  			   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # this method should use the existing policy and test it against new data  		   	  			  	 		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):  		   	  			 

        data = self.getData(sd, ed, symbol)

        # get indicator data
        indicator_m = MomentumIndicator(data.iloc[:,0], n=8).calculate_helper_data()
        indicator_bb = BollingerBandIndicator(data.iloc[:,0],20,2).calculate_helper_data()
        indicator_s = StochasticIndicator(data, 14).calculate_helper_data()

        momentums = np.digitize(indicator_m.iloc[:,1], self.bin_momentum)
        bb_diffs = np.digitize(indicator_bb.iloc[:,1] - indicator_bb.iloc[:,3], self.bin_bollinger)
        stochastics = np.digitize(indicator_s.iloc[:,1], self.bin_stochastic)
        price_features = np.digitize(data.iloc[:,0].diff(), self.bin_price)

        # Set first 20 input to -1 as the algo requires 20 days to get started due to rolling window for bollinger band.
        momentums[:20] = -1
        bb_diffs[:20] = -1
        stochastics[:20] = -1
        price_features[:20] = -1

        trade_df = pd.DataFrame(index=data.index, columns=[symbol])
        current_holdings = 0
        action = 0
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
        # + 1 is for the state when some values are not yet calculated
        return 5*5*5*3*4 + 1

    # stochastic -> Value from 0-100
    # bollinger -> 3 Values. SMA + 2*STD, SMA and SMA - 2*STD
    # momentum -> value around -0.5 to 0.5
    # holding -> -1, 0 or 1
    # Col 0 is always adjusted close
    # Features starts from col 1
    def convertFeaturesToState(self, price, momentum, bollinger, stochastic, holding):  		   	  			  	 		  		  		    	 		 		   		 		  
        if np.isnan(momentum) or np.isnan(bollinger) or np.isnan(stochastic) or momentum == -1 or bollinger == -1 or stochastic == -1 or price == -1:
            return self.getTotalNumberOfStates() - 1
        
        # These values starts from 1. -1 to make it start from 0
        momentum -= 1
        bollinger -= 1
        stochastic -= 1
        price -= 1
        # Holding starts from -1, +1 to make it start from 0
        holding += 1
        return momentum + stochastic*5 + bollinger*25 + holding*125 + price*375
    def calculateReward(self, total_value, prev_day_order):
        try :
            return_val = (total_value - self.prev_total_value)
            self.prev_total_value = total_value
            return return_val
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


def generate_graphs():
    import experiment1
    import experiment2
    experiment1.generate_graphs()
    experiment2.generate_graphs()

def train_learner(qlearner):
    symbol = "JPM"
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)  			  	 		  		  		    	 		 		   		 		  
    qlearner.addEvidence(symbol, start_date, end_date, 100000)
    
if __name__=="__main__":  
    generate_graphs()		 
    print("One does not simply think up a strategy")  		   	  			  	 		  		  		    	 		 		   		 		  
