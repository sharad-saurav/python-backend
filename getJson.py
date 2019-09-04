def get_Json_data(target):
    import xlrd
    from collections import OrderedDict
    import simplejson as json
    import requests
    import urllib

    wb = xlrd.open_workbook(target)
    sh = wb.sheet_by_index(6)
    # List to hold dictionaries
    data_list = []
    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):
        data = OrderedDict()
        row_values = sh.row_values(rownum)
        data['File_Name'] = row_values[0]
        data['Total_Issues'] = row_values[1]
        data['Perfect_Excel_Format'] = row_values[2]
        data['Process_ID'] = row_values[3]
        data['Special_CHar_In_Entity_Name'] = row_values[4]
        data['Start_Date_Less_Than_End_Date'] = row_values[5]
        data['Start_Date_Less_Than_End_Time'] = row_values[6]
        data['Time_in_hh'] = row_values[7]
        
        data_list.append(data)
 
    j = json.dumps(data_list)
    return j
