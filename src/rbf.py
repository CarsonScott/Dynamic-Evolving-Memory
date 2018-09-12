import numpy as np
import matplotlib.pyplot as plt
from lib.util import *

class RBFN(object):

    def __init__(self, input_shape, hidden_shape, sigma = 1.0):
        """ radial basis function network
        # Arguments
            input_shape: dimension of the input data
            e.g. scalar functions have should have input_dimension = 1
            hidden_shape: the number
            hidden_shape: number of hidden radial basis functions,
            also, number of centers.
        """
        self.input_shape = input_shape
        self.hidden_shape = hidden_shape
        self.sigma = sigma
        self.centers = None
        self.weights = None

    def _kernel_function(self, center, data_point):
        return np.exp(-self.sigma*np.linalg.norm(center-data_point)**2)

    def _calculate_interpolation_matrix(self,X):
        """ Calculates interpolation matrix G using self._kernel_function
        # Arguments
            X: Training data
        # Input shape
            (num_data_samples, input_shape)
        # Returns
            G: Interpolation matrix
        """
        G = np.zeros((X.shape[0], self.hidden_shape))
        for data_point_arg, data_point in enumerate(X):
            for center_arg, center in enumerate(self.centers):
                G[data_point_arg,center_arg] = self._kernel_function(center,
                                                                data_point)
        return G

    def fit(self,X,Y):
        """ Fits self.weights using linear regression
        # Arguments
            X: training samples
            Y: targets
        # Input shape
            X: (num_data_samples, input_shape)
            Y: (num_data_samples, input_shape)
        """
        random_args = np.random.permutation(X.shape[0]).tolist()
        self.centers = [X[arg] for arg in random_args][:self.hidden_shape]
        G = self._calculate_interpolation_matrix(X)

        self.weights = np.dot(np.linalg.pinv(G),Y)

    def predict(self,X):
        """
        # Arguments
            X: test data
        # Input shape
            (num_test_samples, input_shape)
        """
        G = self._calculate_interpolation_matrix(X)
        predictions = np.dot(G, self.weights)
        return predictions

x = np.array([i for i in range(100)])

y = np.sin(x)
model = RBFN(input_shape = 1, hidden_shape = 10)
for i in range(10):
    model.fit(x,y)
y_pred = model.predict(x)

plt.plot(x,y,'b-',label='real')
plt.plot(x,y_pred,'r-',label='fit')
plt.legend(loc='upper right')
plt.title('Interpolation using a RBFN')
plt.show()