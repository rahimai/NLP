#! /usr/bin/python3

#no rare tags so what happens if a tag is unseen in training

from collections import defaultdict
import math

def emission_calculator(counts_trigram, counts_bigram):
    prob_list = {}
    for key3, key2, key1 in counts_trigram:
        prob_list[(key3, key2, key1)] = counts_trigram[(key3, key2, key1)] / counts_bigram[(key3, key2)]
    return prob_list


if __name__ == "__main__":
    #read in training data line by line and add words to dictionary
    with open('ner_rare.counts') as file_iterator:
        data = file_iterator.readlines()

    file_array = [(k.strip()).split(" ") for k in data]
    count_trigram = {}
    count_bigram = {}




    for vec in file_array:
        if vec[1] == '3-GRAM':
            count_trigram[(vec[-3], vec[-2], vec[-1])] = int(vec[0])
        elif vec[1] == '2-GRAM':
            count_bigram[(vec[-2], vec[-1])] = int(vec[0])

    prob_list = emission_calculator(count_trigram, count_bigram)

    with open('trigrams.txt') as file2_iterator:
        data2 = file2_iterator.readlines()

    file_array = [tuple((k.strip()).split(" ")) for k in data2]

    results = []
    for tag in file_array:
        results.append(" ".join(tag) + " " + str(math.log(prob_list[tag])) + "\n")

    with open('5_1.txt', 'w') as w_iterator:
        for res in results:
            w_iterator.write(res)


