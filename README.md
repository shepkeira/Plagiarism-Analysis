# Plagiarism-Analysis

## Set Up
```
pip install os
pip install re
pip install pathlib
pip install csv
```

## Files
All code can be found in main.py
build_n_grams(files) takes in a dictionary of file names, and file paths {file_name: file_path} and returns a dictionary of n_grams for each file
{filename: {
    n: [n-grams]
}}

It will also write all this into a file "ngrams-per-file.txt"

calculate_set_containment(file_n_n_grams) takes in the output of build_n_grams and a list of file names and returns all the values of cvals

It will also write all this into a file "cvals.csv"

The answer to the questions can be found in answers.txt

The input files are found in the directory data