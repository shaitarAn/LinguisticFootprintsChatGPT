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

            python3 truncate_files.py

            python3 extract_features.py -c $corpus --params $params

            python3 average_dataframes.py -c $corpus --params $params

            python3 compare_features.py -c $corpus

            python3 combine_pngs.py

            echo "----------------------"

        done
    done
done

# for corpus in 'pubmed_de' 'ggponc' 'cnn' 'pubmed_en' 'e3c' '20min'
        
#         do

#             echo "Running $corpus"
#             # python3 generate.py -t $temp -fp $fp -c $corpus

#             python3 extract_features.py -c $corpus --params $params

#             python3 average_dataframes.py -c $corpus --params $params

#             python3 compare_features.py -c $corpus

            

#             echo "----------------------"

#         done