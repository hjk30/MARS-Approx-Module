'''Класс ModelView для модели линейной регрессии.'''
import pandas as pd
import numpy as np
from .ModelBase import ModelsBase
from .ModelBase import NotFittedError
from enum import Enum as Enums
from .Enums.Colors import Colors
from .Enums.Markers import Markers
from .Enums.LineTypes import Lines
from sklearn.linear_model import LinearRegression
from sklearn import metrics

class LinearModel(ModelsBase):
    '''Экземпляр линейной модели'''
    
    _model: LinearRegression
    model_type = 'Линейная регрессия'

    Intercept = 0
    '''Значение перехвата модели'''
    
    def __init__(self, name):
        '''Инициализатор экземпляра данного класса.'''
        super().__init__(name)
            
    def TrainModel(self,X,Y,ratio,hyperparams):
        '''Производит обучение модели на входных данных.
        Входные данные делятся на обучающую и тестовую выборки, после чего произходит обучение модели.
        Метрики качества записываются в поле QualityMetrix.'''
        self._model = LinearRegression(**hyperparams)

        self._model.fit(X, Y)
        
        self._SetDataTypes(X,Y)
    
    def Predict(self,X):
        '''Производит предсказание целевой переменной по входным данным.
        Входной массив должен иметь размерность, заданную предикторам при обучении.'''
        
        try:
            return self._model.predict(X)
        except:
            raise NotFittedError("Модель не обучена")