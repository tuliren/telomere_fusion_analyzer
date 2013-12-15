
def summarize(filename):
    f = open(filename)
    file_content = f.readlines()
    total_reads = 0
    for each_line in file_content:
        mapped, unmapped = map(int, each_line.split()[2:])
        total_reads += mapped + unmapped
    return total_reads

for i in range(1, 25):
    if i <10:
        file_id = "000" + str(i)
    else:
        file_id = "00" + str(i)
    filename_normal = "F://BRCA" + file_id + ".normal.idxstats"
    filename_tumor =  "F://BRCA" + file_id + ".tumor.idxstats"
    print file_id, "N:", summarize(filename_normal)
    print file_id, "T:", summarize(filename_tumor)
