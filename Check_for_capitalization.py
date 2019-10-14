def rule_capitalization(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	file_name="Check_for_capitalization.py"
	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule=file_name[:file_name.find('.py')]
	print('rule---',rule)
	config_file=configFile
# 	target= 'C:/Users/105666/projects/pythonProject/angular-python-flask-demo/DataFiles_Rules_Report.xlsx'
	fles = []
	fles.append(fleName)
	all_files= fles
	files=[]

	config=pd.read_excel(config_file)
	print('config---',config)
	newdf=config[config['RULE']==rule]
	print('newdf---',newdf)
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	
	print('to_check----',to_check)
	print(type(to_check))
	to_check=json.loads(to_check)
	
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']

	if(to_check['files_to_apply']=='ALL'):
		files = all_files
	else:
		for f in files_to_apply:
			for file in all_files:
				if(file.startswith(f)):
					files.append(file)

	regex = re.compile('[,-/()]')

	data=[]

	for file in files:
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index,row in df.iterrows():
			for column_name in columns_to_apply:
				print('column_name-----',column_name)
				column_value=row[column_name]
				if(pd.notnull(row[column_name])):
					if not column_value[0].isupper():
						entry=[index,file,'\''+column_value+'\' in '+column_name+' does not start with capital letter']
						data.append(entry)
						break
							
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)
