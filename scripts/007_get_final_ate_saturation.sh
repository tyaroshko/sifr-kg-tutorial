#!/bin/sh

data_dir=../data
python3 \
   007_get_final_ate_saturation.py \
       --config=$data_dir/config.ini \
       --in_dir=$data_dir/terms_merged_clear \
       --out_thd=$data_dir/thd_final.csv