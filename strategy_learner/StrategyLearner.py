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
        start_date = sd
        end_date = ed
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
        
        # get indicator data
        indicator_m = MomentumIndicator(data.iloc[:,0], n=8).calculate_helper_data()
        indicator_bb = BollingerBandIndicator(data.iloc[:,0],20,2).calculate_helper_data()
        indicator_s = StochasticIndicator(data, 14).calculate_helper_data()

        # standardize features
        # for stochastic, instead of having a value from 0-100, make 0-10 = 1, 11-20 = 2 etc. 

        # initialize learner
        learner = QLearner(num_states=100, \
                            num_actions = 3, \
                            alpha = 0.2, \
                            gamma = 0.9, \
                            rar = 0.5, \
                            radr = 0.99, \
                            dyna = 0, \
                            verbose = False)
        

        # loop day by day
        # create variables for loop
        portfolio = pd.DataFrame(np.zeros((len(date_list), 1)), index = date_list)
        date_list = data.index 
        stock_shares = 0
        balance = sv
        commission = 0
        for day in date_list: 
            current_strtime = day.strftime('%Y-%m-%d') 
            # TODO: update state and reward accordingly
            state = 0
            reward = 0
            # Get action
            action = learner.query(state, reward)

            holdings = 0 # -1 for short, 0 for cash, 1 for long
            current_num_stocks = 0
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
            portfolio.loc[current_strtime] = balance + stock_value.sum()

  		   	  			  	 		  		  		    	 		 		   		 		  
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
        dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        trades = prices_all[[symbol,]]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
        trades.values[:,:] = 0 # set them all to nothing  		   	  			  	 		  		  		    	 		 		   		 		  
        trades.values[0,:] = 1000 # add a BUY at the start  		   	  			  	 		  		  		    	 		 		   		 		  
        trades.values[40,:] = -1000 # add a SELL  		   	  			  	 		  		  		    	 		 		   		 		  
        trades.values[41,:] = 1000 # add a BUY  		   	  			  	 		  		  		    	 		 		   		 		  
        trades.values[60,:] = -2000 # go short from long  		   	  			  	 		  		  		    	 		 		   		 		  
        trades.values[61,:] = 2000 # go long from short  		   	  			  	 		  		  		    	 		 		   		 		  
        trades.values[-1,:] = -1000 #exit on the last day  		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(type(trades)) # it better be a DataFrame!  		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(trades)  		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(prices_all)  		   	  			  	 		  		  		    	 		 		   		 		  
        return trades  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		   	  			  	 		  		  		    	 		 		   		 		  
