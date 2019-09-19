import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class RTLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size, verbose = False):  		   	  			  	 		  		  		    	 		 		   		 		  
        pass # move along, these aren't the drones you're looking for  		   	  			  	 		  		  		    	 		 		   		 		  
        self.leaf_size = leaf_size

    def author(self):  		   	  			  	 		  		  		    	 		 		   		 		  
        return 'jkok7' # replace tb34 with your Georgia Tech username  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def addEvidence(self,dataX,dataY):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Add training data to learner  		   	  			  	 		  		  		    	 		 		   		 		  
        @param dataX: X values of data to add  		   	  			  	 		  		  		    	 		 		   		 		  
        @param dataY: the Y training values  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			
        tree = self.build_tree(np.column_stack((dataX, dataY)))	  			  	 		  		  		    	 		 		   		 		  
        self.dt = tree
  		   	  			  	 		  		  		    	 		 		   		 		  
    def query(self,points):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Estimate a set of test points given the model we built.  		   	  			  	 		  		  		    	 		 		   		 		  
        @param points: should be a numpy array with each row corresponding to a specific query.  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns the estimated values according to the saved model.  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        result = np.zeros((points.shape[0]))
        tree = self.dt
        counter = 0
        for point in points:
            i = 0
            # If tree is not a leaf, keep going deeper till it reach a leaf
            while tree[i,0] != -1:
                var = int(tree[i,0])
                # go left
                if point[var] <= tree[i,1]:
                    i += int(tree[i,2])
                # go right
                else: 
                    i += int(tree[i,3])
            # store result
            result[counter] = tree[i,1]
            counter += 1
        return result
    
    def build_tree(self, data):
        # Separate X and Y for easier management
        dataX = data[:, :-1]
        dataY = data[:, -1].reshape(dataX.shape[0], 1)
        if dataX.shape[0] <= self.leaf_size: 
            return np.array([-1, dataY.mean(), -1, -1]).reshape(1,4)
        if np.all(dataY == dataY[0]): 
            return np.array([-1, dataY.mean(), -1, -1]).reshape(1,4)
        
        loop = 0
        # This loop will try to split data. If not possible, try other random values.
        # If no split after 10 tries, return as leaf.
        while True:
            if loop >= 10:
                return np.array([-1, dataY.mean(), -1, -1]).reshape(1,4)
            i = np.random.randint(0, dataX.shape[1])
            var1 = np.random.randint(0, dataX.shape[0])
            var2 = np.random.randint(0, dataX.shape[0])
            split_val = (dataX[var1, i] + dataX[var2, i]) / 2
            left_data = data[data[:,i] <= split_val]
            right_data = data[data[:,i] > split_val]
            # If data is successfully split, exit loop
            if left_data.shape != data.shape:
                break
            loop += 1
        lefttree = self.build_tree(data[data[:,i] <= split_val])
        righttree = self.build_tree(data[data[:,i] > split_val])
        root = np.array([i, split_val, 1, lefttree.shape[0] + 1]).reshape(1,4)
        tree = np.append(root, lefttree, axis=0)
        tree = np.append(tree, righttree, axis=0)
        return tree


if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("the secret clue is 'zzyzx'")  	