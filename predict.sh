#!/bin/bash
#kw_extractor,newmodel,newcrf,testmodel

cd /home/sid/icfoss/ICFOSS-KeyWord-Extractor/Features
cp features.txt /home/sid/icfoss/ICFOSS-KeyWord-Extractor/CRF
cd /home/sid/icfoss/ICFOSS-KeyWord-Extractor/CRF
crf_test -m kwnew features.txt > output.txt
cp output.txt /home/sid/icfoss/ICFOSS-KeyWord-Extractor/Extraction
