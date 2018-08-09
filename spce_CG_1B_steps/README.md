## Tools to generate a 1-Bead Coarse-Grained potentials from Radical distribution function.

All necessary scripts to generate the potentials are in ./scripts directory. 


Also, here we have included an example to build one site water CG potentials. 

## To run the example,

cd ./example

chmod +x water_CG.sh

./water_CG.sh water.gro gR_water.xvg

> Python scripts are expecting to read the coordinate file from GROMACS. 

> Note: by calling water_CG.sh, the script will automatically run the following scripts: 
* cp xxxx.gro aa.gro
* python GPy_rdf3.py    # accepting xvg format of RDF file
* R CMD BATCH Non-linear_Regression_2.R
* python table.py
* mv AA.dat table_CG_CG.xvg
* python mapping_2.py


## Testing:
To test your generated CG potentials by GROMACS, you can use the followings:

GROMACS MD Run:

gmx make_ndx -f CG.gro -o CG.ndx

> a CG

> q

gmx grompp -f CG.mdp -c CG.gro -p CG.top -n CG.ndx -o CG.tpr

gmx mdrun -v -s CG.tpr

vmd CG.gro traj_comp.xtc  


Analysis:

gmx rdf -f traj_comp.xtc -o gR_C.xvg -s CG.tpr -selrpos whole_mol_com -seltype whole_mol_com -bin 0.01 -n CG.ndx -sel CG -ref CG

xmgrace gR_C.xvg

## Required Libraries:
* Python
> numpy

> GPy (https://sheffieldml.github.io/GPy/)

> Ipython

> matplotlib

> math

> groio (https://pypi.org/project/groio/)

> xml

* R

## NOTE: 
You can generate your own RDF from regular atomistic simulation of GROMACS:

gmx rdf -f atomistic_traj.xtc -o gR_C.xvg -s md.tpr -selrpos whole_mol_com -seltype whole_mol_com -bin 0.01

