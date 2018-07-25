#!/bin/bash
#largest is the latest model
cp /home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/tokenized_text.txt /home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/TnT
cd /home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/TnT
./tnt largest tokenized_text.txt > /home/sid/icfoss/ICFOSS-KeyWord-Extractor/POSTagging/tagged_text.txt
