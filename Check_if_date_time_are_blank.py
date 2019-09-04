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

	file_name="Check_if_date_time_are_blank.py"
	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule=file_name[:file_name.find('.py')]
	# file_directory= 'C:/uploads'
	
	config_file=configFile
	# target= 'C:/Users/105666/projects/pythonProject/angular-python-flask-demo/DataFiles_Rules_Report.xlsx'
	
	fles = []
	fles.append(fleName)
	all_files= fles
	files=[]

	config=pd.read_excel(config_file)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
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

	data=[]

	for file in files:
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index,row in df.iterrows():
			start_date=row['START_DATE']
			end_date=row['END_DATE']
			start_time=row['START_TIME']
			end_time=row['END_TIME']
			
			if(type(start_date)==float):
				entry=[index,file,' This row does not have start date']
				print('The row '+str(index)+' in the file '+file+' does not have start_date')
				data.append(entry)
			if(type(end_date)==float):
				entry=[index,file,' This row does not have end date']
				print('The row '+str(index)+' in the file '+file+' does not have end date')
				data.append(entry)
			if(type(start_time)==float):
				entry=[index,file,' This row does not have start time']
				print('The row '+str(index)+' in the file '+file+' does not have start time')
				data.append(entry)
			if(type(end_time)==float):
				entry=[index,file,' This row does not have end time']
				print('The row '+str(index)+' in the file '+file+' does not have end time')
				data.append(entry)
				
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)