#Rule 7 - If the information in TEXT, VOICE, VOICE_ONLY column exceeds 500 characters, then in the VOICE column, certain verbiages need to be used.
def exceeding_500_characters(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Exceeding_500_characters"

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
			for column_name in columns_to_apply:
				column_value=row[column_name]
				if(pd.notnull(row[column_name])):
					if(len(column_value)>=500):
						#print(index)
						entry=[index,fleName,column_name+' has more than 500 characters']
						print('The row '+str(index)+' in the file '+fleName+' has content greater than 500 characters in the '+column_name+' column')
						data.append(entry)
					
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)