#!/bin/sh

data_dir=../data
python3 \
   003_get_terms.py \
       --config=$data_dir/config.ini \
       --in_dir_dataset=$data_dir/datasets_partial \
       --out_dir_terms=$data_dir/terms_partial  \
       --stopwords=$data_dir/ate_stopwords.csv  \
       --trace=0