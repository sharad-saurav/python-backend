def rule_unstructured(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import pandas as pd
	import openpyxl
	from pandas import ExcelWriter
	from pandas import ExcelFile
	import validators
	import requests

	configFile1 = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	file_name='Allowed_intents_in_Unstructured.py'
	rule=file_name[:file_name.find('.py')]
	
	config_file1=configFile1
	
	fles = []
	fles.append(fleName)
	all_files= fles
	files=[]

	config1=pd.read_excel(config_file1)

	newdf=config1[config1['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']

	columns_to_apply=to_check['columns_to_apply']
	intents=to_check['intents_to_check']
	if(to_check['files_to_apply']=='ALL'):
		files = all_files
	else:
		for f in files_to_apply:
			for file in all_files:
				if(file.startswith(f)):
					files.append(file)
	data=[]

	for file in files:
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
			
		for index, row in df.iterrows():
			column_value=row['INTENT']
			if(type(column_value)!=float):
				if(column_value not in intents):
					entry=[index,file,column_value+' is not a allowed intent in the Unstructured file']
					data.append(entry)
	
	
	print('target-----------',target)
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	print('target-----------',df1)
	with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
		print('target-----------',writer)
		df1.to_excel(writer,sheet_name=rule,index=False)