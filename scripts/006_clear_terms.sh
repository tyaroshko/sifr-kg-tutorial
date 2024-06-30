#!/bin/sh

data_dir=../data
python3  \
   006_clear_terms.py \
       --config=$data_dir/config.ini \
       --in_dir_terms=$data_dir/terms_merged \
       --out_dir_terms=$data_dir/terms_merged_clear \
       --stopwords=$data_dir/noisy_terms.txt  \
       --trace=0
