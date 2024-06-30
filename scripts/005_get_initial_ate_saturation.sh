#!/bin/sh

data_dir=../data
python3 \
   005_get_initial_ate_saturation.py \
       --config=$data_dir/config.ini \
       --in_dir=$data_dir/terms_merged \
       --out_thd=$data_dir/thd_initial.csv