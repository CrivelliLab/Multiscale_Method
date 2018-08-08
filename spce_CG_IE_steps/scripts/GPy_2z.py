#
# Gaussian Process - for Coarse-Grain Potential Development
# Berkeley National Lab, Summer 2018
# University of Saint Mary
#

import numpy as np
from matplotlib import pyplot as plt
import GPy
from IPython.display import display

d = 1 # input dimension
var = 1 # variance
theta = 1 # 0.2 # lengthscale

InFileName = 'BiomolecularData.dat'
f = open(InFileName, 'r')
N = len(f.readlines())  # number of observed points.
f.close()

X = np.zeros(shape=(N,1))
Y = np.zeros(shape=(N,1))

#------------------------------------
# Open the file and read data points from the file

InFile = open(InFileName, 'r')
LineNumber = 0
for Line in InFile:
    #Remove the lin-ending characters
    Line = Line.strip('\n')
    row = Line.split()
    #Index the counter used to keep track of line number
    X[LineNumber] = float(row[0])
    Y[LineNumber] = float(row[1])
    LineNumber += 1
#After the loop is completed., close the file
InFile.close()
# -----------------------------------

# plt.scatter(X, Y)
# plt.axis([0, 1.5, -2, 15])

kernel = GPy.kern.RBF(d, var, theta)

# Original
#m = GPy.models.GPRegression(X,Y,kernel)
#
# Zach modefication:
m = GPy.models.SparseGPRegression(X,Y,kernel)


fig = m.plot()
GPy.plotting.show(fig, filename='basic_gp_regression_notebook')
display(m)

m.optimize(messages=True)
m.optimize_restarts(num_restarts = 10)

fig = m.plot()
GPy.plotting.show(fig, filename='basic_gp_regression_notebook_optimized')
display(m)

# fig = m.plot(plot_density=True)
# GPy.plotting.show(fig, filename='basic_gp_regression_density_notebook_optimized')
# display(m)

m.predict(m.X)

Xp = np.arange(0.1,2.5,0.002).reshape(-1,1)
Yp = m.predict(Xp)

plt.axis([0, 1.5, -3, 15])
plt.plot(Xp,Yp[0])
plt.show()

Dataout = np.column_stack((Xp,Yp[0]))
np.savetxt('CGPotential.dat',(Dataout),fmt=('%10.5f', '%12.6f'))
