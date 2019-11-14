#Rule 21 - Date and Time fields should not be blank
def rule_date_time_blank(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile


	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Check_if_date_time_are_blank"
	
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
			if(pd.isnull(row['START_DATE'])):
				entry=[index,fleName,' This row does not have start date']
				print('The row '+str(index)+' in the file '+fleName+' does not have start_date')
				data.append(entry)
			if(pd.isnull(row['END_DATE'])):
				entry=[index,fleName,' This row does not have end date']
				print('The row '+str(index)+' in the file '+fleName+' does not have end date')
				data.append(entry)
			if(pd.isnull(row['START_TIME'])):
				entry=[index,fleName,' This row does not have start time']
				print('The row '+str(index)+' in the file '+fleName+' does not have start time')
				data.append(entry)
			if(pd.isnull(row['END_TIME'])):
				entry=[index,fleName,' This row does not have end time']
				print('The row '+str(index)+' in the file '+fleName+' does not have end time')
				data.append(entry)
				
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)