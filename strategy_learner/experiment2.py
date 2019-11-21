from ManualStrategy import BenchmarkStrategy, ManualStrategy
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals_df, calculate_daily_returns

import datetime as dt  	
import pandas as pd 
import numpy as np
import random as rand
import matplotlib.pyplot as plt

def generate_graphs():
    impacts = [0.000, 0.001, 0.003, 0.005]
    for impact in impacts:
        np.random.seed(5)
        rand.seed(5)
        learner = StrategyLearner(impact=impact)
        train_learner(learner)
        in_pv1, in_pv2 = runSimulation(ManualStrategy(), learner, f"experiment2_{impact}.png",True, impact=impact)

def train_learner(qlearner):
    symbol = "JPM"
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)  			  	 		  		  		    	 		 		   		 		  
    qlearner.addEvidence(symbol, start_date, end_date, 100000)


def runSimulation(Strategy1, Strategy2, fileName, plot_entry_points=False,in_sample=True, impact = 0):
    import matplotlib.pyplot as plt
    symbol = "JPM"
    if in_sample:
        start_date = dt.datetime(2008,1,1)
        end_date = dt.datetime(2009,12,31)
    else:
        start_date = dt.datetime(2010,1,1)
        end_date = dt.datetime(2011,12,31)
    pv1, sharpe_ratio, cum_ret, std_daily_ret, avg_daily_ret, trades1 = test_code_df(Strategy1,symbol, start_date=start_date ,end_date=end_date,commission=0, impact=impact)
    pv2, sharpe_ratio, cum_ret, std_daily_ret, avg_daily_ret, trades2 = test_code_df(Strategy2,symbol,start_date=start_date ,end_date=end_date,commission=0, impact=impact)
    #pv2, cum_ret, std_daily_ret, avg_daily_ret = test_code_df(ManualStrategy())
    pv1 = pv1/pv1[0]
    pv2 = pv2/pv2[0]
    pv1.plot(label=Strategy1.getStrategyName(), color="red")
    pv2.plot(label=Strategy2.getStrategyName(), color="green")
    if plot_entry_points:
        holdings = 0
        # for day in trades1.index:
        #     holdings += trades1.loc[day]
        #     if (holdings == 1000).all() and (trades1.loc[day] > 0).all():
        #         plt.vlines(day, pv1.loc[day], pv1.loc[day]+0.2, color="blue")
        #     if (holdings == -1000).all() and (trades1.loc[day] < 0).all():
        #         plt.vlines(day, pv1.loc[day]-0.2, pv1.loc[day], color="black")
        num_trades = 0
        for day in trades2.index:
            holdings += trades2.loc[day]
            if (holdings == 1000).all() and (trades2.loc[day] > 0).all():
                num_trades += 1
                plt.vlines(day, pv2.loc[day], pv2.loc[day]+0.2, color="blue")
            if (holdings == -1000).all() and (trades2.loc[day] < 0).all():
                num_trades += 1
                plt.vlines(day, pv2.loc[day]-0.2, pv2.loc[day], color="black")

    # Generate table in graph
    row_labels=['Number of trades','Cumulative Return','Sharpe Ratio']
    table_vals=[[num_trades],[round(cum_ret,3)],[round(sharpe_ratio,3)]]
    plt.table(cellText=table_vals,
                    colWidths = [0.1]*3,
                    rowLabels=row_labels,
                    loc='upper left', bbox=[0.35, 0.75, 0.1, 0.2])

    plt.legend(loc="upper right")
    if in_sample:
        plt.title(f"In-Sample, Impact = {impact}")
    else:
        plt.title("Out-Of-Sample")
    plt.savefig(fileName)
    plt.close()
    return pv1[-1], pv2[-1]

def test_code_df(Strategy, symbol="JPM", start_date= dt.datetime(2008,1,1), end_date=dt.datetime(2010,1,1), start_value=100000, commission=0, impact=0, verbose=False):  		   	  			  	 		  		  		    	 		 		   		 		  
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

    if verbose:
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

    return portvals, sharpe_ratio, cum_ret, std_daily_ret, avg_daily_ret, of

def author():
    return "jkok7"

if __name__=="__main__":  
    generate_graphs()
