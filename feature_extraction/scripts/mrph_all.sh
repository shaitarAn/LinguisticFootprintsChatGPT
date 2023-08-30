#!/bin/bash

# Check if at least two arguments were provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 corpus_directory language"
    exit 1
fi

DATADIR="$1"
lang="$2"

dataset=$(basename "$DATADIR")

outdir=../results/morphology/${dataset}

mkdir -p $outdir

# iterate through a directory of files
for system in human machine; do
  echo "${system}"
  for file in $DATADIR/${system}/*; do
    file_name=$(basename "$file" .txt)
    echo "${file_name}"
    python mrph_calculate.py -f ${file} -l $lang -sys "${system}_$file_name" -dat "${dataset}" -v "freq_voc/${dataset}/${system}_${file_name}.freq_voc" -t 0 > "${outdir}/${system}_$file_name.txt"
  done
done
