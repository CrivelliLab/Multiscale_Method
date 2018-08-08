#!/usr/bin/env bash

#A1=$1
#A2=$2

#if [ $# -lt 1 ] ; then
#  echo "Usage: water_CG.com <GROfile> <Reference Residue Number>"
#  exit 1
#fi
gmx make_ndx -f conf_cg.gro -o CG.ndx < CG.txt
gmx grompp -f CG.mdp -c conf_cg.gro -p topol_CG.top -n CG.ndx -o CG.tpr
gmx mdrun -v -s CG.tpr
echo 0 | gmx trjconv -f traj_comp.xtc -s CG.tpr -o cg_centered.xtc -pbc mol
