#!/bin/sh

data_dir=../data
python3 \
     004_merge_terms.py \
         --config=$data_dir/config.ini \
         --dir_in_terms=$data_dir/terms_partial  \
         --dir_out_terms=$data_dir/terms_merged \
         --trace=0
