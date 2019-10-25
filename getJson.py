def get_Json_data(target, length):
    import xlrd
    import os
    from collections import OrderedDict
    import simplejson as json
    import requests
    import urllib
    import pandas as pd

    df = pd.read_excel(target, sheet_name="Summary")
    json_data = df.to_json(orient='records')
    os.remove(target)
    return json_data
