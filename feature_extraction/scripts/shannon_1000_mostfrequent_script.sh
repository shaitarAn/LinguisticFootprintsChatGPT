#!/bin/bash

# bash shannon_1000_mostfrequent_script.sh ~/switchdrive/IMAGINE_files/astred_results/merged_on_orig/*

#choose target language and corpus suffix
LANG="de"
CORPUS="_csbull"

for i in "$@"

do

#extract file name
one=${i#*orig/}
file=${one%*.csv*}
SYST=${file#*en-}

echo ${one}
echo ${file}
echo ${SYST}
echo ${CORPUS}
  python3 shannon_pairwise.py -f ${i} -l $LANG -sys "${SYST}${CORPUS}" -v freq_voc/${file}.freq_voc > results_shannon/1000mostfrequent_${file}.out

done
