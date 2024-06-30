#!/bin/sh

data_dir=../data
python3 \
   001_clear_txts.py --config=$data_dir/config.ini \
                   --rawtxtdir=$data_dir/txts \
                   --cleartxtdir=$data_dir/clear_txts
