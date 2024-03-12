#!/bin/bash

#  pilot with parameters

for temp in 1.0 0.7 0.0 
do
    for fp in 1.0 0.0
    do
        params=$temp\_$fp
        echo "Running $params"
        for corpus in 'cs_en' 'cs_de' 'ggponc' '20min' 'pubmed_de' 'pubmed_en' 'ggponc' 'cnn' 'e3c' '20min' 'zora_en' 'zora_de'
        do

            echo "Running $corpus"

            output_folder="../output/pilot_raw"

            mkdir -p $output_folder
            python3 generate_personas.py -t $temp -fp $fp -c $corpus -i "~/switchdrive/IMAGINE_files/chatGPT/project_2_gpt_personas/tests/5_files_json/" -o $output_folder

            mkdir -p ../output/pilot_truncated
            pytyhon3 truncate_files.py -i $output_folder -o ../output/pilot_truncated

        done
    done
done

## without parameters

for corpus in 'cs_en' 'cs_de' 'pubmed_de' 'ggponc' 'cnn' 'pubmed_en' 'e3c' 'zora_en' 'zora_de' '20min'
        
        do

            echo "Running $corpus"

            mkdir -p ../output/raw
            python3 generate_personas.py -c $corpus -i "~/switchdrive/IMAGINE_files/chatGPT/project_2_gpt_personas/tests/100_files_json/" -o "../output/raw"

            mkdir -p ../output/truncated
            python3 truncate_files.py -i "../output/raw" -o "../output/truncated"

        done