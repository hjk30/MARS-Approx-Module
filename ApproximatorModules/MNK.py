import numpy as np
import sklearn.metrics as skm
class MNK(object):
    __X_original = []
    __Y_original = []
    __X_new = []
    __Coeffs = []

    def __init__(self, X_original, Y_original, X_new):
        self.__X_original = X_original
        self.__Y_original = Y_original
        self.__X_new = X_new

    def CalculateCoeffs(self):
        raise NotImplementedError
    
    def CalculateY(self, X_new = []):
        raise NotImplementedError
    
    def CalculateError(self):
        raise NotImplementedError

class LinearFunc(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._MNK__X_original[i]
                Y += self._MNK__Y_original[i]
                XX += self._MNK__X_original[i] * self._MNK__X_original[i]
                XY += self._MNK__X_original[i] * self._MNK__Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] + self._MNK__Coeffs[0]*X_new[i])
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
class RationalForm(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._MNK__X_original[i]
                Y += 1/self._MNK__Y_original[i]
                XX += self._MNK__X_original[i] * self._MNK__X_original[i]
                XY += self._MNK__X_original[i] / self._MNK__Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, 1/(self._MNK__Coeffs[1] + self._MNK__Coeffs[0]*X_new[i]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon

class LnForm(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += np.log(self._MNK__X_original[i])
                Y += self._MNK__Y_original[i]
                XX += np.log(self._MNK__X_original[i]) * np.log(self._MNK__X_original[i])
                XY += np.log(self._MNK__X_original[i]) * self._MNK__Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] + self._MNK__Coeffs[0]*np.log(X_new[i]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
class EForm(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._MNK__X_original[i]
                Y += np.log(self._MNK__Y_original[i])
                XX += self._MNK__X_original[i] * self._MNK__X_original[i]
                XY += self._MNK__X_original[i] * np.log(self._MNK__Y_original[i])
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = np.exp((Y - A * X) / N)
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] * np.exp(self._MNK__Coeffs[0]*X_new[i]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon

class PowerFunc(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += np.log(self._MNK__X_original[i])
                Y += np.log(self._MNK__Y_original[i])
                XX += np.log(self._MNK__X_original[i]) * np.log(self._MNK__X_original[i])
                XY += np.log(self._MNK__X_original[i]) * np.log(self._MNK__Y_original[i])
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = np.exp((Y - A * X) / N)
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] + np.power(X_new[i],self._MNK__Coeffs[0]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
class HyperFunc(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += 1/self._MNK__X_original[i]
                Y += self._MNK__Y_original[i]
                XX += 1/self._MNK__X_original[i] * 1/self._MNK__X_original[i]
                XY += 1/self._MNK__X_original[i] * self._MNK__Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] + self._MNK__Coeffs[0]/X_new[i])
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
class ExpForm(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._MNK__X_original[i]
                Y += np.log(self._MNK__Y_original[i])
                XX += self._MNK__X_original[i] * self._MNK__X_original[i]
                XY += self._MNK__X_original[i] * np.log(self._MNK__Y_original[i])
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            A = np.exp(A)
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] + self._MNK__Coeffs[0]*np.log(X_new[i]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
class RationalFunc(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += self._MNK__X_original[i]
                Y += self._MNK__X_original[i]/self._MNK__Y_original[i]
                XX += self._MNK__X_original[i] * self._MNK__X_original[i]
                XY += self._MNK__X_original[i] * (self._MNK__X_original[i]/self._MNK__Y_original[i])
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, X_new[i]/(self._MNK__Coeffs[1] + self._MNK__Coeffs[0]*X_new[i]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
class Aperiodic1Func(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self, alpha):
        N = len(self._MNK__X_original)
        X = 0
        Y = 0
        XX = 0
        XY = 0
        if N:
            for i in range(N):
                X += np.exp(self._MNK__X_original[i]*alpha)
                Y += self._MNK__Y_original[i]
                XX += np.exp(2*self._MNK__X_original[i]*alpha)
                XY += np.exp(self._MNK__X_original[i]*alpha) * self._MNK__Y_original[i]
            A = (N * XY - X * Y) / (N * XX - X * X)
            B = (Y - A * X) / N
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] + np.power(self._MNK__Coeffs[0],X_new[i]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
    
class Aperiodic2Func(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self, alpha, beta):
        N = len(self._MNK__X_original)
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
                X1 += np.exp(alpha*self._MNK__X_original[i])
                X2 += np.exp(beta*self._MNK__X_original[i])
                Y += self._MNK__Y_original[i]
                XX1 += np.exp(2*alpha*self._MNK__X_original[i])
                XX2 += np.exp(2*beta*self._MNK__X_original[i])
                XY1 += np.exp(alpha*self._MNK__X_original[i]) * self._MNK__Y_original[i]
                XY2 += np.exp(beta*self._MNK__X_original[i]) * self._MNK__Y_original[i]
                XX12 += np.exp((alpha+beta)*self._MNK__X_original[i])
            C = N * XY2 - X2 * Y + (N * XY1 - X1 * Y) * (X1 * X2 - N * XX12) / (N * XX1 - X1 * X1)
            C = C / (N * XX2 - X2 * X2 - (X1 * X2 - N * XX12)/(N * XX1 - X1 * X1))
            A = (N * XY1 - X1 * Y + C * (X1 * X2 - N * XX12))/(N * XX1 - X1 * X1)
            B = (Y - A * X1 - C * X2) / N
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] * np.power(self._MNK__Coeffs[0],X_new[i]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
class HarmonicFunc(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self, alpha, omega):
        N = len(self._MNK__X_original)
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
                X1 += np.exp(alpha * self._MNK__X_original[i]) * np.sin(omega * self._MNK__X_original[i])
                X2 += np.exp(alpha * self._MNK__X_original[i]) * np.cos(omega * self._MNK__X_original[i])
                Y += self._MNK__Y_original[i]
                XX1 += np.exp(2 * alpha * self._MNK__X_original[i]) * np.sin(omega * self._MNK__X_original[i]) * np.sin(omega * self._MNK__X_original[i])
                XX2 += np.exp(2 * alpha *self._MNK__X_original[i]) * np.cos(omega * self._MNK__X_original[i]) * np.cos(omega * self._MNK__X_original[i])
                XY1 += np.exp(alpha * self._MNK__X_original[i]) * np.sin(omega * self._MNK__X_original[i]) * self._MNK__Y_original[i]
                XY2 += np.exp(alpha * self._MNK__X_original[i]) * np.cos(omega * self._MNK__X_original[i]) * self._MNK__Y_original[i]
                XX12 += np.exp(2 * alpha * self._MNK__X_original[i]) * np.sin(omega * self._MNK__X_original[i]) * np.cos(omega * self._MNK__X_original[i])
            Z2 = XY2 * X1 * X1 - XY2 * XX1 * N + X2 * Y * XX2 - X1 * X2 * XY1 + XX12 * XY1 * N - XX12 * X1 * Y
            Z2 = Z2 / (X2*X2*XX1-2*X2*XX12*X1+XX12*XX12*N+XX2*X1*X1-XX2*XX1*N)
            Z1 = -(XY1*N-Y*X1+X1*X2*Z2-XX12*N*Z2)/(X1*X1-XX1*N)
            C = np.arctan(Z2/Z1)
            A = Z2/np.sin(C)
            B = -(-Y+Z1*X1+Z2*X2)/N
            self._MNK__Coeffs.insert(0, A)
            self._MNK__Coeffs.insert(1, B)
        return self._MNK__Coeffs
    
    def CalculateY(self, X_new):
        Y_new = []
        N = len(X_new)
        if N:
            for i in range(0,N):
                Y_new.insert(i, self._MNK__Coeffs[1] * np.power(self._MNK__Coeffs[0],X_new[i]))
        return Y_new
    
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
class PolyFunc(MNK):
    def __init__(self, X_original, Y_original, X_new):
        MNK.__init__(self, X_original, Y_original, X_new)
    def CalculateCoeffs(self, NumberPoly):
        self._MNK__Coeffs = np.polyfit(self._MNK__X_original, self._MNK__Y_original, NumberPoly)
        return self._MNK__Coeffs
    def CalculateY(self, X_new):
        N = len(X_new)
        predict = np.poly1d(self._MNK__Coeffs)
        Y_new = []
        for i in range(0,N):
            Y_new.append(predict(X_new[i]))
        return Y_new
    def CalculateError(self):
        Y_error = self.CalculateY(self._MNK__X_original)
        epsilon = skm.mean_squared_error(self._MNK__Y_original, Y_error)
        return epsilon
X_orig = [5, 8, 17, 24, 27, 28, 29, 62, 95, 98]
Y_orig = [7, 68, 23, 40, 97, 4, 90, 17, 73, 29]
X_new = [6, 11, 16, 20, 27, 34, 44, 79, 94, 96]
alpha = 0.8
beta = 0.4
omega = 0.6
NumberPoly = 4
ExampleObj = PolyFunc(X_orig, Y_orig, X_new)
print(ExampleObj.CalculateCoeffs(NumberPoly))
print(ExampleObj.CalculateY(ExampleObj._MNK__X_new))
print(ExampleObj.CalculateError())