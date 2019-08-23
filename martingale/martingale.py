"""Assess a betting strategy.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
  		   	  			  	 		  		  		    	 		 		   		 		  
def author():  		   	  			  	 		  		  		    	 		 		   		 		  
        return 'jkok7' # replace tb34 with your Georgia Tech username.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def gtid():  		   	  			  	 		  		  		    	 		 		   		 		  
	return 903550380 # replace with your GT ID number  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		   	  			  	 		  		  		    	 		 		   		 		  
	result = False  		   	  			  	 		  		  		    	 		 		   		 		  
	if np.random.random() <= win_prob:  		   	  			  	 		  		  		    	 		 		   		 		  
		result = True  		   	  			  	 		  		  		    	 		 		   		 		  
	return result  		   	  			  	 		  		  		    	 		 		   		 		  

# episode_winnings = 0
# while episode_winnings < 80:
# 	won = False
# 	bet_amount = 1
# 	while not won:
# 		won = get_spin_result(win_prob)
# 		if won == True:
# 		episode_winnings = episode_winnings + bet_amount
# 		else:
# 		episode_winnings = episode_winnings - bet_amount
# 		bet_amount = bet_amount * 2					  	 		  		  		    	 		 		   		 		  
def test_code():  		   	  			  	 		  		  		    	 		 		   		 		  
	win_prob = 0.40 # set appropriately to the probability of a win  		   	  			  	 		  		  		    	 		 		   		 		  
	np.random.seed(gtid()) # do this only once

	# define variables  		  
	num_episodes = 10
	num_spins = 1000

	# Experiment 1 Figure 1
	# episode loop
	for episode in range(num_episodes): 	  	
		winnings = play_episode(win_prob, num_spins)
		plt.plot(winnings)

	save_plot("figure1.png")
	plt.close()

	# Experiment 1 Figure 2
	num_episodes = 1000
	mean_winnings = np.zeros((1001))
	all_winnings = np.zeros((num_episodes, 1001))
	for episode in range(num_episodes):
		winnings = play_episode(win_prob, num_spins)
		mean_winnings += winnings 
		all_winnings[episode] = winnings
	# TODO: calculate mean and std with all_winnings
	print(all_winnings)
	mean_winnings /= num_episodes
	plt.plot(mean_winnings)
	save_plot("figure2.png")
	plt.close()
	#print(list(mean_winnings))


  		   	  			  	 		  		  		    	 		 		   		 		  
	# add your code here to implement the experiments  		   	  			  	 		  		  		    	 		 		   		 		  

def save_plot(figure_name):
	plt.xlim([0, 300])
	plt.ylim([-256, 100])
	plt.savefig(figure_name)

def play_episode(win_prob, num_spins):
	winnings = np.zeros((1001)) # 0 is before first spin. 
	bet = 1
	# spin loop
	for i in range(num_spins):
		if winnings[i] >= 80:
			winnings[(i+1):] = winnings[i] 
			break
		won = get_spin_result(win_prob)
		if won:
			winnings[i+1] = winnings[i] + bet
			bet = 1
		else:
			winnings[i+1] = winnings[i] - bet
			bet = bet*2
	return winnings


if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    test_code()  		   	  			  	 		  		  		    	 		 		   		 		  
