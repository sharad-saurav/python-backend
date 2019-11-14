def date_format(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile
	import datetime

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Date_in_YYYY_MM_DD_format"

	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']
	print('true test-----------------------------------',files_to_apply=='ALL' ,  fleName + ".xlsx" in  files_to_apply, files_to_apply=='ALL' or fleName + ".xlsx" in  files_to_apply)
	if(files_to_apply=='ALL' or fleName in  files_to_apply):
		data=[]
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		for index,row in df.iterrows():
			start_date=row['START_DATE']
			end_date=row['END_DATE']
			if(pd.notnull(row['START_DATE'])):
				try:
					datetime.datetime.strptime(start_date, '%Y-%m-%d')
				except:
					entry=[index,fleName,'start_date is not in YYYY-MM-DD format']
					print('The row '+str(index)+' in the file '+fleName+' does not have start date in YYYY-MM-DD format')
					data.append(entry)
			if(pd.notnull(row['END_DATE'])):
				try:
					datetime.datetime.strptime(end_date, '%Y-%m-%d')
				except:
					entry=[index,fleName,'END_DATE is not in YYYY-MM-DD format']
					print('The row '+str(index)+' in the file '+fleName+' does not have end date in YYYY-MM-DD format')
					data.append(entry)
				
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)