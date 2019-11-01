CS4646/7646 Project 6 Manual Strategy 

Running instructions:

I have implemented Indicator as a class. 
To use an indicator, create the Indicator object with the data and required variables. 
After that, you will be able to call `Indicator.calculate_helper_data()` to retrieve the values calculated by the indicators.
After calling `Indicator.calculate_helper_data()`, `Indicator.plot_graph()` can then be called to generate a graph for the calculated indicator values.

To use a strategy, simply import the Strategy, and run it by calling Strategy.testPolicy()

To generate all charts of indicators with default dataset, run command "python indicators.py". 

To generate charts of Theoretical and Manual Strategy with default dataset, run command "python marketsim.py".

The dataset can be modified by changing the variables in __main__ in 'indicator.py' and 'marketsim.py'
