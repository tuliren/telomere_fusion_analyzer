import sys
from operator import itemgetter

def ReadFile(filename):
    data_list = []
    f = open(filename)
    title_line = f.readline()
    for line in f:
        f_line = line.rstrip("\n").split()
        data_list.append([f_line[1], # 0, name
                          f_line[0], # 1, bin
                          f_line[12], # 2, name2
                          f_line[2], # 3, chrom
                          f_line[3], # 4, strand
                          int(f_line[4]), # 5, txStart
                          int(f_line[5])]) # 6, txEnd
    f.close
    return data_list

data_list = ReadFile("C://input//genelist_sample.table")
sorted_list = sorted(data_list, key = itemgetter(3, 5))
for line in sorted_list:
    result = ""
    for i in xrange(0, 7):
        result += str(line[i]) + "\t"
    print result[:-1]
