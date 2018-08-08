#

import numpy as np

InFileName = 'table_CG_CG.xvg'
f = open(InFileName, 'r')
N = len(f.readlines())  # number of observed points.
f.close()

R  = np.zeros(shape=(N,1))
X  = np.zeros(shape=(N,1))
Y  = np.zeros(shape=(N,1))
X0 = np.zeros(shape=(N,1))
#------------------------------------
# Open the file and read data points from the file

InFile = open(InFileName, 'r')
LineNumber = 0
for Line in InFile:
    #Remove the lin-ending characters
    Line = Line.strip('\n')
    row = Line.split()
    #Index the counter used to keep track of line number
    R[LineNumber] = float(row[0])
    X[LineNumber] = float(row[5])
    Y[LineNumber] = -1 * float(row[6])
    LineNumber += 1
#After the loop is completed., close the file
InFile.close()
# -----------------------------------

Dataout = np.column_stack((R,X0,X0,X0,X0,X,Y))
np.savetxt('AA.dat',(Dataout),fmt=('%12.10e ', ' %12.10e ', ' %12.10e ',' %12.10e ', ' %12.10e ', ' %12.10e ',' %12.10e '))

Dataout1 = np.column_stack((R,X0,X0,X0,X0,X0,X0))
np.savetxt('table.xvg',(Dataout),fmt=('%12.10e ', ' %12.10e ', ' %12.10e ',' %12.10e ', ' %12.10e ', ' %12.10e ',' %12.10e '))
