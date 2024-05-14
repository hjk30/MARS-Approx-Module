#%%
import View
import numpy as np
from ApproximatorModules.LeastSquaresMethod import *
from ApproximatorModules.DecTreeRegressor import *
from ApproximatorModules.LinearModel import *
import csv
    
#view = View.MainWindow()
#
#view.start()
def generate_numbers(start, end):
    result = []
    for i in range(1000):
        result.append(start + i * (end - start) / 1000)
    return result

class Controller:
	GraphWindow: View.MainGraphWindow

	def __init__(self):
		return
	def writeSamleData(self):
		xarr = []
		yarr = []
		for i in range(100):
			xarr.append(i)
			yarr.append(i*i + 2 * i + 10 + np.random.uniform(-500,500))
		self.save_to_csv(xarr,yarr)

	def save_to_csv(self, xarr, yarr):
		with open('output.csv', 'w', newline='') as f:
			writer = csv.writer(f)
			for i in range(len(xarr)):
				writer.writerow([xarr[i], yarr[i]])
	def add_tab(self,name,model_type,hyperparams,xarr:list,yarr:list):
		if (xarr == []):
			for i in range(100):
				xarr.append(i)
				yarr.append(i*i + 2 * i + 10 + np.random.uniform(-500,500))
		new_x = generate_numbers(max(xarr), min(xarr))
		if (model_type == 'Poly'):
			NewModel = PolyFunc(name)
			NewModel.CalculateCoeffs(hyperparams['NumberPoly'],xarr,yarr)
			new_y = NewModel.Predict(new_x)
			NewModel.FillQualityMatrix(NewModel,xarr,yarr,0.3)
		elif(model_type == 'Linear'):
			NewModel = LinearModel(name)
			NewModel.TrainModel([[i] for i in xarr],[[i] for i in yarr],0.3,hyperparams)
			new_y = NewModel.Predict([[i] for i in new_x])
			NewModel.FillQualityMatrix(NewModel,[[i] for i in xarr],[[i] for i in yarr],0.3)
		elif(model_type == 'Tree'):
			NewModel = TreeApprox(name)
			NewModel.TrainModel([[i] for i in xarr],[[i] for i in yarr],0.3,hyperparams)
			new_y = NewModel.Predict([[i] for i in new_x])
			NewModel.FillQualityMatrix(NewModel,[[i] for i in xarr],[[i] for i in yarr],0.3)
		elif(model_type == 'RandomForest'):
			NewModel = RandomForestApprox(name)
			NewModel.TrainModel([[i] for i in xarr],yarr,0.3,hyperparams)
			new_y = NewModel.Predict([[i] for i in new_x])
			NewModel.FillQualityMatrix(NewModel,[[i] for i in xarr],[[i] for i in yarr],0.3)
			
		self.GraphWindow.add_tab(xarr,yarr, new_x, new_y, NewModel)

	def start(self):
		self.GraphWindow = View.MainGraphWindow()
		self.GraphWindow.start(self)
# %%
Contr = Controller()
#Contr.writeSamleData()
Contr.start()