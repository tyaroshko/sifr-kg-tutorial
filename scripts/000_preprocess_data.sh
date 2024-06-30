#!/bin/sh

data_dir=../data
python3 \
   000_preprocess_data.py \
       --input_file=$data_dir/2010.txt  \
       --output_dir=$data_dir/txts