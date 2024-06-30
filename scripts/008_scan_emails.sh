#!/bin/sh

data_dir=../data
python3 \
   008_scan_emails.py \
       --concepts_file=$data_dir/conceptualization.txt \
       --input_dir=$data_dir/clear_txts  \
       --output_file=$data_dir/email_concepts_data.json
