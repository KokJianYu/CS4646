"""MC2-P1: Market simulator.  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
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
                                                                                                                  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import os  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):  		   	  			  	 		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		   	  			  	 		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			  	 		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		   	  			  	 		  		  		    	 		 		   		 		  
    # TODO: Your code here  

    orders = pd.read_csv(orders_file)

    # Get list of dates.
    unique_dates = orders["Date"].unique().tolist()
    unique_dates.sort()
    start_date = dt.datetime.strptime(unique_dates[0], '%Y-%m-%d')  		   	  			  	 		  		  		    	 		 		   		 		  
    end_date = dt.datetime.strptime(unique_dates[-1], '%Y-%m-%d')
    date_list = pd.date_range(start_date, end_date)

    # Get all unique symbols.
    unique_symbols = orders["Symbol"].unique().tolist()  	 		  		  		    	 		 		   		 		  

    # Initialize starting balance and stocks
    balance = start_val
    stock_shares = pd.DataFrame(np.zeros((len(unique_symbols), 1)), index = unique_symbols)
                                                                                                                  
    # Get data from start to end date.	   	  			  	 		  		  		    	 		 		   		 		  
    datas = get_data(unique_symbols, date_list)  		   	  			  	 		  		  		    	 		 		   		 		  
    datas = datas[unique_symbols]  # remove SPY 
    date_list = datas.index 		   	  			  	 				   	  			  	 		  		  		    	 		 		   		 		  	  	 		  		  		    	 		 		   		 		  
    # Remove unfulfilled orders, orders that are made when market is closed.
    orders = orders[orders["Date"].isin(datas.index.strftime('%Y-%m-%d'))]
    portfolio = pd.DataFrame(np.zeros((len(date_list), 1)), index = date_list)
    
    datas = datas.fillna(method="ffill")
    datas = datas.fillna(method="bfill")
    for day in date_list: 
        current_strtime = day.strftime('%Y-%m-%d') 
        orders_today = orders[orders["Date"] == current_strtime]
        # If there are orders
        if orders_today.shape[0] != 0:
            for i in range(orders_today.shape[0]):
                # get order details
                current_order = orders_today.iloc[i]
                order_type = current_order["Order"]
                order_num_of_shares = current_order["Shares"]
                order_symbol = current_order["Symbol"]
                current_symbol_price = datas.loc[current_strtime, order_symbol]
                order_type_multiplier = 0
                # if sell, add to balance. if buy, reduce from balance
                if order_type == "BUY":
                    order_type_multiplier = -1
                else: 
                    order_type_multiplier = 1
                # execute order 66
                balance += order_type_multiplier * order_num_of_shares * current_symbol_price
                stock_shares.loc[order_symbol] += -1 * order_type_multiplier * order_num_of_shares

                # Minus commission
                balance -= commission

                # Minus impact
                balance -= order_num_of_shares * current_symbol_price * impact



        # Update portfolio with balance and current stock worth
        stock_value = datas.loc[current_strtime, unique_symbols] * stock_shares.transpose()[unique_symbols]
        portfolio.loc[current_strtime] = balance + stock_value.sum(axis=1)
   	   	  			  	 		  		  		    	 		 		   		 		  
    return portfolio  		   	  			  	 		  		  		    	 		 		   		 		  


def compute_portvals_df(orders, symbol,start_date,end_date, start_val = 1000000, commission=9.95, impact=0.005):  		   	  			  	 		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		   	  			  	 		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			  	 		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		   	  			  	 		  		  		    	 		 		   		 		  
    # TODO: Your code here  

    # Get list of dates.
    # unique_dates = orders.index.unique().tolist()
    # unique_dates.sort()
    # start_date = unique_dates[0]
    # end_date = unique_dates[-1]
    date_list = pd.date_range(start_date, end_date)
	 		  		  		    	 		 		   		 		  

    # Initialize starting balance and stocks
    balance = start_val
    stock_shares = 0
                                                                                                                  
    # Get data from start to end date.	   	  			  	 		  		  		    	 		 		   		 		  
    datas = get_data([symbol], date_list)  		   	  			  	 		  		  		    	 		 		   		 		  
    datas = datas[symbol]  # remove SPY 
    date_list = datas.index 		   	  			  	 				   	  			  	 		  		  		    	 		 		   		 		  	  	 		  		  		    	 		 		   		 		  
    # Remove unfulfilled orders, orders that are made when market is closed.
    orders = orders[orders.index.isin(datas.index)]
    portfolio = pd.DataFrame(np.zeros((len(date_list), 1)), index = date_list)
    
    datas = datas.fillna(method="ffill")
    datas = datas.fillna(method="bfill")
    for day in date_list: 
        current_strtime = day.strftime('%Y-%m-%d') 
        try:
            orders_today = orders.loc[day]
        except KeyError:
            orders_today = None
        # If there are orders
        if orders_today is not None and orders_today.shape[0] != 0:
            for i in range(orders_today.shape[0]):
                # get order details
                order_num_of_shares = orders_today.iloc[i]
                current_symbol_price = datas[day]
                
                balance += -1 * order_num_of_shares * current_symbol_price
                stock_shares += order_num_of_shares
                # Minus commission
                if order_num_of_shares != 0:
                    balance -= commission


                # Minus impact
                balance -= order_num_of_shares * current_symbol_price * impact
        # Update portfolio with balance and current stock worth
        stock_value = datas[current_strtime] * stock_shares
        portfolio.loc[current_strtime] = balance + stock_value.sum()
   	   	  			  	 		  		  		    	 		 		   		 		  
    return portfolio  		   	  	
	   	  			  	 		  		  		    	 		 		   		 		  

def test_code_df(Strategy, symbol="JPM", start_date= dt.datetime(2008,1,1), end_date=dt.datetime(2010,1,1), start_value=100000, commission=0, impact=0):  		   	  			  	 		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		   	  			  	 		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			  	 		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			  	 		  		  		    	 		 		   		 		  	
    of = Strategy.testPolicy(symbol = symbol, sd=start_date, ed=end_date, sv = start_value)                                                                                                        
    #of = "./orders/orders2.csv"  		   	  			  	 		  		  		    	 		 		   		 		  
    sv = 100000  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # Process orders  		  Momentum 	  			  	 		  		  		    	 		 		   		 		  
    portvals = compute_portvals_df(of, symbol, start_date, end_date, start_value, commission,impact)
    if isinstance(portvals, pd.DataFrame):  		   	  			  	 		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]] # just get the first column  		   	  			  	 		  		  		    	 		 		   		 		  
    else:  		   	  			  	 		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # Get portfolio stats  		   	  			  	 		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		   	  			  	 		  		  		    	 		 		   		 		  
    portfolio_dr = calculate_daily_returns(portvals)
    cum_ret = portvals[-1] / portvals[0] - 1
    avg_daily_ret = portfolio_dr.mean()
    std_daily_ret = portfolio_dr.std()
    sharpe_ratio = np.sqrt(252) * avg_daily_ret / std_daily_ret

    # Compare portfolio against $SPX  
    print("################################################################################")
    print(f"Results for {Strategy.getStrategyName()}:" )		   	  			  	 		  		  		    	 		 		   		 		  
    print()
    print(f"Date Range: {start_date} to {end_date}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  	  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  	 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Final Portfolio Value: {portvals[-1]}")

    return portvals, cum_ret, std_daily_ret, avg_daily_ret, of

def calculate_daily_returns(portfolio):
    df_portfolio = portfolio.copy()
    portfolio_dr = df_portfolio.pct_change(1).fillna(0)
    return portfolio_dr

def author():
    return "jkok7"

def runSimulation(Strategy1, Strategy2, fileName, plot_entry_points=False,in_sample=True):
    import matplotlib.pyplot as plt
    symbol = "JPM"
    if in_sample:
        start_date = dt.datetime(2008,1,1)
        end_date = dt.datetime(2009,12,31)
    else:
        start_date = dt.datetime(2010,1,1)
        end_date = dt.datetime(2011,12,31)
    pv1, cum_ret, std_daily_ret, avg_daily_ret, trades1 = test_code_df(Strategy1,symbol, start_date=start_date ,end_date=end_date,commission=0, impact=0)
    pv2, cum_ret, std_daily_ret, avg_daily_ret, trades2 = test_code_df(Strategy2,symbol,start_date=start_date ,end_date=end_date)
    #pv2, cum_ret, std_daily_ret, avg_daily_ret = test_code_df(ManualStrategy())
    pv1 = pv1/pv1[0]
    pv2 = pv2/pv2[0]
    # pv1.plot(label=Strategy1.getStrategyName(), color="red")
    # pv2.plot(label=Strategy2.getStrategyName(), color="green")
    # if plot_entry_points:
    #     holdings = 0
    #     for day in trades1.index:
    #         holdings += trades1.loc[day]
    #         if (holdings == 1000).all() and (trades1.loc[day] > 0).all():
    #             plt.vlines(day, pv1.loc[day], pv1.loc[day]+0.2, color="blue")
    #         if (holdings == -1000).all() and (trades1.loc[day] < 0).all():
    #             plt.vlines(day, pv1.loc[day]-0.2, pv1.loc[day], color="black")
    # plt.legend()
    # if in_sample:
    #     plt.title("In-Sample")
    # else:
    #     plt.title("Out-Of-Sample")
    # plt.savefig(fileName)
    # plt.close()
    return pv1[-1], pv2[-1]
