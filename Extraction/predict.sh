#!/bin/bash
cd /home/sid/icfoss/ICFOSS-KeyWord-Extractor/Features
cp features.txt /home/sid/icfoss/ICFOSS-KeyWord-Extractor/CRF
cd /home/sid/icfoss/ICFOSS-KeyWord-Extractor/CRF
crf_test -m crfnew features.txt > output.txt
cp output.txt /home/sid/icfoss/ICFOSS-KeyWord-Extractor/Extraction
