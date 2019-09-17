def get_Json_data(target):
    import xlrd
    from collections import OrderedDict
    import simplejson as json
    import requests
    import urllib

    wb = xlrd.open_workbook(target)
    try:
        sh = wb.sheet_by_index(31)
    except:
        print('------------------30------------------------')
        sh = wb.sheet_by_index(30)
    # print('sh-------------',sh)
    print('sh.ncols-------------',sh.ncols)
    # List to hold dictionaries
    data_list = []
    # Iterate through each row in worksheet and fetch values into dict

    for colnum in range(1, sh.ncols):
        # print('colnum---------', colnum)
        # print(' sh.col_values(colnum)--------', sh.col_values(colnum))
        data = OrderedDict()
        col_values = sh.col_values(colnum)
        # print(col_values)
        
        data['name'] = col_values[0]
        data['academicEvents'] = col_values[1]
        data['campusEvents'] = col_values[2]
        data['contact'] = col_values[3]
        data['location'] = col_values[4]
        data['timing'] = col_values[5]
        data['unstructured'] = col_values[6]
        data_list.append(data)
 
    j = json.dumps(data_list)
    return j
