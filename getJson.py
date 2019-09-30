def get_Json_data(target):
    import xlrd
    import os
    from collections import OrderedDict
    import simplejson as json
    import requests
    import urllib

    wb = xlrd.open_workbook(target)
    try:
        sh = wb.sheet_by_index(31)
    except:
        sh = wb.sheet_by_index(30)
    data_list = []

    for colnum in range(1, sh.ncols):
        data = dict()
        col_values = sh.col_values(colnum)
        data['name'] = col_values[0]
        data['academicEvents'] = col_values[1]
        data['campusEvents'] = col_values[2]
        data['contact'] = col_values[3]
        data['location'] = col_values[4]
        data['timing'] = col_values[5]
        data['unstructured'] = col_values[6]
        data_list.append(data)
 
    j = json.dumps(data_list)
    os.remove(target)
    return j
