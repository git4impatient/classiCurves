#!/usr/bin/bash
# (C) copyright 2018 Martin Lurie   Sample code, not supported
#
#
#export NUMROWS=10000000
#./gendata.py 1000000 > mydata.txt
#ls -l

hadoop fs -rm -r  /tmp/logicurvesSVM
#!hadoop fs -mkdir   s3a://cdp-sandbox-default-se/datalake/marty/logicurves
hadoop fs -mkdir /tmp/logicurvesSVM
#!python 200gencurves.py | gzip >logicurves.gz 
#hadoop fs -put - s3a://cdp-sandbox-default-se/datalake/marty/logicuves/logicuves.gz
# no local store go direct to S3

# svm format can't read a gz file !python 210gencurvesSVM.py | gzip | hadoop fs -put -   s3a://cdp-sandbox-default-se/datalake/marty/logicurvesSVM/logicurvesSVM.gz

python 210gencurvesSVM.py | hadoop fs -put -   /tmp/logicurvesSVM/logicurvesSVM

#!hadoop fs -put logicurves.gz  s3a://cdp-sandbox-default-se/datalake/marty/logicurves

hadoop fs -ls /tmp/logicurvesSVM


