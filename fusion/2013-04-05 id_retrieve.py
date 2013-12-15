import urllib.request

def get_id(a_id):
    '''(str) -> tuple of str

    Retrieve participant_id and sample_id by a_id from
    https://tcga-data.nci.nih.gov/uuid/uuidws/metadata/xml/uuid/<id>

    >>>aliquot_id = '519e1ea1-6658-4978-9f3d-313d7cc1e0c1'
    >>>get_id(aliquot_id)
    ('786e8dbe-442e-4551-87b3-b4c333b04dd4', '8ef7ad6f-a6e4-405c-b20e-d547985bd9d6')

    '''
    
    info_url = 'https://tcga-data.nci.nih.gov/uuid/uuidws/metadata/xml/uuid/'
    t_url = urllib.request.urlopen(info_url + a_id)
    t_page = str(t_url.read())    

    p_start = t_page.find('<participant href=')
    p_end = t_page.find('>', p_start + 1)
    p_id = t_page[p_end-38:p_end-2]
    
    s_start = t_page.find('<sample href=')
    s_end = t_page.find('>', s_start + 1)
    s_id = t_page[s_end-38:s_end-2]
    
    return (p_id, s_id)

if __name__ == '__main__':
    a_list = '''519e1ea1-6658-4978-9f3d-313d7cc1e0c1
81689324-2986-49f6-bef6-f5a525ca36c2
1fe98b05-6803-4803-83cd-a59e794b956e
4808bc63-000a-4a49-a25b-4b817ca5ea54
fac9101c-a974-4415-9eac-d2d433d02b13
6d2744ba-4817-482b-ad46-2e4e0897ad88
e8ef8b75-7c0c-4a42-9a10-3789b6afa5d2
2ad8d416-08a4-4e6f-947e-d74269d02ab1
62dd11c2-2271-45e7-b753-d0f0d79fdf23
bd51f90a-ec67-4a7d-87bf-9d85acd65d51
97168a1f-abf8-414b-af10-b63f5daa7023
d71e12c1-d92c-4cb6-8244-d100b2ef1c43
79d7a589-60bd-4b4a-89c1-d557fe24c733
'''
    a_list = a_list.split()
    for a_id in a_list:
        print(get_id(a_id))
    
