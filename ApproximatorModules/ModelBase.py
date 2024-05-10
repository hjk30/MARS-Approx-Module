import numpy as np
from .Enums.Colors import Colors
from .Enums.Markers import Markers
from .Enums.LineTypes import Lines
from sklearn.model_selection import train_test_split
from sklearn import metrics

class NotFittedError(ValueError, AttributeError):
    '''Exception class to raise if estimator is used before fitting.'''

class ModelsBase():
    _X_original = []
    _Y_original = []
    name: str
    model_type: str
    _model: object
    
    HyperParameters = dict()
    '''Список-словарь гиперпараметров модели.'''
    
    Parameters = list()
    '''Список параметров модели'''

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
    
    TargetValueName = ""
    '''Наименование целевой переменной данных'''
    
    DataTypes = {}
    '''Список-словарь типов данных для предикторов данных'''
    
    PredictorNames = list()
    '''Список наименований имен предикторов'''

    def __init__(self, name):
        self.name = name

    def Predict(self, X_new):
        raise NotImplementedError
    
    def FillQualityMatrix(self, model, X, Y, ratio):
        '''Заполняет матрицу матриками качества'''
        X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=ratio,random_state=42)
    
        Test_prediction = model.Predict(X_test)
        
        MSM = np.sqrt(metrics.mean_squared_error(Y_test,Test_prediction))
        MSM = {'Метрика среднеквадратической ошибки' : MSM}
        self.QualityMetrix.update(MSM)
        
        R2M = np.round(metrics.r2_score(Y_test,Test_prediction),2)
        R2M = {'Метрика R^2' : R2M}
        self.QualityMetrix.update(R2M)
        
    def _SetDataTypes(self,X,Y):
        '''Производит формирование словаря типов данных предикторов и
        целевой переменной.'''
        
        #X_train = pd.DataFrame(X)
        #Y_train = pd.DataFrame(Y)
        #dataTypes = X_train.dtypes
        #[self.DataTypes.update({f'{X_train.keys()[i]}': dataTypes[i]}) for i in range(len(dataTypes))]
        #
        #self.DataTypes.update({f'{Y_train.Name}':Y_train.dtypes})
        #predictors = X_train.keys().tolist()
        #[self.PredictorNames.append(predictors[i]) for i in range(len(predictors))]
        #self.TargetValueName = Y_train.Name