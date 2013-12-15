#!~/bin/python
import re
import sys

def FileNameList():
    '''(NoneType) -> list
    Return a list of file name prefixes:
    BRCA0001 - BRCA0024
    '''
    filename_list = []
    for i in range(1, 25):    
        if i < 10:
            file_id = "BRCA000" + str(i)
        else:
            file_id = "BRCA00" + str(i)        
            filename_list.append(file_id)
    return filename_list

def ReadFile(filename):
    '''(filename:str) -> list

    Read the data from filename into data_list.
    '''
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

def FusionScreening(paired_read_list, p=False):
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
	result = ""
	y_count = 0
	if match_1_g and match_2_c or match_1_c and match_2_g:
            g_c += 1
            result = "G/C"
            y_count += 1            
        elif match_1_g and match_2_g:
            g_g += 1
            result = "G/G"
            y_count += 1
        elif match_1_c and match_2_c:
            c_c += 1
            result = "C/C"
            y_count += 1
        if p:
            print
            print result, read_1
            print result, read_2
    return g_c, g_g, c_c

if __name__ == '__main__':
    help_info = '''
    ***********************************************************************
    Generate statistics or dump paired reads for telomere-like reads.
    python fusion_vis.py sample_name [normal|tumor]

    Without tissue type (normal or tumor), strand statistics of both
    normal and tumor of the specified sample will be printed.
    e.g.
    python fusion_vis.py BRCA0001

    With tissue type (normal or tumor), paired reads will be printed
    together with the statistics.
    e.g.
    python fusion_vis.py BRCA0001 normal
    ***********************************************************************
    '''
    print help_info
    
    if len(sys.argv) == 3:
        filename = sys.argv[1]
        sample_type = sys.argv[2]
        result = []
        filepath = "//N//dcwan//projects//ngs//users//liren//201301_TCGA//filtered_reads//"
        sample_type = "." + sample_type
        data_list = ReadFile(filepath + filename + sample_type + ".filtered.fastq")
        paired_read_list = PairFilter(data_list)
        g_c, g_g, c_c = FusionScreening(paired_read_list, True)
        print
        print filename, sample_type[1:]
        print 'G / C reads:', g_c
        print 'G / G reads:', g_g
        print 'C / C reads:', c_c
        
    else:
        filename = sys.argv[1]
        result = []
        filepath = "//N//dcwan//projects//ngs//users//liren//201301_TCGA//filtered_reads//"
        # normal
        sample_type = ".normal"
        data_list = ReadFile(filepath + filename + sample_type + ".filtered.fastq")
        paired_read_list = PairFilter(data_list)
        n_g_c, n_g_g, n_c_c = FusionScreening(paired_read_list, False)
        # tumor
        sample_type = ".tumor"
        data_list = ReadFile(filepath + filename + sample_type + ".filtered.fastq")
        paired_read_list = PairFilter(data_list)
        t_g_c, t_g_g, t_c_c = FusionScreening(paired_read_list, False)
        
        print(filename)
        print('G / C reads: N - ' + str(n_g_c))
        print('             T - ' + str(t_g_c))
        print('G / G reads: N - ' + str(n_g_g))
        print('             T - ' + str(t_g_g))
        print('C / C reads: N - ' + str(n_c_c))
        print('             T - ' + str(t_c_c))
