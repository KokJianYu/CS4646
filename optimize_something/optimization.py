"""MC1-P2: Optimize a portfolio.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
  		   	  			  	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		
import scipy.optimize as spo   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			  	 		  		  		    	 		 		   		 		  


def f(allocs, *args):
    prices = args[0].copy()
    portfolio = calculate_portfolio(prices, allocs)
    portfolio_dr = calculate_daily_returns(portfolio)
    adr = portfolio_dr.mean()
    sddr = portfolio_dr.std()
    sr = np.sqrt(252) * adr / sddr
    return -sr

def calculate_portfolio(prices, allocs):
    df = prices.copy()
    if len(df.shape) > 1:
        df = df.div(df.iloc[0,:])
        df *= allocs
        portfolio = df.sum(axis=1)
    else:
        portfolio = df.div(df.iloc[0])

    return portfolio

def calculate_daily_returns(portfolio):
    df_portfolio = portfolio.copy()
    portfolio_dr = portfolio.pct_change(1).fillna(0)
    return portfolio_dr
 		  		  		    	 		 		   		 		  
# This is the function that will be tested by the autograder  		   	  			  	 		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		   	  			  	 		  		  		    	 		 		   		 		  
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # Read in adjusted closing prices for given symbols, date range  		   	  			  	 		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # find the allocations for the optimal portfolio  		   	  			  	 		  		  		    	 		 		   		 		  
    # note that the values here ARE NOT meant to be correct for a test case  	
    n = len(syms)
    allocs = []
    allocs_bound=[]
    for i in range(n):
        allocs.append(1/n)
        allocs_bound.append((0,1))
    #allocs = np.asarray([0.1, 0.2, 0.1, 0.3, 0.3]) # add code here to find the allocations  		   	  			  	 		  		  		    	 		 		   		 		  
    
    #optimize
    min_result = spo.minimize(f, allocs, (prices), method="SLSQP", options={'disp':True}, bounds=allocs_bound , constraints= ({ 'type': 'eq', 'fun': lambda inputs: 1 - np.sum(inputs) }))
    allocs = min_result["x"]
    # calculate portfolio
    portfolio = calculate_portfolio(prices, allocs)
    portfolio_dr = calculate_daily_returns(portfolio)
    cr = portfolio[-1] / portfolio[0] - 1
    adr = portfolio_dr.mean()
    sddr = portfolio_dr.std()
    sr = np.sqrt(252) * adr / sddr

    # cr, adr, sddr, sr = [portfolio.iloc[-1], portfolio_dr.mean(), portfolio_dr.std(), 2.1] # add code here to compute stats  		   	  			  	 		  		  		    	 		 		   		 		  

    # Get daily portfolio value  		   	  			  	 		  		  		    	 		 		   		 		  
    port_val = portfolio_dr # add code here to compute daily portfolio values  		   	  			  	 		  		  		    	 		 		   		 		  
    prices_SPY_normalized = prices_SPY.div(prices_SPY.iloc[0])
    # Compare daily portfolio value with SPY using a normalized plot  		   	  			  	 		  		  		    	 		 		   		 		  
    if gen_plot:  		   	  			  	 		  		  		    	 		 		   		 		  
        # add code to plot here  		   	  			  	 		  		  		    	 		 		   		 		  
        df_temp = pd.concat([portfolio, prices_SPY_normalized], keys=['Portfolio', 'SPY'], axis=1)  		   	  			  	 		  		  		    	 		 		   		 		  
        ax = df_temp.plot(title="Daily Portfolio value and SPY")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.savefig("1.png")
        pass  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    return allocs, cr, adr, sddr, sr  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def test_code():  		   	  			  	 		  		  		    	 		 		   		 		  
    # This function WILL NOT be called by the auto grader  		   	  			  	 		  		  		    	 		 		   		 		  
    # Do not assume that any variables defined here are available to your function/code  		   	  			  	 		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			  	 		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		   	  			  	 		  		  		    	 		 		   		 		  
    # the autograder!  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,6,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2009,6,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    symbols =  ['IBM', 'X', 'GLD', 'JPM']
    # Assess the portfolio  		   	  			  	 		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # Print statistics  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Start Date: {start_date}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"End Date: {end_date}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Symbols: {symbols}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Allocations:{allocations}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio: {sr}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Volatility (stdev of daily returns): {sddr}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return: {adr}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return: {cr}")  		   	  			  	 		  		  		    	 		 		   		 		  

def str2dt(strng):  		   	  			  	 		  		  		    	 		 		   		 		  
    year,month,day = map(int,strng.split('-'))  		   	  			  	 		  		  		    	 		 		   		 		  
    return dt.datetime(year,month,day)  	

if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		   	  			  	 		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			  	 		  		  		    	 		 		   		 		  
    test_code()  		   	  			  	 		  		  		    	 		 		   		 		  
