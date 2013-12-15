#!/usr/local/bin/python

# Parameter 1: filename, in the form of BRCA00XX
# Parameter 2: sample_type, either "normal" or "tumor"
# Parameter 3: option, either "stat" or "fastq"
# E.g. python filter_aux.py BRCA0001 normal stat
#      python filter_aux.py BRCA0010 tumor fastq

import re
import sys

def ReadFile(filename):
    # data_list structure:
    # [read_1, read_2, read_3, ...]
    data_list = []
    f = open(filename)
    file_content = map(lambda x: x.rstrip("\n"), f.readlines())
    f.close
    for each_line in file_content:
        data_list.append(each_line)
    return data_list

def TelomereReadScreening(data_list, printout=False):
    # telomere_repeat = re.compile("(TTAGGG[ATGC]??)|(CCCTAA[ATGC]??)")
    telomere_repeat = re.compile("TTAGGG|CCCTAA")
    selected_count = 0
    unselected_count = 0
    for line in data_list:
        sequence = line.split()[9]
        total_read_length = 1.0 * len(sequence)
        telomere_repeat_num = 0.0
        e = -1
        small_interval = True
        for match in re.finditer(telomere_repeat, sequence):
            # no gap larger than 4 repeats of (6 + 1) nucleotides
            if match.start() > e + 7 * 4 and e != -1:
                small_interval = False
                break
            else:
                e = match.end()
            telomere_repeat_num += 1
        telomere_repeat_len = telomere_repeat_num * 6.0
        telomere_ratio = 1.0 * telomere_repeat_len / total_read_length
        # telomere_ratio >= 0.6
        if small_interval == True and telomere_ratio >= 0.5:
            #TestPatterns(sequence, [(telomere_repeat, "Telomere repeat")])
            if printout:
                print line
            selected_count += 1
        else:
            #TestPatterns(sequence, [(telomere_repeat, "Telomere repeat")])
            unselected_count += 1
    return selected_count, unselected_count

filename = sys.argv[1]
sample_type = sys.argv[2]
option = sys.argv[3]
result = []
filepath = "//N//dcwan//projects//ngs//users//liren//201301_TCGA//all_reads//"
data_list = ReadFile(filepath + filename + "." + sample_type + ".all.t2c2.fastq")
if option == "fastq":
    TelomereReadScreening(data_list, True)
elif option == "stat":
    print filename, sample_type, TelomereReadScreening(data_list, False)
