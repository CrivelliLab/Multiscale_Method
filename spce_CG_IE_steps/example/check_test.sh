#!/usr/bin/env bash

A1=$1
A2=$2

if [ $# -lt 1 ] ; then
  echo "Usage: water_CG.com <GROfile> <Reference Residue Number>"
  exit 1
fi

cp $A1 aa.gro
perl check_test.pl $A2
