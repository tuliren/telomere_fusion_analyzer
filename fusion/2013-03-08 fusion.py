#!/usr/local/bin/python
import re
import sys

# Parameter 1: target, either "all" or "BRCA00XX"
# E.g. pyton fusion.py all
#      pyton fusion.py BRCA0001

def FileNameList():
    filename_list = []
    for i in range(1, 25):    
        if i < 10:
            file_id = "BRCA000" + str(i)
        else:
            file_id = "BRCA00" + str(i)        
        filename_list.append(file_id)
    return filename_list

def ReadFile(filename):
    data_list = {}
    f = open(filename)
    file_content = map(lambda x: x.rstrip("\n"), f.readlines())
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
    return data_list

def PairFilter(data_list):
    paired_read_list = {}
    for pair in data_list:
        if data_list[pair][0] == 2:
            paired_read_list[pair] = data_list[pair][1]
    return paired_read_list

def FusionScreening(paired_read_list):
    g_strand = re.compile("TTAGGG")
    c_strand = re.compile("CCCTAA")
    g_c, g_g, c_c = 0, 0, 0
    for pair in paired_read_list:
        read_1 = paired_read_list[pair][0]
        read_2 = paired_read_list[pair][1]
	match_1_g = re.search(g_strand, read_1)
	match_1_c = re.search(c_strand, read_1)
	match_2_g = re.search(g_strand, read_2)
	match_2_c = re.search(c_strand, read_2)
	# y /n for g_c, g_g, c_c
	result = ["n", "n", "n"]
	y_count = 0
	if match_1_g and match_2_c or match_1_c and match_2_g:
            g_c += 1
            result[0] = "y"
            y_count += 1
        elif match_1_g and match_2_g:
            g_g += 1
            result[1] = "y"
            y_count += 1
        elif match_1_c and match_2_c:
            c_c += 1
            result[2] = "y"
            y_count += 1
        if y_count == 0 or y_count > 1:
            print result, read_1, read_2
    return g_c, g_g, c_c

argv = sys.argv[1]
result = []
filepath = "//N//dcwan//projects//ngs//users//liren//201301_TCGA//filtered_reads//"
if argv == "all":
    filename_list = FileNameList()
else:
    filename_list = [argv]

for filename in filename_list:
    for sample_type in [".normal", ".tumor"]:
        data_list = ReadFile(filepath + filename + sample_type + ".filtered.fastq")
        paired_read_list = PairFilter(data_list)
        print filename, sample_type[1:], FusionScreening(paired_read_list)
