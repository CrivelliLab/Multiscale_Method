Tools to generate Coarse-Grained potentials from intermolecular interaction energy.

All necessary scripts to generate the potentials are in ./scripts directory. 


Also, here we have included an example to build water CG potentials. 


To run the example,

The following steps require GROMACS 5.1 or later to run the script. Please start by entering the command:
gmx -version

This command should print out information about the version of GROMACS installed. If this, in contrast, returns the phrase 

gmx: command not found.

Set-up Steps:
cd ./example

chmod +x water_com1.sh
chmod +x water_com2.sh

grep -v “energygrps “  grompp.mdp > AT.mdp
gmx grompp -f AT.mdp -c water.gro -p water.top -o run_prep.tpr
gmx make_ndx -f water.gro -o water.ndx
> del 2
> del 1
> q

Run the GP-CG Processing:

./water_com1.sh water.gro 100

Note: by calling water_com.sh, the script will automatically run the following codes: 
* perl energy_distance.pl
* python GPy_2z.py
* python RtoPy2.py
* python table.py
* mv AA.dat table_CG_CG.xvg
* python mapping.py
* mv fileout.gro conf_cg.gro

MD Run:

./water_com2.sh

Note: by calling water_com2.sh, the script will automatically run the following codes: 
* gmx make_ndx -f conf_cg.gro -o CG.ndx < CG.txt
* gmx grompp -f CG.mdp -c conf_cg.gro -p topol_CG.top -n CG.ndx -o CG.tpr
* gmx mdrun -v -s CG.tpr
* gmx trjconv -f traj_comp.xtc  -s CG.tpr  -o cg_centered.xtc -pbc mol

Analysis:

vmd conf_cg.gro cg_centered.xtc


gmx rdf -f cg_centered.xtc -o gR_C.xvg -s CG.tpr -selrpos whole_mol_com -seltype whole_mol_com -bin 0.01 -n CG.ndx -sel CG -ref CG

xmgrace gR_C.xvg


