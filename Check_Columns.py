def checkColumn(fle, fleName):
    import pandas as pd
    from pandas import ExcelWriter
    from pandas import ExcelFile
    import numpy as np
    import json

    checkColumnFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/checkColumn.xlsx'
    df=pd.read_excel(checkColumnFile)
    print('df.File--------',df.File)
    print('fleName--------',fleName)
    columnNames =  df.loc[df.File == fleName,'Columns'].tolist()
    print('columnNames1------',columnNames)
    columnNames =  "[" + columnNames[0] + "]"
    print('columnNames2------',columnNames)
    columnNames = json.loads(columnNames)
    print('columnNames3----------',columnNames)
    print('columnNames-----',columnNames)
    df = pd.read_excel(fle)
    print('df----',df)
    for col in columnNames:
        print('col---------',col)
        if col not in df.columns:
            raise KeyError("column " + col + " not present in " + fleName)
