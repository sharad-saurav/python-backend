'''
Rule 19 - Start Time and End Time, below is the Time format
HH:MM:SS
'''
def time_in_hh_mm_ss_format(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile
	from dateutil.parser import parse
	import validators
	from datetime import date

	file_name="Time_in_HH-MM-SS_format.py"
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
			start_time=row['START_TIME']
			end_time=row['END_TIME']
			if(type(start_time)!=float and type(end_time)!=float):
				if (not re.match(r"(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)",start_time)):
					entry=[index,file,column_name+' does not have time in HH:MM:SS format']
					print('The row '+str(index)+' in the file '+file+' does not have start time in HH:MM:SS format')
					data.append(entry)
				if (not re.match(r"(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)",end_time)):
					entry=[index,file,column_name+' does not have time in HH:MM:SS format']
					print('The row '+str(index)+' in the file '+file+' does not have end time in HH:MM:SS format')
					data.append(entry)
					
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)