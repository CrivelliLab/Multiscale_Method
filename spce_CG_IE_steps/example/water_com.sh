#!/usr/bin/env bash

A1=$1
A2=$2

if [ $# -lt 1 ] ; then
  echo "Usage: water_CG.com <GROfile> <Reference Residue Number>"
  exit 1
fi

cp $A1 aa.gro
perl ../scripts/energy_distance.pl $A2
python ../scripts/GPy_3z.py
python ../scripts/RtoPy2.py 
python ../scripts/table.py
mv AA.dat table_CG_CG.xvg
python ../scripts/mapping.py
mv fileout.gro conf_cg.gro
rm aa.gro
