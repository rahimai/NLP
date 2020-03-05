#! /usr/bin/python3

from collections import defaultdict
import time

if __name__ == "__main__":


    #Preallocate high performance container
    count_list = {}
    array_file = []
    punct = [',', '.', ':', ';']
    #read in training data line by line and add words to dictionary
    with open('ner_train.dat') as file_iterator:
        l = file_iterator.readline()
        while l:
             line = l.strip()
             if line:
                 # extract line information if line non-empty
                 fields = line.split(" ")
                 array_file.append(fields)
                 word = " ".join(fields[:-1])
                 if word not in count_list:
                     count_list[word] = 1
                 else:
                     count_list[word] += 1
             else:
                 array_file.append(line.split(" "))
             l = file_iterator.readline()

    #Filter rare words
    rare_words = set([k for k, v in count_list.items() if v < 5])

    for elem in array_file:
        if elem[0] in rare_words:
            if elem[0] == "":
                continue
            elif elem[0].isupper():
                elem[0] = '_UPPER_'
            elif elem[0][0].isupper():
                elem[0] = '_FCAP_'
            elif elem[0] in punct:
                elem[0] = '_PUNC_'
            else:
                elem[0] = '_RARE_'


    new_array = [" ".join(x) for x in array_file]

    with open('ner_train_rare_updated.dat', 'w') as handle:
        for elem in new_array:
            handle.write(elem+"\n")