#!/usr/bin/env bash

A1=$1
A2=$2

if [ $# -lt 1 ] ; then
  echo "Usage: water_CG.sh <Coordinate file in GRO format> <RDF file in xvg format>"
  exit 1
fi

cp $A1 aa.gro
cp $A2 aa.xvg

python ../scripts/GPy_rdf3.py
R CMD BATCH ../scripts/Non-linear_Regression_2.R
python ../scripts/table.py
mv AA.dat table_CG_CG.xvg
python ../scripts/mapping_2.py
rm Non-linear_Regression_2.Rout
