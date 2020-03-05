#! /usr/bin/python3

from collections import defaultdict
import time

if __name__ == "__main__":

    with open('ner_train.dat') as file_iterator:
        lines = file_iterator.readlines()

    data = [(lines[k].strip()).split(" ") for k in range(len(lines))]

    count_list = {}

    for vec in data:
        if vec[0] not in count_list:
            count_list[vec[0]] = 1
        else:
            count_list[vec[0]] += 1





    #Filter rare words
    rare_words = [k for k, v in count_list.items() if v < 5]
    rare_words = set(rare_words)

    array_file = []

    for elem in data:
        if elem[0] in rare_words:
            elem[0] = '_RARE_'

        pair = " ".join(elem) + "\n"
        array_file.append(pair)



    with open('ner_train_rare.dat', 'w') as handle:
        for elem in array_file:
            handle.write(elem)











