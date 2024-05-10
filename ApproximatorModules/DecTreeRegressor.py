from sklearn import tree
from sklearn import ensemble
import numpy as np
import matplotlib.pyplot as plt
from .ModelBase import *


class TreeApprox(ModelsBase):
    _model: tree.DecisionTreeRegressor

    model_type = 'Дерево решений'

    def __init__(self, name):
        super().__init__(name)

    def Predict(self, X):
        
        try:
            return self._model.predict(X)
        except:
            raise NotFittedError("Модель не обучена")

    def TrainModel(self,X,Y,ratio,hyperparams):

        self._model = tree.DecisionTreeRegressor(**hyperparams)
        self._X_original, self._Y_original = X, Y
        self._model.fit(X, Y)
        
        #predictors = X.keys().tolist()
        #[self.PredictorNames.append(predictors[i]) for i in range(len(predictors))]
        #self.TargetValueName = Y.name
        
        self._SetDataTypes(X,Y)
    
class RandomForestApprox(ModelsBase):
    _model: ensemble.RandomForestRegressor
    model_type = 'Случайный лес'

    def __init__(self, name):
        super().__init__(name)

    def Predict(self, X):
        '''Производит предсказание целевой переменной по входным данным.
        Входной массив должен иметь размерность, заданную предикторам при обучении.'''
        
        try:
            return self._model.predict(X)
        except:
            raise NotFittedError("Модель не обучена")

    def TrainModel(self,X,Y,ratio,hyperparams):
        '''Производит обучение модели на входных данных.
        Входные данные делятся на обучающую и тестовую выборки, после чего произходит обучение модели.
        Метрики качества записываются в поле QualityMetrix.'''

        self._model = ensemble.RandomForestRegressor(**hyperparams)
        self._X_original, self._Y_original = X, Y
        self._model.fit(X, Y)
        
        self._SetDataTypes(X,Y)