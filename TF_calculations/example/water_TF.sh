#!/usr/bin/env bash

A1=$1
A2=$2

if [ $# -lt 1 ] ; then
  echo "Usage: water_TF.sh <Coordinate file in PDB format> <XTC file from GROMACS>"
  exit 1
fi

cp $A1 AA.pdb
cp $A2 AA.xtc

python ../scripts/Gaussian_1D_density_V3.py
python ../scripts/GPy_TF.py

rm AA.pdb
rm AA.xtc
