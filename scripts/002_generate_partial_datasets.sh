#!/bin/sh

data_dir=../data
python3 \
   002_generate_partial_datasets.py --input_folder=$data_dir/clear_txts \
                   --output_folder=$data_dir/datasets_partial \
                   --increment_size=200
