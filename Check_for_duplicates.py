def rule_duplicates(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Check_for_duplicates"
	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	print('true test-----------------------------------',files_to_apply=='ALL' ,  fleName + ".xlsx" in  files_to_apply, files_to_apply=='ALL' or fleName + ".xlsx" in  files_to_apply)
	if(files_to_apply=='ALL' or fleName in  files_to_apply):
		data=[]

		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		duplicatedRowsDF = df[df.duplicated()]
		if(not duplicatedRowsDF.empty):
			for index,row in duplicatedRowsDF.iterrows():
				print('index')
				entry=[index,fleName,'This is a duplicated row']
				data.append(entry)
			print('The duplicate rows in the file '+ fleName +' are:')
			print(duplicatedRowsDF)
				
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)