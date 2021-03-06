def checkColumn(fle, fleName):
    import pandas as pd
    from pandas import ExcelWriter
    from pandas import ExcelFile
    import numpy as np
    import json

    checkColumnFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/checkColumn.xlsx'
    df=pd.read_excel(checkColumnFile)
    columnNames =  df.loc[df.File == fleName,'Columns'].tolist()
    columnNames =  "[" + columnNames[0] + "]"
    columnNames = json.loads(columnNames)
    df = pd.read_excel(fle)
    for col in columnNames:
        if col not in df.columns:
            raise KeyError("column " + col + " not present in " + fleName)
