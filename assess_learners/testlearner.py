"""  		   	  			  	 		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
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
"""  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import math  		   	  			  	 		  		  		    	 		 		   		 		  
import LinRegLearner as lrl 
import DTLearner as dtl 	
import RTLearner as rtl	   
import BagLearner as bl	  			  	 		  		  		    	 		 		   		 		  
import sys  
import matplotlib.pyplot as plt		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:  		   	  			  	 		  		  		    	 		 		   		 		  
        print("Usage: python testlearner.py <filename>")  		   	  			  	 		  		  		    	 		 		   		 		  
        sys.exit(1)  		   	  			  	 		  		  		    	 		 		   		 		  
    inf = open(sys.argv[1])
    
    data = np.genfromtxt(inf,delimiter=",")
    if sys.argv[1] == 'Data/Istanbul.csv':	  			  	 		  		  		    	 		 		   		 		  
        data = data[1:, 1:]
                                                                                                                  
    # compute how much of the data is training and testing  		   	  			  	 		  		  		    	 		 		   		 		  
    train_rows = int(0.6* data.shape[0])  		   	  			  	 		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		   	  			  	 		  		  		    	 		 		   		 		                                                                                                      
    # separate out training and testing data  		   	  			  	 		  		  		    	 		 		   		 		  
    trainX = data[:train_rows,0:-1]  		   	  			  	 		  		  		    	 		 		   		 		  
    trainY = data[:train_rows,-1]  		   	  			  	 		  		  		    	 		 		   		 		  
    testX = data[train_rows:,0:-1]  		   	  			  	 		  		  		    	 		 		   		 		  
    testY = data[train_rows:,-1]  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    print(f"{testX.shape}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"{testY.shape}")  		   	  			  	 		  		  		    	 		 		   		 		  
    def testLearnerRmse(learner, verbose=False):
        learner.addEvidence(trainX, trainY) # train it  		   	  			  	 		  		  		    	 		 		   		 		  
        print(learner.author())  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                
        # evaluate in sample  		   	  			  	 		  		  		    	 		 		   		 		  
        predY = learner.query(trainX) # get the predictions  		   	  			  	 		  		  		    	 		 		   		 		  
        rmse_in = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])  		   	  			  	 		  		  		    	 		 		   		 		  
        if verbose:
            print()  		   	  			  	 		  		  		    	 		 		   		 		  
            print("In sample results")  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"RMSE: {rmse_in}")  		   	  			  	 		  		  		    	 		 		   		 		  
            c = np.corrcoef(predY, y=trainY)  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"corr: {c[0,1]}")  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                
        # evaluate out of sample  		   	  			  	 		  		  		    	 		 		   		 		  
        predY = learner.query(testX) # get the predictions  		   	  			  	 		  		  		    	 		 		   		 		  
        rmse_out = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])  		   	  			  	 		  		  		    	 		 		   		 		  
        if verbose:
            print()  		   	  			  	 		  		  		    	 		 		   		 		  
            print("Out of sample results")  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"RMSE: {rmse_out}")  		   	  			  	 		  		  		    	 		 		   		 		  
            c = np.corrcoef(predY, y=testY)  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"corr: {c[0,1]}")  	
        return rmse_in, rmse_out 	  		

    # create a learner and train it  		   	  			  	 		  		  		    	 		 		   		 		  
    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner  		   	  			  	 		  		  		    	 		 		   		 		  
    learner = dtl.DTLearner(10, verbose=True)
    learner = rtl.RTLearner(10, verbose=True)

    # Code to create figure for question 1 in report
    rmse_in_points = []
    rmse_out_points = []
    leaf_range = range(1,30)
    for leaf_size in leaf_range:
        learner = dtl.DTLearner(leaf_size, verbose=True)
        rmse_in, rmse_out = testLearnerRmse(learner, True)
        rmse_in_points.append(rmse_in)
        rmse_out_points.append(rmse_out)
    plt.plot(leaf_range, rmse_in_points, label="in_sample")
    plt.plot(leaf_range, rmse_out_points, label="out_sample")
    plt.title("DT RMSE vs Leaf Size")
    plt.xlabel("Leaf size")
    plt.ylabel("RMSE")
    plt.legend()
    plt.savefig("fig1.png")	
    plt.close()  

    # Code for qn2
    rmse_in_points = []
    rmse_out_points = []
    leaf_range = range(1,30)
    for leaf_size in leaf_range:
        learner = bl.BagLearner(dtl.DTLearner, kwargs={"leaf_size":leaf_size}, bags=20, boost=False, verbose=False)
        rmse_in, rmse_out = testLearnerRmse(learner, True)
        rmse_in_points.append(rmse_in)
        rmse_out_points.append(rmse_out)
    plt.plot(leaf_range, rmse_in_points, label="in_sample")
    plt.plot(leaf_range, rmse_out_points, label="out_sample")
    plt.title("Bagging RMSE vs Leaf Size (20 bags)")
    plt.xlabel("Leaf size")
    plt.ylabel("RMSE")
    plt.legend()
    plt.savefig("fig2.png")	
    plt.close()  	 			

    # Code for qn3	  		    	 	
     		  
    def testLearnerMae(learner, verbose=False):
        learner.addEvidence(trainX, trainY) # train it  		   	  			  	 		  		  		    	 		 		   		 		  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                
        # evaluate in sample  		   	  			  	 		  		  		    	 		 		   		 		  
        predY = learner.query(trainX) # get the predictions  		   	  			  	 		  		  		    	 		 		   		 		  
        mae_in = (abs(trainY - predY)).sum()/trainY.shape[0]  		   	  			  	 		  		  		    	 		 		   		 		  
        if verbose:
            print()  		   	  			  	 		  		  		    	 		 		   		 		  
            print("In sample results")  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"MAE: {mae_in}")  		   	  			  	 		  		  		    	 		 		   		 		  
            c = np.corrcoef(predY, y=trainY)  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"corr: {c[0,1]}")  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                
        # evaluate out of sample  		   	  			  	 		  		  		    	 		 		   		 		  
        predY = learner.query(testX) # get the predictions  		   	  			  	 		  		  		    	 		 		   		 		  
        mae_out = (abs(testY - predY)).sum()/testY.shape[0]		   	  			  	 		  		  		    	 		 		   		 		  
        if verbose:
            print()  		   	  			  	 		  		  		    	 		 		   		 		  
            print("Out of sample results")  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"MAE: {mae_out}")  		   	  			  	 		  		  		    	 		 		   		 		  
            c = np.corrcoef(predY, y=testY)  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"corr: {c[0,1]}")  	
        return mae_in, mae_out 

    print("################Creating MAE charts###################")

    mae_in_points = []
    mae_out_points = []
    leaf_range = range(1,30)
    for leaf_size in leaf_range:
        learner = dtl.DTLearner(leaf_size)
        mae_in, mae_out = testLearnerMae(learner,False)
        mae_in_points.append(mae_in)
        mae_out_points.append(mae_out)
    plt.plot(leaf_range, mae_in_points, label="in_sample")
    plt.plot(leaf_range, mae_out_points, label="out_sample")
    plt.title("DT MAE vs Leaf Size ")
    plt.xlabel("Leaf size")
    plt.ylabel("MAE")
    plt.legend()
    plt.ylim([0, 0.008])
    plt.savefig("fig3a.png")	
    plt.close()  	 

    mae_in_points = []
    mae_out_points = []
    leaf_range = range(1,30)
    for leaf_size in leaf_range:
        learner = rtl.RTLearner(leaf_size)
        mae_in, mae_out = testLearnerMae(learner,False)
        mae_in_points.append(mae_in)
        mae_out_points.append(mae_out)
    plt.plot(leaf_range, mae_in_points, label="in_sample")
    plt.plot(leaf_range, mae_out_points, label="out_sample")
    plt.title("RT MAE vs Leaf Size ")
    plt.xlabel("Leaf size")
    plt.ylabel("MAE")
    plt.legend()
    plt.ylim([0, 0.008])
    plt.savefig("fig3b.png")	
    plt.close()  		


    def testLearnerRSquare(learner, verbose=False):
        learner.addEvidence(trainX, trainY) # train it  		   	  			  	 		  		  		    	 		 		   		 		  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                
        # evaluate in sample  		   	  			  	 		  		  		    	 		 		   		 		  
        predY = learner.query(trainX) # get the predictions  		   	  			  	 		  		  		    	 		 		   		 		  
        mae_in = (abs(trainY - predY)).sum()/trainY.shape[0]  		   	  			  	 		  		  		    	 		 
        r_in = np.corrcoef(predY, y=trainY)[0,1]		   	  			  	 		  		  		    	 		 		   		 		  		   		 		  
        if verbose:
            print()  		   	  			  	 		  		  		    	 		 		   		 		  
            print("In sample results")  		   	  			  	 		  		  		    	 		 		   		 		  
            #print(f"MAE: {mae_in}")  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"corr: {r_in ** 2}")  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                
        # evaluate out of sample  		   	  			  	 		  		  		    	 		 		   		 		  
        predY = learner.query(testX) # get the predictions  		   	  			  	 		  		  		    	 		 		   		 		  
        mae_out = (abs(testY - predY)).sum()/testY.shape[0]		   	  			  	 		  		  		    	 		 		   		 		  
        r_out = np.corrcoef(predY, y=testY)[0,1]  		   	  			  	 		  		  		    	 		 		   		 		  
        if verbose:
            print()  		   	  			  	 		  		  		    	 		 		   		 		  
            print("Out of sample results")  		   	  			  	 		  		  		    	 		 		   		 		  
            #print(f"MAE: {mae_out}")  		   	  			  	 		  		  		    	 		 		   		 		  
            print(f"corr: {r_out ** 2}")  	
        return r_in**2, r_out**2 	

    print("################Creating R-Squared charts###################")
    r2_in_points = []
    r2_out_points = []
    leaf_range = range(1,30)
    for leaf_size in leaf_range:
        learner = dtl.DTLearner(leaf_size)
        r2_in, r2_out = testLearnerRSquare(learner,False)
        r2_in_points.append(r2_in)
        r2_out_points.append(r2_out)
    
    plt.plot(leaf_range, r2_in_points, label="in_sample")
    plt.plot(leaf_range, r2_out_points, label="out_sample")
    plt.title("DT R^2 vs Leaf Size ")
    plt.xlabel("Leaf size")
    plt.ylabel("R^2")
    plt.legend()
    plt.ylim([0.2,1.1])
    plt.savefig("fig3c.png")	
    plt.close()  
    
    r2_in_points = []
    r2_out_points = []
    leaf_range = range(1,30)
    for leaf_size in leaf_range:
        learner = rtl.RTLearner(leaf_size)
        r2_in, r2_out = testLearnerRSquare(learner,False)
        r2_in_points.append(r2_in)
        r2_out_points.append(r2_out)
    
    plt.plot(leaf_range, r2_in_points, label="in_sample")
    plt.plot(leaf_range, r2_out_points, label="out_sample")
    plt.title("RT R^2 vs Leaf Size ")
    plt.xlabel("Leaf size")
    plt.ylabel("R^2")
    plt.ylim([0.2,1.1])
    plt.legend()
    plt.savefig("fig3d.png")	
    plt.close()  