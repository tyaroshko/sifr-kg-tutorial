#!/bin/sh

data_dir=../data
python3 \
   009_create_visualizations.py \
       --input_file=$data_dir/email_concepts_data.json \
       --output_dir=$data_dir/plots
