# sifr-kg-tutorial

This repository contains the code and data for the tutorial on Scientific Knowledge Graphs at UCU SIFR.

### Environment Setup

1. Clone the repository
```bash
git clone https://github.com/tyaroshko/sifr-kg-tutorial
cd sifr-kg-tutorial/
```

2. Install the required packages

- using `venv`
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- using `conda`
```bash
conda create --name sifr-kg-tutorial python=3.10
conda activate sifr-kg-tutorial
pip install -r requirements.txt
```

3. Get the necessary data
```bash
bash download_data.sh
```


### Pipeline Overview

The pipeline consists of the following steps:

1. `000_preprocess_data.py`: Preprocess the raw data from the text file and saves the individual emails in a separate directory.
2. `001_clear_txts.py`: Clean the text files by removing unwanted characters/patterns and save the cleaned text files.
3. `002_generate_partial_datasets.py`: Generate partial datasets from the cleaned emails by combining multiple emails into one dataset using a specified increment parameter.
4. `003_get_terms.py`: Extract the possible terms from the partial datasets.
5. `004_merge_terms.py`: Merge the extracted terms so that each of the merged files contains a set of terms obtained before generating the incremental datasets (but only up to this point).
6. `005_get_initial_ate_saturation.py`: Get the initial saturation for the automatic term extraction on our dataset.
7. `006_clear_terms.py`: Perform denoising on the extracted terms in order to remove the unwanted terms.
8. `007_get_final_ate_saturation.py`: Perform the automatic term extraction on the cleaned terms and get the final saturation.
9. `008_scan_email.py`: Scan the emails for the extracted terms and label them accordingly (associate the emails with the terms present inside them).
10. `009_create_visualizations.py`: Create plots for visualization of ATE saturation pipeline.