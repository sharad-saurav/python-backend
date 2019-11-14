#Rule 29 - There should not be any timing related information in TEXT, VOICE and VOICE_ONLY column of timing data file. Extra information about the service can be added in the DESCRIPTION column 
def no_timings_values_in_txt(fle, fleName, target):
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

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="No_timings_values_in_txt"

	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']


	data=[]
	if(files_to_apply=='ALL' or fleName in files_to_apply):
		def find_time(string):
			time = re.findall('([0-1]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)', string) 
			if(len(time)!= 0):
				return True
			else:
				return False

		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index, row in df.iterrows():
			for column_name in columns_to_apply:
				txt=row[column_name]
				if(pd.notnull(row[column_name])):
					if(find_time(txt)):
						entry=[index,fleName,column_name + ' has timings information in its contents']
						print('The row '+str(index)+' in the file '+fleName+' has timings in the '+column_name+' column')
						data.append(entry)

		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)