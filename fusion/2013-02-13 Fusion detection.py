#!/usr/local/bin/python
import re
import sys

def FileNameList():
    filename_normal, filename_tumor = [], []
    for i in range(1, 25):    
        if i <10:
            file_id = "BRCA000" + str(i)
        else:
            file_id = "BRCA00" + str(i)
        filepath = "C://seq//"
        filename_normal.append(filepath + file_id + ".normal.all.t2c2.fastq")
        filename_tumor.append(filepath + file_id + ".tumor.all.t2c2.fastq")
    return filename_normal, filename_tumor

def ReadFile(filename):
    print "# Reading file. #"
    # data_list structure:
    # {read_name:[n, [sequence_1, sequence_2]], read_name:[n, [sequence_1, sequence_2]]}
    data_list = {}
    f = open(filename)
    file_content = f.readlines()
    f.close
    for each_line in file_content:
        split_each_line = each_line.split()
        temp_name = split_each_line[0]
        temp_seq = split_each_line[9]
        if temp_name in data_list:
            data_list[temp_name][0] += 1
            data_list[temp_name][1].append(temp_seq)
        else:
            data_list[temp_name] = [1,[temp_seq]]
    print "# File reading complete. #"
    return data_list

def PairFilter(data_list):
    print "# Filtering pair reads. #"
    paired_read_list = {}
    for pair in data_list:
        if data_list[pair][0] == 2:
            paired_read_list[pair] = data_list[pair][1]
    print "# Filter complete. #"
    return paired_read_list

def FusionScreening(paired_read_list):
    print "# Fusion screening. #"
    g_strand = re.compile("TTAGGGTTAGGG")
    c_strand = re.compile("CCCTAACCCTAA")
    for pair in paired_read_list:
        read_1 = paired_read_list[pair][0]
        read_2 = paired_read_list[pair][1]
	if sys.argv[2] == "g":
	    match_1 = re.search(g_strand, read_1)
	else:
	    match_1 = re.search(c_strand, read_1)
        if match_1:
	    if sys.argv[2] == "g":
	        match_2 = re.search(g_strand, read_2)
	    else:
		    match_2 = re.search(c_strand, read_2)
            if match_2:
                    print pair
		    print read_1, read_2
    print "# Screening complete. #"

filename_normal, filename_tumor = FileNameList()
# data_list = ReadFile("C://seq//trial.fastq")
data_list = ReadFile("//N//dcwan//projects//ngs//users//liren//201301_TCGA//all_reads//" + sys.argv[1] + ".all.t2c2.fastq")
paired_read_list = PairFilter(data_list)
FusionScreening(paired_read_list)
