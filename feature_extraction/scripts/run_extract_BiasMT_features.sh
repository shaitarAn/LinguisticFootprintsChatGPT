#!/bin/bash

INPUTDIR=$1
OUTPUTDIR=$2

# ###################################
# ### **Sophistication**

## Step 1: Concatenates all corpus files into one txt file in the data folder
bash concatenate_files.sh $INPUTDIR $OUTPUTDIR

## Step 2: Outputs ../$OUTPUTDIR/results/sophistication/sophistication_scores.csv
bash sophistication.sh $OUTPUTDIR

# ###################################
# ### **Lexical richness**

## Outputs ../$OUPUTDIR/results/lexical_richness/{corpus}.csv
bash lxr_scores.sh $INPUTDIR $OUTPUTDIR

# ###################################
# ### **Morphology** for the German corpora

## Step 1: Extract vocabulary of most frequent words
## Outputs ../$OUTPUTDIR/morphology/freq_voc/{corpus}/ 
bash create_most_freq_vocs.sh $INPUTDIR $OUTPUTDIR

## Step 2: Measure the surprisal levels within the inflectional paradigms of the German lemmas and Produce Shannon entropy and Simpson diversity metrics 
## Output1 ../$OUTPUTDIR/results/morphology/${corpus_name}.csv
## Output2 ../$OUTPUTDIR/morphology/lemmas/${corpus_name}/lemma_files
## Output3 ../$OUTPUTDIR/morphology/per_lemma/${corpus_name}/{perosona_counter}.csv

bash mrph_all.sh $INPUTDIR $OUTPUTDIR