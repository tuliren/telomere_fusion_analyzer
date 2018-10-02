#!/usr/local/bin/python
import re
import sys
import os

# Parameter 1: target, either "all" or in the form of "BRCA00XX"
# Parameter 2: option, either "stat" or "fastq"
# E.g. python filter.py BRCA0001 stat
#      python filter.py BRCA0001 fastq
#      python filter.py all stat
#      python filter.py all fastq

def FileNameList():
    filename_list = []
    for i in range(1, 25):    
        if i <10:
            file_id = "BRCA000" + str(i)
        else:
            file_id = "BRCA00" + str(i)        
        filename_list.append(file_id)
    return filename_list

target = sys.argv[1]
option = sys.argv[2]
cmd = "python filter_aux.py "
if target != "all":
    cmd_1 = cmd + target + " normal " + option
    cmd_2 = cmd + target + " tumor " + option
    os.system(cmd_1)
    os.system(cmd_2)
else:
    filename_list = FileNameList()
    filepath = "//N//dcwan//projects//ngs//users//liren//201301_TCGA//filtered_reads//"
    for filename in filename_list:
        cmd_1 = cmd + filename + " normal " + option
        cmd_2 = cmd + filename + " tumor " + option
        if option == "fastq":
            cmd_1 += " > " + filepath + filename + ".normal.filtered.fastq"
            cmd_2 += " > " + filepath + filename + ".tumor.filtered.fastq"
        os.system(cmd_1)
        os.system(cmd_2)
    
