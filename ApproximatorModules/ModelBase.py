'''Класс ModelView для модели линейной регрессии.'''
import pandas as pd
import numpy as np
from Enums.Colors import Colors
from Enums.Markers import Markers
from Enums.LineTypes import Lines
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

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
        return metrics.mean_squared_error(self._Y_original, self._Predictor.predict(self._X_original))