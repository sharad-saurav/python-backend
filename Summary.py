def summary(target, numberOfFiles, rules):
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

	flag = True

	sheet_columns=['File_name','Total_Issues']



	for file in files:
		total_issues[file]=0
	newdf=pd.DataFrame(list(total_issues.items()),columns=sheet_columns)

	#wb=openpyxl.load_workbook(file)
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
		print('r---',r)
		print('target---',target)
		df = pd.read_excel(target, sheet_name=r)
		file_cnt=df.groupby(by='FILE_NAME',as_index=False).agg({'ROW_NO': pd.Series.nunique})
		for index,row in file_cnt.iterrows():
			file_name=row['FILE_NAME']
			file_name=file_name[:file_name.find('.xlsx')]
			i=newdf.index[newdf['File_name'] == file_name]
			newdf.loc[i,r]=row['ROW_NO']
			newdf.loc[i,'Total_Issues']+=row['ROW_NO']

	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		newdf.to_excel(writer,sheet_name='Summary',index=False)
