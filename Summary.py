def summary(fle, fleName, target):
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
	# target= 'C:/Users/105666/projects/pythonProject/angular-python-flask-demo/DataFiles_Rules_Report.xlsx'
	config=pd.read_excel(config_file)
	dfObj=config[config['RULE']=='Summary']
	to_check=''
	for index,row in dfObj.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files=sorted(to_check['files'])
	total_issues={}

	sheet_columns=['File_name','Total_Issues']
	for file in files:
		total_issues[file]=0
	newdf=pd.DataFrame(list(total_issues.items()),columns=sheet_columns)
	print(newdf)

	#wb=openpyxl.load_workbook(file)
	wb=ExcelFile(target)
	sheet_names=wb.sheet_names
	print(sheet_names)

	for sheet in sheet_names:
		newdf[sheet]=0
		df = pd.read_excel(target, sheet_name=sheet)
		#print(df.head())
		file_cnt=df.groupby(by='FILE_NAME',as_index=False).agg({'ROW_NO': pd.Series.nunique})
		print(file_cnt)
		for index,row in file_cnt.iterrows():
			file_name=row['FILE_NAME']
			file_name=file_name[:file_name.find('.xlsx')]
			i=newdf.index[newdf['File_name'] == file_name]
			newdf.loc[i,sheet]=row['ROW_NO']
			newdf.loc[i,'Total_Issues']+=row['ROW_NO']
		print(newdf)
		
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		newdf.to_excel(writer,sheet_name='Summary',index=False)
