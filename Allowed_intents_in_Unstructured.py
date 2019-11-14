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

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule= 'Allowed_intents_in_Unstructured'
	config1=pd.read_excel(configFile)
	newdf=config1[config1['RULE']==rule]

	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']
	intents=to_check['intents_to_check']
	if(files_to_apply=='ALL' or fleName in files_to_apply):
		data=[]
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		for col in columns_to_apply:	
			for index, row in df.iterrows():
				column_value=row[col]
				if(pd.notnull(row[col])):
					if(column_value not in intents):
						entry=[index,fleName,column_value+' is not a allowed intent in the Unstructured file']
						data.append(entry)		
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)