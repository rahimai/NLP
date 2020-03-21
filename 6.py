#! /usr/bin/python3

#no rare tags so what happens if a tag is unseen in training
#not seen trigrams and bigrams in training data can lead to poor results

from collections import defaultdict
import math
import time

def q_calculator(counts_trigram, counts_bigram):
    prob_list = {}
    for key3, key2, key1 in counts_trigram:
        prob_list[(key1, key3, key2)] = math.log(counts_trigram[(key3, key2, key1)] / counts_bigram[(key3, key2)])
    return prob_list

def emission_calculator(count_follow, count):
    emissions = {}
    for tag, word in count_follow:
        emissions[(word, tag)] = math.log(count_follow[(tag, word)]/count[tag])
    return emissions

if __name__ == "__main__":
    #read in training data line by line and add words to dictionary
    with open('ner_rare_updated.counts') as file_iterator:
        data = file_iterator.readlines()

    file_array = [(k.strip()).split(" ") for k in data]
    count_trigram = {}
    count_bigram = {}
    count = {}
    count_follow = {}
    tags = {}



    #calculate the q values
    for vec in file_array:
        if vec[1] == '3-GRAM':
            count_trigram[(vec[-3], vec[-2], vec[-1])] = int(vec[0])
        elif vec[1] == '2-GRAM':
            count_bigram[(vec[-2], vec[-1])] = int(vec[0])
        elif vec[1] =='1-GRAM':
            count[(vec[2])] = int(vec[0])
        elif vec[1] == 'WORDTAG':
            count_follow[(vec[2], vec[3])] = int(vec[0])
            if vec[-1] in tags:
                tags[vec[-1]].append(vec[-2])
            else:
                tags[vec[-1]] = [vec[-2]]


    q_list = q_calculator(count_trigram, count_bigram)
    emissions = emission_calculator(count_follow, count)

    #get the rare_words list
    with open('ner_train_rare_updated.dat') as rare_iterator:
        rare = rare_iterator.readlines()
    all_symbols = [(r.strip()).split(" ") for r in rare]
    rare_list = set([part[0] for part in all_symbols if part[0] != ""])


    #split sentences
    sentences = []
    with open("ner_dev.dat") as read_iterator:
        l = read_iterator.readline()
        sub_array = []
        while l:
            line = l.strip()
            if line != "":
                sub_array.append(line)
            else:
                sentences.append(sub_array)
                sub_array = []
            l = read_iterator.readline()

    import copy
    original_sentences = copy.deepcopy(sentences)

    punct = [',', '.', ':', ';']

    for sub in sentences:
        sub.insert(0, '*')
        sub.insert(0, '*')
        for k in range(len(sub)):
            if sub[k] not in rare_list:
                if sub[k].isupper():
                    sub[k] = '_UPPER_'
                elif sub[k][0].isupper():
                    sub[k] = '_FCAP_'
                elif sub[k] in punct:
                    sub[k] = '_PUNC_'
                else:
                    sub[k] = '_RARE_'
        sub.append('STOP')



    output = []

    lambdafunction = lambda word, i: tags[word] if i >= 2 else ['*']



    for j, sen in enumerate(sentences):
        q_acc = []
        table = {}
        backp = {}
        table[(1, '*', '*')] = 1
        for k in range(2, len(sen)-1):
            for u in lambdafunction(sen[k-1], k-1):
                for v in lambdafunction(sen[k], k):
                    max = -99999
                    w_opt = 'K'
                    for w in lambdafunction(sen[k-2], k-2):
                        if (sen[k], v) in emissions and (v, w, u) in q_list and (k-1, w, u) in table:
                            temp = table[(k-1, w, u)] + q_list[(v, w, u)] + emissions[(sen[k], v)]
                        else:
                            continue
                        if temp > max:
                            max = temp
                            w_opt = w

                    table[(k, u, v)] = max
                    backp[(k, u, v)] = w_opt



        tag_list = ['G'] * (len(sen)-1)
        max2 = -9999999
        for u in lambdafunction(sen[len(sen)-3], len(sen)-3):
            for v in lambdafunction(sen[len(sen)-2], len(sen)-2):
                 if ('STOP', u, v) in q_list and (len(sen)-2, u, v) in table:
                     tempo = table[(len(sen)-2, u, v)] + q_list[('STOP', u, v)]
                     if tempo > max2:
                         max2 = tempo
                         u_opt = u
                         v_opt = v

        tag_list[-1] = v_opt
        tag_list[-2] = u_opt



        for m in range(len(sen)-4, 1, -1):
            tag_list[m] = backp[(m+2, tag_list[m+1], tag_list[m+2])]



        tag_list[0] =  '*'
        tag_list[1] =  '*'
        tag_list.append('STOP')

        for k in range(2, len(sen)-1):
            if not q_acc:
                q_acc.append(q_list[(tag_list[k], tag_list[k-2], tag_list[k-1],)] + emissions[(sen[k], tag_list[k])])
            else:
                q_acc.append(q_acc[k-3] + q_list[(tag_list[k], tag_list[k-2], tag_list[k-1])] + emissions[(sen[k], tag_list[k])])


        tag_list.pop(0)
        tag_list.pop(0)
        tag_list.pop()


        sen.pop()
        sen.pop(0)
        sen.pop(0)

        for i in range(0, len(sen)):
            if sen[i] in ['_RARE_', '_UPPER_', '_FCAP_', '_PUNC_']:
                sen[i] = original_sentences[j][i]



        zipped = list(zip(sen, tag_list))
        result = [zipped[k][0] + " " + zipped[k][1] + " " + str(q_acc[k]) + "\n" for k in range(0, len(zipped))]
        output.append(result)


    with open('6.txt', 'w') as write_iterator:
        for sen in output:
            for word in sen:
                write_iterator.write(word)
            write_iterator.write("\n")
