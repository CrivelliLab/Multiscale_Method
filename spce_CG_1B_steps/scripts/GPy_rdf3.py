#
# Gaussian Process - for Coarse-Grain Potential Development
# Berkeley National Lab, Summer 2018
# University of Saint Mary
#

import numpy as np
from matplotlib import pyplot as plt
import GPy
from IPython.display import display
import math

d = 1 # input dimension
var = 1 # variance
theta = 1 # 0.2 # lengthscale

InFileName = 'aa.xvg'
N = 0
f = open(InFileName, 'r')
for line in f:
    li=line.strip()
    if (not li.startswith("#")) and (not li.startswith("@")):
        N += 1
f.close()

X = np.zeros(shape=(N,1))
Y = np.zeros(shape=(N,1))

LineNumber = 0
InFile = open(InFileName, 'r')
for line in InFile:
    li=line.strip()
    if (not li.startswith("#")) and (not li.startswith("@")):
        row = line.split()
        #Index the counter used to keep track of line number
        X[LineNumber] = float(row[0])
        Y[LineNumber] = float(row[1])
        LineNumber += 1
InFile.close()
# -----------------------------------

kernel = GPy.kern.RBF(d, var, theta)

#m = GPy.models.GPRegression(X,Y,kernel)
m = GPy.models.SparseGPRegression(X,Y,kernel)

#fig = m.plot()
#GPy.plotting.show(fig, filename='basic_gp_regression_notebook')
#display(m)

m.optimize(messages=True)
m.optimize_restarts(num_restarts = 10)

#fig = m.plot()
#GPy.plotting.show(fig, filename='basic_gp_regression_notebook_optimized')
#display(m)

# fig = m.plot(plot_density=True)
# GPy.plotting.show(fig, filename='basic_gp_regression_density_notebook_optimized')
display(m)

# m.predict(m.X)

Xp = np.arange(0.15,1.4,0.005).reshape(-1,1)
Yp = m.predict(Xp)

Vp = -np.log(Yp[0])

#print (Vp)
Xp1 = Xp[~np.isnan(Vp)]
Vp1 = Vp[~np.isnan(Vp)]

Dataout = np.column_stack((Xp1,2.4*Vp1))
np.savetxt('RDF_dat',(Dataout),fmt=('%10.5f', '%12.6f'))

#fig = m.plot()
plt.plot(Xp1,Vp1)
plt.show()
