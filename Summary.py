def summary(target, numberOfFiles, rules, fileNames):
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile
	from dateutil.parser import parse
	import validators
	from datetime import date

	config_file= 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'

	
	total_issues={}

	flag = True

	sheet_columns=['File_name','Total_Issues']
	print('fileNames-----',fileNames)

	for file in fileNames:
		total_issues[file]=0
	newdf=pd.DataFrame(list(total_issues.items()),columns=sheet_columns)

	wb=ExcelFile(target)
	sheet_names=wb.sheet_names

	for r in rules:
		array = []
		if(r in sheet_names):
			for i in range(numberOfFiles):
				if(i != 0):
					array.append(wb.parse(r + str(i)))
				else:
					array.append(wb.parse(r))
			concat = pd.concat(array)
			if(flag):
				with ExcelWriter(target,engine='openpyxl',mode='w') as writer:
					concat.to_excel(writer,sheet_name=r,index=False)
					flag = False
			else:
				with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
					concat.to_excel(writer,sheet_name=r,index=False)

	for r in rules:
		newdf[r]=0
		df = pd.read_excel(target, sheet_name=r)
		file_cnt=df.groupby(by='FILE_NAME',as_index=False).agg({'ROW_NO': pd.Series.nunique})
		for index,row in file_cnt.iterrows():
			print('row----------',row)
			file_name=row['FILE_NAME']
			i=newdf.index[newdf['File_name'] == file_name]
			newdf.loc[i,r]=row['ROW_NO']
			newdf.loc[i,'Total_Issues']+=row['ROW_NO']

	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		newdf.to_excel(writer,sheet_name='Summary',index=False)

	
    
	