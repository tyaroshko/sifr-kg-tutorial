#!/bin/sh

data_dir=../data
python3 \
   009_create_visualizations.py \
       --file_path=$data_dir/email_concepts_data.json
