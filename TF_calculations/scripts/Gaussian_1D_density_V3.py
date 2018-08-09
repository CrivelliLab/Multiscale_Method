#
# Python - 1-D Density Profile 
# Convoluting the position of the center of mass of a molecule with a Gaussian function
# Reading trajectory files from GROMACS
# 
# Masa Watanabe - 
# Berkeley National Lab, Summer 2018
# University of Saint Mary
# Version 0.3
#

import numpy as np
import scipy.integrate as integrate
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
import math
import mdtraj as md

#import time
#import sys
#s = '.'
#sys.stdout.write( 'working' )
#while True:
#        sys.stdout.write( s )
#        sys.stdout.flush()
#        time.sleep(0.5)


def integrand(x, x00, sig):
    return np.exp(-(x-x00)**2/(2*sig**2))

#
# MDTraj is a python library that allows users to manipulate molecular dynamics (MD) trajectories. 
#
# t = md.load('trajectory.xtc', top='trajectory.pdb')
# To get all atributes: 
# dir(traj)

traj = md.load('AA.xtc',top="AA.pdb")


mass = 1 #18.0

#s = 0.05
s = 0.5  # associated with the typical excluded volume radisu of the molecules
N = 25

cutoff = 100 #(2.5 * s)**2

#A = integrate.quad(integrand, -2.5*s, 2.5*s,args=(0,s))[0]
B = integrate.quad(integrand, -math.inf, math.inf,args=(0,s))[0]

Xp = np.arange(-2.0,2,0.01).reshape(-1,1)
Yp = integrand(Xp,0,s)/B

#AA = integrate.quad(integrand,-0.5,0.5,args=(0,s))[0]/B
plt.plot(Xp,Yp)
plt.show()

#print (B,AA)

Box =[]
Box = np.ndarray.tolist(traj.unitcell_lengths[0])
print ("\nDimensitons of Simulation box = ", Box)
print ("\nNumbers of molecules in the system       = ", traj.n_residues)
print ("\nNumbers of frames in the trajectory file = ", traj.n_frames)

boxlx = float(Box[0])

hboxx = 0.5 * boxlx

binx = boxlx/float(N)

Vol = float(Box[1])*float(Box[2])*binx

Xp = np.arange(0,boxlx,binx).reshape(-1,1)
X = []
for i in range(0,len(Xp)-1):
    aa = [Xp[i],Xp[i+1]]
    bb = Xp[i+1]
    X.append(aa)
bb = Xp[len(Xp)-1]
aa=[bb,boxlx]
X.append(aa)
    

Cube = []
for i in range(0,N):
    aa = [i]
    Cube.append(aa)

#           
# Denisty calculation by Gaussian paticle method
#

Rho = []

cg_index = traj.topology.select('name CG')

#xyz = traj.xyz[3,traj.topology.select('name CG')]

for j in range(0,traj.n_frames):
    
    print("Frame = ",j+1)
    
    xyz = traj.xyz[j,traj.topology.select('name CG')]
    
    for i in range(0,len(Cube)):
        
        resultx = 0.0
    
        rho = 0.0
    
        xi = X[Cube[i][0]][0]
        xi1 = X[Cube[i][0]][1]
        xhalf = (xi + xi1)/2
     
        rcut = (0.5*(xi - xi1))**2
    
        rr = (xhalf - hboxx)**2
        
        for x in xyz: #gro_atoms:
            
            x0  = float(x[0])
            dx = x0 - xhalf
            dx = dx - int(dx / boxlx) * boxlx
        
            r2 = (dx)**2
        
            if(r2 < (rcut + cutoff)):
                #print (r2)
                resultx0 = integrate.quad(integrand, xi, xi1,args=(x0,s))
                resultx1 = integrate.quad(integrand, xi, xi1,args=(x0-boxlx,s))
                resultx2 = integrate.quad(integrand, xi, xi1,args=(x0+boxlx,s))
                
                resultx = (resultx0[0] + resultx1[0] + resultx2[0])/B
                
            #resultx = (resultx0[0])/B
            
            rho = rho + resultx
    
        #print(i, float(rr), rho)
        aa=[i,float(rr),rho]
        Rho.append(aa)
    
#
# Sorting the Rho data by distance from the center of the box
#

N1 = len(Rho)
R = np.zeros(shape=(N1,1))
D = np.zeros(shape=(N1,1))

LineNumber = 0

for line in Rho:
    R[LineNumber] = round(float(line[1]),4)
    D[LineNumber] = round(float(line[2]),5)
    LineNumber += 1

unique, counts = np.unique(R, return_counts=True)
#print (dict(zip(unique, counts)))

Final_rho = []

RQ = np.zeros(shape=(len(unique),1))
DQ = np.zeros(shape=(len(unique),1))
LineNumber = 0

for i in range(0,len(unique)):
    R0 = unique[i]
    # numbers: 
    # Odd # - center box count once; other boxes count more than once
    # Even # - all boxes count multiple time b/c here R0 is a distance from the center of box
    #
    d = np.sum(D[np.where(R == R0)])/float(counts[i])
    bb = round(d/Vol,5)
    RQ[LineNumber] = math.sqrt(R0)
    DQ[LineNumber] = bb #/float(traj.n_frames)
    aa = [math.sqrt(R0),mass*bb]
    Final_rho.append(aa)
    LineNumber += 1

    
RQx = np.concatenate(RQ)
DQx = np.concatenate(DQ)
f2 = interp1d(RQx, DQx, kind='cubic')

xnew = np.linspace(0, 1.9, num=51, endpoint=True)

plt.scatter(RQ,DQ)
plt.plot(xnew,f2(xnew))
plt.show()

mean = np.mean(DQ)
sd   = np.std(DQ)

print ("\nmean density  = ", mean)
print ("\nSTD (density) = ", sd)

#print (Final_rho)
Dataout = np.column_stack((xnew,f2(xnew)))
np.savetxt('Density.dat',(Dataout),fmt=('%10.5f', '%12.6f'))

