#! /usr/bin/python3

#rare is being tagged always wrt to maximum that is bloc

from collections import defaultdict
import math
import time

def emission_calculator(counts_emission, counts_tag):
    emission_list = {}
    for key1, key2 in counts_emission:
        emission_list[(key1, key2)] = counts_emission[(key1, key2)] / counts_tag[key2]
    return emission_list


if __name__ == "__main__":


    #read in training data line by line and add words to dictionary
    with open('ner_rare.counts') as file_iterator:
        data = file_iterator.readlines()

    file_array = [(k.strip()).split(" ") for k in data]

    count_emission = {}
    count_tag = {}
    words = []

    for vec in file_array:
        if vec[1] == 'WORDTAG':
            count_emission[(vec[-1], vec[2])] = int(vec[0])
            words.append(vec[-1])
        elif vec[1] == '1-GRAM':
            count_tag[vec[-1]] = int(vec[0])

    emission_dict = emission_calculator(count_emission, count_tag)


    with open("ner_dev.dat") as iterator:
        data2 = iterator.readlines()

    dev_array = [(k.strip()) for k in data2]



    intersection = set(words) & set(dev_array)



    results = []
    maxword = None
    maxtag = None



    for word in dev_array:
        if word == "":
            results.append(word + "\n")
            continue
        elif word not in intersection:
            search = '_RARE_'
        else:
            search = word
        max = -1
        for tag in count_tag:
            val = emission_dict.get((search, tag))

            if val is None:
                continue
            else:
                if val>max:
                    max = val
                    maxword = word
                    maxtag = tag
        if max>0:
            results.append(maxword + " " + maxtag + " " + str(math.log(max)) + "\n")



    

    with open('4_2.txt', 'w') as write_iterator:
        for elem in results:
            write_iterator.write(elem)


