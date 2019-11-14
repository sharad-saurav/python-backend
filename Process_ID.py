#Rule 9 - PROCESS_AGENT_ID should be alphanumberic and PROCESS_ID should be a number
def process_id(fle, fleName, target):
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

	file_name="Process_ID.py"
	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Process_ID"

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

		def validate_process_id(string):
			if(re.match("^[a-zA-Z0-9-_]+$",string)):
				return False
			else:
				return True

		def validate_process_agent_id(string):
			if(re.match("^[-+]?[0-9]+$",string)):
				return False
			else:
				return True
	
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index,row in df.iterrows():
			process_id=row['PROCESS_ID']
			process_agent_id=row['PROCESS_AGENT_ID']
			
			if(pd.notnull(row['PROCESS_ID'])): 
				if(validate_process_id(process_id)):		
					entry=[index,fleName,'PROCESS_ID has space or any character other than aphanumeric']
					data.append(entry)
			
			if(pd.notnull(row['PROCESS_AGENT_ID'])): 
				if(validate_process_agent_id(str(process_agent_id))):		
					entry=[index,fleName,'PROCESS_AGENT_ID has any character other than numeric']
					data.append(entry)

		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
