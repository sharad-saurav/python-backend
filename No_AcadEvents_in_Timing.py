#Rule 28 - Make sure interactions in AcadEvents are not present in Timing file.
def no_acadEvents_in_timing(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import pandas as pd
	import openpyxl
	from pandas import ExcelWriter
	from pandas import ExcelFile
	import validators
	
	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="No_AcadEvents_in_Timing"
	
	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']
	if(files_to_apply=='ALL' or fleName in files_to_apply):
		data=[]
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index, row in df.iterrows():
			column_value=row['ENTITY_TYPE']
			if(pd.notnull(row['ENTITY_TYPE'])):
				if(column_value=='AcadEvents'):
					entry=[index,fleName,'ENTITY_TYPE has entity of type AcadEvents which is not allowed entity type in timing file']
					print('The row '+str(index)+' in the file '+fleName+' is of type AcadEvents which is not allowed')
					data.append(entry)

		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)