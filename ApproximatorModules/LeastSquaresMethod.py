from .ModelBase import ModelsBase
from .ModelBase import NotFittedError
import numpy as np

class LSM(ModelsBase):
    _Coeffs = []
    model_type = 'Наименьших квадратов'

    def __init__(self, name):
        super().__init__(name)

    def CalculateCoeffs(self, X_original, Y_original):
        self._X_original, self._Y_original = X_original, Y_original
        self._SetDataTypes(X_original, Y_original)

class LinearFunc(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._X_original[i]
                Y += self._Y_original[i]
                XX += self._X_original[i] * self._X_original[i]
                XY += self._X_original[i] * self._Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] + self._Coeffs[0]*X_new[i])
        return Y_new

class RationalForm(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._X_original[i]
                Y += 1/self._Y_original[i]
                XX += self._X_original[i] * self._X_original[i]
                XY += self._X_original[i] / self._Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, 1/(self._Coeffs[1] + self._Coeffs[0]*X_new[i]))
        return Y_new

class LnForm(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += np.log(self._X_original[i])
                Y += self._Y_original[i]
                XX += np.log(self._X_original[i]) * np.log(self._X_original[i])
                XY += np.log(self._X_original[i]) * self._Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] + self._Coeffs[0]*np.log(X_new[i]))
        return Y_new

class EForm(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._X_original[i]
                Y += np.log(self._Y_original[i])
                XX += self._X_original[i] * self._X_original[i]
                XY += self._X_original[i] * np.log(self._Y_original[i])
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = np.exp((Y - A * X) / N)
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] * np.exp(self._Coeffs[0]*X_new[i]))
        return Y_new

class PowerFunc(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += np.log(self._X_original[i])
                Y += np.log(self._Y_original[i])
                XX += np.log(self._X_original[i]) * np.log(self._X_original[i])
                XY += np.log(self._X_original[i]) * np.log(self._Y_original[i])
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = np.exp((Y - A * X) / N)
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] + np.power(X_new[i],self._Coeffs[0]))
        return Y_new

class HyperFunc(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += 1/self._X_original[i]
                Y += self._Y_original[i]
                XX += 1/self._X_original[i] * 1/self._X_original[i]
                XY += 1/self._X_original[i] * self._Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] + self._Coeffs[0]/X_new[i])
        return Y_new

class ExpForm(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._X_original[i]
                Y += np.log(self._Y_original[i])
                XX += self._X_original[i] * self._X_original[i]
                XY += self._X_original[i] * np.log(self._Y_original[i])
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            A = np.exp(A)
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] + self._Coeffs[0]*np.log(X_new[i]))
        return Y_new

class RationalFunc(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._X_original[i]
                Y += self._X_original[i]/self._Y_original[i]
                XX += self._X_original[i] * self._X_original[i]
                XY += self._X_original[i] * (self._X_original[i]/self._Y_original[i])
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, X_new[i]/(self._Coeffs[1] + self._Coeffs[0]*X_new[i]))
        return Y_new

class Aperiodic1Func(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, alpha, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += np.exp(self._X_original[i]*alpha)
                Y += self._Y_original[i]
                XX += np.exp(2*self._X_original[i]*alpha)
                XY += np.exp(self._X_original[i]*alpha) * self._Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] + np.power(self._Coeffs[0],X_new[i]))
        return Y_new

class Aperiodic2Func(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, alpha, beta, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X1 = 0
        X2 = 0
        Y = 0
        XX1 = 0
        XX2 = 0
        XX12 = 0
        XY1 = 0
        XY2 = 0
        if N:
            for i in range(N):
                X1 += np.exp(alpha*self._X_original[i])
                X2 += np.exp(beta*self._X_original[i])
                Y += self._Y_original[i]
                XX1 += np.exp(2*alpha*self._X_original[i])
                XX2 += np.exp(2*beta*self._X_original[i])
                XY1 += np.exp(alpha*self._X_original[i]) * self._Y_original[i]
                XY2 += np.exp(beta*self._X_original[i]) * self._Y_original[i]
                XX12 += np.exp((alpha+beta)*self._X_original[i])
            C = N * XY2 - X2 * Y + (N * XY1 - X1 * Y) * (X1 * X2 - N * XX12) / (N * XX1 - X1 * X1)
            C = C / (N * XX2 - X2 * X2 - (X1 * X2 - N * XX12)/(N * XX1 - X1 * X1))
            A = (N * XY1 - X1 * Y + C * (X1 * X2 - N * XX12))/(N * XX1 - X1 * X1)
            B = (Y - A * X1 - C * X2) / N
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] * np.power(self._Coeffs[0],X_new[i]))
        return Y_new

class HarmonicFunc(LSM):
    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, alpha, omega, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        N = len(self._X_original)
        X1 = 0
        X2 = 0
        Y = 0
        XX1 = 0
        XX2 = 0
        XX12 = 0
        XY1 = 0
        XY2 = 0
        if N:
            for i in range(N):
                X1 += np.exp(alpha * self._X_original[i]) * np.sin(omega * self._X_original[i])
                X2 += np.exp(alpha * self._X_original[i]) * np.cos(omega * self._X_original[i])
                Y += self._Y_original[i]
                XX1 += np.exp(2 * alpha * self._X_original[i]) * np.sin(omega * self._X_original[i]) * np.sin(omega * self._X_original[i])
                XX2 += np.exp(2 * alpha *self._X_original[i]) * np.cos(omega * self._X_original[i]) * np.cos(omega * self._X_original[i])
                XY1 += np.exp(alpha * self._X_original[i]) * np.sin(omega * self._X_original[i]) * self._Y_original[i]
                XY2 += np.exp(alpha * self._X_original[i]) * np.cos(omega * self._X_original[i]) * self._Y_original[i]
                XX12 += np.exp(2 * alpha * self._X_original[i]) * np.sin(omega * self._X_original[i]) * np.cos(omega * self._X_original[i])
            Z2 = XY2 * X1 * X1 - XY2 * XX1 * N + X2 * Y * XX2 - X1 * X2 * XY1 + XX12 * XY1 * N - XX12 * X1 * Y
            Z2 = Z2 / (X2*X2*XX1-2*X2*XX12*X1+XX12*XX12*N+XX2*X1*X1-XX2*XX1*N)
            Z1 = -(XY1*N-Y*X1+X1*X2*Z2-XX12*N*Z2)/(X1*X1-XX1*N)
            C = np.arctan(Z2/Z1)
            A = Z2/np.sin(C)
            B = -(-Y+Z1*X1+Z2*X2)/N
            self._Coeffs.insert(0, A)
            self._Coeffs.insert(1, B)
        return self._Coeffs
    
    def Predict(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._Coeffs[1] * np.power(self._Coeffs[0],X_new[i]))
        return Y_new

class PolyFunc(LSM):
    
    model_type = 'Полинаминальный'

    def __init__(self,name):
        super().__init__(name)
    def CalculateCoeffs(self, NumberPoly, X_original, Y_original):
        super().CalculateCoeffs(X_original, Y_original)
        self._Coeffs = np.polyfit(self._X_original, self._Y_original, NumberPoly)
        return self._Coeffs
    def Predict(self, X_new):
        N = len(X_new)
        predict = np.poly1d(self._Coeffs)
        Y_new = []
        for i in range(0,N):
            Y_new.append(predict(X_new[i]))
        return Y_new
