## Calculation for Thermodynamics Force to blance the density profile in the AdResS system.

Simple tools to generate Thermodyanamic force for the AdResS method.

All necessary scripts to generate the potentials are in ./scripts directory. Since all necessary tools are written in Python, you can call these codes from ESPResSo++ program.

Also, here we have included an example to calculate TF from a water simulation trajectory. 

To run the example,

> cd ./example

> chmod +x water_TF.sh

> ./water_CG.sh water.pdb water.xtc


### Note:
> In order to use these tools, users need to generate xtc format trajectory files from GROMACS and a pdb coordinate file for topology. 

