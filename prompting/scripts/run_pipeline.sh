#!/bin/bash

#  example: ./run_pipeline.sh 

for temp in 0.0 0.7 1.0 
do
    for fp in 0.0 1.0
    do
        params=$temp\_$fp
        echo "Running $params"
        for corpus in 'pubmed_de' 'ggponc' 'cnn' 'pubmed_en' 'e3c' '20min' 'zora_en' 'zora_de'
        do

            echo "Running $corpus"
            python3 generate.py -t $temp -fp $fp -c $corpus

            echo "truncating files ----------------------" 

            python3 truncate_files.py

            echo "extracting features ----------------------"

            python3 extract_features.py -c $corpus --params $params

            echo "averaging dataframes ----------------------"

            python3 average_dataframes.py -c $corpus --params $params

            echo "comparing features ----------------------"

            python3 compare_features.py -c $corpus

            echo "combining pngs ----------------------"

            python3 combine_pngs.py

            echo "----------------------"
            echo "----------------------"

        done
    done
done

## without parameters

# for corpus in 'pubmed_de' 'ggponc' 'cnn' 'pubmed_en' 'e3c' '20min' 'zora_en' 'zora_de'
        
#         do

#             echo "Running $corpus"

#             echo "comparing features ----------------------"

#             python3 compare_features.py -c $corpus
            
#             echo "combining pngs ----------------------"

#             python3 combine_pngs.py
            
#             echo "----------------------"

#         done