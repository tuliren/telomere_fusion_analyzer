f = open("C://input//2013-02-07 BRCA_metadata.txt", 'r')
file_content = f.readlines()
f.close
# data_list includes the information for all samples
# 'analysis_id' is the key for each sample
data_list = {}
current_sample = None
for line in file_content:
    line_content = line.split()
    if line_content:
        if line_content[0] == 'analysis_id':
            current_sample = line_content[2]
            data_list[current_sample] = {}
        elif current_sample != None:
            if len(line_content) == 3:
                data_list[current_sample][line_content[0]] = line_content[2]

f = open("C://input//2013-02-14 BRCA name list.txt")
file_content = f.readlines()
f.close

# name_list correlates filename with sample information
# 'filename' is the key for each sample
name_list = {}
for line in file_content[1:]:
    t_id, t_type, t_filename = line.split()
    name_list[t_filename] = {'id': t_id, 'type': t_type}

# merge the info in name_list with data_list
# by adding two more keys into each sample: 'id' and 'type'
merge_list = {}
for e in data_list:
    t_filename = data_list[e]['filename']
    if t_filename in name_list:
        t_id = name_list[t_filename]['id']
        t_type = name_list[t_filename]['type']
        if len(t_id) == 1:
            t_id = 'BRCA000' + t_id
        else:
            t_id = 'BRCA00' + t_id
        t_key = t_id + ' ' + t_type
        merge_list[t_key] = data_list[e]
        merge_list[t_key]['analysis_id'] = e

# information can be retrived from:
# https://tcga-data.nci.nih.gov/uuid/uuidws/metadata/xml/uuid/xxxxxxxxx

# print the merge_list
f = open('2013-04-05 Sample list.txt', 'w')
header = 'sample,type,analysis_id,center_name,study,library_strategy,platform,' + \
         'legacy_sample_id,disease_abbr,analyte_code,sample_type,tss_id,participant_id,' + \
         'sample_id,aliquot_id'
f.write(header + '\n')
for e in merge_list:
    # print(merge_list[e])
    content = e[:e.find(' ')] + ',' + \
              e[e.find(' ')+1:] + ',' + \
              merge_list[e]["analysis_id"] + ',' + \
              merge_list[e]["center_name"] + ',' + \
              merge_list[e]["study"] + ',' + \
              merge_list[e]["library_strategy"] + ',' + \
              merge_list[e]["platform"] + ',' + \
              merge_list[e]["legacy_sample_id"] + ',' + \
              merge_list[e]["disease_abbr"] + ',' + \
              merge_list[e]["analyte_code"] + ',' + \
              merge_list[e]["sample_type"] + ',' + \
              merge_list[e]["tss_id"] + ',' + \
              merge_list[e]["participant_id"] + ',' + \
              merge_list[e]["sample_id"] + ',' + \
              merge_list[e]["aliquot_id"]
    f.write(content + '\n')
f.close()
    
print('Total number of samples:', len(merge_list))
