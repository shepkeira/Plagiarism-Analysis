import re
import os
from pathlib import Path
import csv

PUNCTUATION = ['?', '.', '!']

def clear_files():
    here = os.path.dirname(Path("main.py").resolve())
    n_grams_file_path = os.path.join(here, 'ngrams-per-file.txt')
    csv_file_path = os.path.join(here, 'cvals.csv')
    with open(n_grams_file_path, 'w') as f:
        f.write("")
    with open(csv_file_path, 'w') as f:
        f.write("")

def main():
    clear_files()
    files = {}
    here = os.path.dirname(Path("main.py").resolve())
    file_path = os.path.join(here, 'data')
    file_names = os.listdir(file_path)

    for file_name in file_names:
        file_name_path = os.path.join(file_path, file_name)
        with open(file_name_path, 'r') as f:
            files[file_name] = f.read()
    file_n_n_grams = build_n_grams(files)
    cvals = calculate_set_containment(file_n_n_grams, file_names)


def calculate_set_containment(file_n_n_grams, file_names):
    num_files = len(file_names)
    cvals = []
    headers = ['A', 'B', 'C1(A,B)', 'C2(A,B)', 'C3(A,B)', 'C4(A,B)', 'C5(A,B)', 'C6(A,B)', 'C7(A,B)', 'C8(A,B)', 'C9(A,B)', 'C10(A,B)']
    cvals.append(headers)
    
    for file_a in range(0, num_files):
        file_a_n_grams = file_n_n_grams[file_names[file_a]]
        for file_b in range(0, num_files):
            file_b_n_grams = file_n_n_grams[file_names[file_b]]
            row = []
            row.append(file_names[file_a]) #file A
            row.append(file_names[file_b]) #file B
            for n in range(1, 11):
                file_a_n_n_grams = file_a_n_grams[n]
                file_a_n_n_grams_set = set(file_a_n_n_grams)
                file_b_n_n_grams = file_b_n_grams[n]
                file_b_n_n_grams_set = set(file_b_n_n_grams)
                denominator = len(file_a_n_n_grams_set.intersection(file_b_n_n_grams_set))
                numerator = len(file_b_n_n_grams_set)
                if numerator > 0:
                    cn = denominator/numerator
                else:
                    cn = 0
                row.append(cn) #Cn(A,B)
            cvals.append(row)
    here = os.path.dirname(Path("main.py").resolve())
    csv_file_path = os.path.join(here, 'cvals.csv')
    with open(csv_file_path, 'w') as f:
        writer = csv.writer(f)
        for row in cvals:
            writer.writerow(row)
    return cvals

def write_to_file(str):
    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, 'ngrams-per-file.txt')
    with open(file_path, 'a') as f:
        f.write(str)
        f.write('\n')


def build_n_grams(files):
    file_n_n_grams = {}
    for k, v in files.items():
        write_to_file(str(k))
        sentences = re.split('[.!?]', v)
        n_n_grams = {}
        for n in range(1, 11):
            n_grams = []
            for sentence in sentences:
                lower_case_sentence = sentence.lower()
                no_punctuation_sentence = re.sub(r'[^A-Za-z0-9 ]+', '', lower_case_sentence)
                words = no_punctuation_sentence.split(" ")
                words = [word for word in words if word != '']
                
                start = 0
                end = n
                
                range_end = len(words)-n+1 #all the words, but stop when we get the end on of the sentence adjusted because indexing from 0
                for start in range(0, range_end):
                    n_gram = words[start:end]
                    n_grams.append(' '.join(n_gram))
                    end += 1
            if(n_grams):
                write_to_file(str(n_grams))
                n_n_grams[n] = n_grams
        file_n_n_grams[k] = n_n_grams
    return file_n_n_grams
        
if __name__ == "__main__":
    main()