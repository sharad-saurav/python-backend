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
	import time

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Time_in_HH_MM_SS_format"

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

		def validate_time(time_text):
			if(re.match("(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)",time_text)):
				return False
			else:
				return True

		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		
		for index,row in df.iterrows():
			start_time=row['START_TIME']
			end_time=row['END_TIME']
			if(pd.notnull(row['START_TIME']) and pd.notnull(row['END_TIME'])):
				if (validate_time(start_time)):
					entry=[index,fleName,'column START_TIME ' + start_time + ' does not have time in HH:MM:SS format']
					print('The row '+str(index)+' in the file '+fleName+' does not have start time in HH:MM:SS format')
					data.append(entry)
				if (validate_time(end_time)):
					entry=[index,fleName,'column END_TIME '+ end_time+' does not have time in HH:MM:SS format']
					print('The row '+str(index)+' in the file '+fleName+' does not have end time in HH:MM:SS format')
					data.append(entry)
					
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)