from sklearn import tree
from sklearn import ensemble
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


class ModelBase():
    _X_original = []
    _Y_original = []
    _X_new = []
    _Y_new = []
    _Predictor: object

    def __init__(self, X_original, Y_original):
        self._X_original = X_original
        self._Y_original = Y_original

    def CalculateY(self, X_new):
        self._X_new = X_new
        self._Y_new = self._Predictor.predict(self._X_new)
        return self._Y_new
    
    def CalculateError(self):
        return mean_squared_error(self._Y_original, self._Predictor.predict(self._X_original))

class TreeApprox(ModelBase):
    _Predictor: tree.DecisionTreeRegressor

    def __init__(self, X_original, Y_original):
        ModelBase.__init__(self, X_original, Y_original)
    
    def CreateModel(self, hyperparams):
        self._Predictor = tree.DecisionTreeRegressor(**hyperparams)
        self._Predictor.fit(self._X_original, self._Y_original)
    
class RandomForestApprox(ModelBase):
    _Predictor: ensemble.RandomForestRegressor

    def __init__(self, X_original, Y_original):
        ModelBase.__init__(self, X_original, Y_original)
    
    def CreateModel(self, hyperparams):
        self._Predictor = ensemble.RandomForestRegressor(**hyperparams)
        self._Predictor.fit(self._X_original, self._Y_original)
    
def test():
    # Create a random dataset
    rng = np.random.RandomState(42)
    X = np.sort(5 * rng.rand(80, 1), axis=0)
    y = np.sin(X).ravel()
    y[::5] += 3 * (0.5 - rng.rand(16))

    # Fit regression model
    regr_1 = TreeApprox(X, y)
    regr_2 = RandomForestApprox(X, y)
    regr_1.CreateModel({'max_depth': 5})
    regr_2.CreateModel({'max_depth': 5})

    # Predict
    X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
    y_1 = regr_1.CalculateY(X_test)
    y_2 = regr_2.CalculateY(X_test)

    # Plot the results
    plt.figure()
    plt.scatter(X, y, s=20, edgecolor="black", c="darkorange", label="data")
    plt.plot(X_test, y_1, color="cornflowerblue", label="max_depth=2", linewidth=2)
    plt.plot(X_test, y_2, color="yellowgreen", label="max_depth=5", linewidth=2)
    plt.xlabel("data")
    plt.ylabel("target")
    plt.title("Decision Tree Regression")
    plt.legend()
    plt.show()
    print(regr_1.CalculateError())
    print(regr_2.CalculateError())

test()