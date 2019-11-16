"""  		   	  			  	 		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
  		   	  			  	 		  		  		    	 		 		   		 		  
Student Name: Jian Yu Kok (replace with your name)  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jkok7 (replace with your User ID)  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903550380 (replace with your GT ID)  		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import random as rand  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class QLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			  	 		  		  		    	 		 		   		 		  
        self.num_actions = num_actions  		   	  			  	 		  		  		    	 		 		   		 		  
        self.s = 0  		   	  			  	 		  		  		    	 		 		   		 		  
        self.a = 0  		   	  		

        # My Code
        self.num_states = num_states
        self.q_table = np.zeros((num_states, num_actions))
        self.epsilon = rar
        self.epsilon_decay = radr
        self.lr = alpha
        self.discount = gamma
        self.T = np.zeros((num_states, num_actions, num_states))
        self.T += 0.0000001
        self.R = np.zeros((num_states, num_actions))
        self.dyna = dyna
        self.observed_s_a = np.zeros((num_states, num_actions))
        # My Code		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def querysetstate(self, s):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Update the state without updating the Q-table  		   	  			  	 		  		  		    	 		 		   		 		  
        @param s: The new state  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        self.s = s  
        action = np.argmax(self.q_table[self.s])              		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: 
            print(f"s = {s}, a = {action}")  		   	  			  	 		  		  		    	 		 		   		 		  
        
        self.a = action
        return action  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def query(self,s_prime,r):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Update the Q table and return an action  		   	  			  	 		  		  		    	 		 		   		 		  
        @param s_prime: The new state  		   	  			  	 		  		  		    	 		 		   		 		  
        @param r: The ne state  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			  	 		  		  		    	 		 		   		 		  
        """  
        self.T[self.s, self.a, s_prime] += 1
        self.R[self.s, self.a] = (1-self.lr)*self.R[self.s, self.a] + self.lr*r
        u = r + self.discount * np.max(self.q_table[s_prime, :])
        diff = u - self.q_table[self.s, self.a]
        self.q_table[self.s, self.a] += self.lr * (diff)

        if rand.random() < self.epsilon:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.q_table[s_prime])    	   	  			  	 		  		  		    	 		 		   		 		  

        if self.dyna > 0:
            self.observed_s_a[self.s,self.a] += 1
            self.hallucinate()
        
        if self.verbose: print(f"s = {s_prime}, a = {action}, r={r}")  		   	  			  	 		  		  		    	 		 		   		 		  
        self.s = s_prime
        self.a = action
        self.epsilon *= self.epsilon_decay    

        return action  		   	  		
    
    def hallucinate(self,):
        observed_states, observed_actions = np.nonzero(self.observed_s_a)
        random_p = np.random.random(size=(self.dyna))
        random_s = np.random.randint(len(observed_states), size=self.dyna)
        T_matrix = self.T / self.T.sum(axis=-1)[:,:,None]
        T_matrix = np.cumsum(T_matrix, axis=-1)
        for i in range(self.dyna):
            idx = random_s[i]
            s = observed_states[idx]
            a = observed_actions[idx]
            T = T_matrix[s,a,:]
            #print(T)
            prob = random_p[i]
            s_prime = np.searchsorted(T, prob, side='left')
            r = self.R[s,a]

            u = r + self.discount * np.max(self.q_table[s_prime, :])
            diff = u - self.q_table[s, a]
            self.q_table[s, a] += self.lr * (diff)

    def author(self):
        return "jkok7"  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("Remember Q from Star Trek? Well, this isn't him")  		   	  			  	 		  		  		    	 		 		   		 		  
