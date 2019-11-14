def no_sentence_in_voice_column(fle, fleName, target):
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

	file_name="No_sentence_in_voice_column.py"
	configFile =  'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="No_sentence_in_voice_column"

	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	strings_to_apply=to_check['strings_to_apply']

	if(files_to_apply=='ALL' or fleName in files_to_apply):
		data=[]
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index, row in df.iterrows():
			column_value=row['VOICE_ONLY']
			if(pd.notnull(row['VOICE_ONLY'])):
				for string in strings_to_apply:
					if(string in column_value):
						#print(index)
						entry=[index,fleName,'VOICE_ONLY column has '+string+' in its contents']
						print('The row '+str(index)+' in the file '+fleName+' has the text\' '+string+' \'in the voice_only column')
						data.append(entry)

		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)