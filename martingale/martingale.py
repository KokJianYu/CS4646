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

			  	 		  		  		    	 		 		   		 		  
def test_code():  	
	# in america wheel, there are 38 holes, 2 green. 
	# therefore, chance of winning given that we bet red or black
	# is 18/38	   	  			  	 		  		  		    	 		 		   		 		  
	win_prob = 18/38 # set appropriately to the probability of a win  		   	  			  	 		  		  		    	 		 		   		 		  
	np.random.seed(gtid()) # do this only once

	# define variables  		  
	num_episodes = 10
	num_spins = 1000

	# Experiment 1 Figure 1
	# episode loop
	for episode in range(num_episodes): 	  	
		winnings = play_episode(win_prob, num_spins)
		plt.plot(winnings, label="simulation_{}".format(episode+1))
	plt.title("Figure 1")
	plt.xlabel("Spins")
	plt.ylabel("Winnings")
	plt.legend()
	save_plot("figure1.png")
	plt.close()

	# Experiment 1 Figure 2
	num_episodes = 1000
	all_winnings = np.zeros((num_episodes, 1001))
	for episode in range(num_episodes):
		winnings = play_episode(win_prob, num_spins)
		all_winnings[episode] = winnings
	mean_winnings = all_winnings.mean(axis=0)
	std_winnings = all_winnings.std(axis=0)
	plt.plot(mean_winnings, label="mean")
	plt.plot(mean_winnings + std_winnings, label="mean + std")
	plt.plot(mean_winnings - std_winnings, label="mean - std")
	plt.title("Figure 2")
	plt.xlabel("Spins")
	plt.ylabel("Winnings")
	plt.legend()
	save_plot("figure2.png")
	plt.close()

	# Experiment 1 Figure 3
	# utilizing all_winnings from experiment 1 figure 2
	median_winnings = np.median(all_winnings, axis=0)
	std_winnings = all_winnings.std(axis=0)
	plt.plot(median_winnings, label="median")
	plt.plot(median_winnings + std_winnings, label="median + std")
	plt.plot(median_winnings - std_winnings, label="median - std")
	plt.title("Figure 3")
	plt.xlabel("Spins")
	plt.ylabel("Winnings")
	plt.legend()
	save_plot("figure3.png")
	plt.close()

	# Experiment 2 Figure 4
	num_episodes = 1000
	all_winnings = np.zeros((num_episodes, 1001))
	for episode in range(num_episodes):
		winnings = play_episode_256_bankroll(win_prob, num_spins)
		all_winnings[episode] = winnings
	mean_winnings = all_winnings.mean(axis=0)
	std_winnings = all_winnings.std(axis=0)
	plt.plot(mean_winnings, label="mean")
	plt.plot(mean_winnings + std_winnings, label="mean + std")
	plt.plot(mean_winnings - std_winnings, label="mean - std")
	plt.title("Figure 4")
	plt.xlabel("Spins")
	plt.ylabel("Winnings")
	plt.legend()
	save_plot("figure4.png")
	plt.close()

	# Calculate probability
	last_spin = all_winnings[:,-1]

	# Experiment 2 Figure 5
	median_winnings = np.median(all_winnings, axis=0)
	std_winnings = all_winnings.std(axis=0)
	plt.plot(median_winnings, label="median")
	plt.plot(median_winnings + std_winnings, label="median + std")
	plt.plot(median_winnings - std_winnings, label="median - std")
	plt.title("Figure 5")
	plt.xlabel("Spins")
	plt.ylabel("Winnings")
	plt.legend()
	save_plot("figure5.png")
	plt.close()
  		   	  			  	 		  		  		    	 		 		   		 		  
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


def play_episode_256_bankroll(win_prob, num_spins):
	winnings = np.zeros((1001)) # 0 is before first spin. 
	bet = 1
	bankroll = 256
	# spin loop
	for i in range(num_spins):
		if winnings[i] >= 80 or winnings[i] <= -256:
			winnings[(i+1):] = winnings[i] 
			break

		if bet > bankroll:
			bet = bankroll

		won = get_spin_result(win_prob)
		if won:
			winnings[i+1] = winnings[i] + bet
			bankroll = bankroll + bet
			bet = 1
		else:
			winnings[i+1] = winnings[i] - bet
			bankroll = bankroll - bet
			bet = bet*2
	return winnings


if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    test_code()  		   	  			  	 		  		  		    	 		 		   		 		  
