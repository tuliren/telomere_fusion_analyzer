#!/usr/local/bin/python

import urllib

f_read = open('2013-05-16 gene_name.txt', 'r')
f_write = open('gene_name.txt', 'w')
f_read.readline()
i = 1
for line in f_read:    
    
    line = line.strip('\n\r')
    print(i, line)
    url = urllib.urlopen('http://www.ncbi.nlm.nih.gov/nuccore/' + line)
    content = str(url.read())
    start = content.find('<h1>')
    end = content.find('</h1>', start)
    name = content[start+4:end]
    f_write.write(line + ' | ' + name + '\n')
    i = i + 1
f_read.close()
f_write.close()
