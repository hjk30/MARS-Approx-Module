'''Класс ModelView для модели линейной регрессии.'''
import pandas as pd
import numpy as np
from Enums.Colors import Colors
from Enums.Markers import Markers
from Enums.LineTypes import Lines
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

class NotFittedError(ValueError, AttributeError):
    '''Exception class to raise if estimator is used before fitting.'''

class LinearModel:
    '''Экземпляр линейной модели'''
    
    HyperParameters = dict()
    '''Список-словарь гиперпараметров модели.'''
    
    Parameters = list()
    '''Список параметров модели'''
    
    Intercept = 0
    '''Значение перехвата модели'''
    
    QualityMetrix = dict()
    '''Список-словарь метрик качества обученной модели'''
    
    LineColor = Colors.RED
    '''Цвет линии графика данной модели'''
    
    Marker = Markers.CIRCLE
    '''Тип маркера данной модели'''
    
    LineType = Lines.LINE
    '''Тип линии графика данной модели'''
    
    DataFilePath = ""
    '''Путь до файла данных'''
    
    PredictorNames = list()
    '''Список наименований имен предикторов'''
    
    TargetValueName = ""
    '''Наименование целевой переменной данных'''
    
    DataTypes = {}
    '''Список-словарь типов данных для предикторов данных'''
    
    def __init__(self, name, intercept=True, positive=False):
        '''Инициализатор экземпляра данного класса.'''
        
        self.__name = name
        self.__model = LinearRegression(fit_intercept=intercept,positive=positive)
    
    def Name(self,name=None):
        '''Свойство наименования данной модели.'''
        
        if name == None:
            return self.__name
        else:
            self.__name = name      
            
    def TrainModel(self,X,Y,ratio=0.3):
        '''Производит обучение модели на входных данных.
        Входные данные делятся на обучающую и тестовую выборки, после чего произходит обучение модели.
        Метрики качества записываются в поле QualityMetrix.'''
        
        predictors = X.keys().tolist()
        [self.PredictorNames.append(predictors[i]) for i in range(len(predictors))]
        self.TargetValueName = Y.name
        
        self.__SetDataTypes(X,Y)
        
        X_train, X_test, Y_train, Y_test = train_test_split(
            X,Y,test_size=ratio,random_state=42)
        
        self.__model.fit(X_train,Y_train)
        Test_prediction = self.__model.predict(X_test)
        
        self.Parameters, self.Intercept = self.__model.coef_, self.__model.intercept_
        
        MSM = np.sqrt(metrics.mean_squared_error(Y_test,Test_prediction))
        MSM = {'Метрика среднеквадратической ошибки' : MSM}
        self.QualityMetrix.update(MSM)
        
        R2M = np.round(metrics.r2_score(Y_test,Test_prediction),2)
        R2M = {'Метрика R^2' : R2M}
        self.QualityMetrix.update(R2M)
    
    def Predict(self,X):
        '''Производит предсказание целевой переменной по входным данным.
        Входной массив должен иметь размерность, заданную предикторам при обучении.'''
        
        try:
            return self.__model.predict(X)
        except:
            raise NotFittedError("Модель не обучена")
        
    def __SetDataTypes(self,X,Y):
        '''Производит формирование словаря типов данных предикторов и
        целевой переменной.'''
        
        X_train = pd.DataFrame(X)
        dataTypes = X_train.dtypes
        [self.DataTypes.update({f'{X_train.keys()[i]}':
            dataTypes[i]}) for i in range(len(dataTypes))]
        
        self.DataTypes.update({f'{Y.name}':Y.dtype})