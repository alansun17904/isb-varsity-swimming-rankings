#!/bin/bash
# Alan Sun
# Main Program for ISB Varsity Swimming Ranking
# 11/21/2021

echo The hyperparameters that are going to be given to the ranker:
echo 
cat hyperparameters.settings
echo 
echo The bonus matrix that is given to the ranker:
echo
cat bonus-matrix.settings
echo

echo The ranker will now start...
echo At any point if you wish to stop press \(ctrl-C\)
echo
python3 src/main.py
