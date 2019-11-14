#Rule 13 - Check for Duplicates - Primary Entity or Virtual Entity values cannot have duplicate.
def duplicate_entity_interaction(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Duplicate_in_Entity_Interactn"
	
	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']
	print('true test-----------------------------------',files_to_apply=='ALL' ,  fleName + ".xlsx" in  files_to_apply, files_to_apply=='ALL' or fleName + ".xlsx" in  files_to_apply)
	if(files_to_apply=='ALL' or fleName in files_to_apply):
		data=[]
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		duplicatedRowsDF = df[df.duplicated(columns_to_apply)]
		if(not duplicatedRowsDF.empty):
			for index,row in duplicatedRowsDF.iterrows():
				entry=[index,fleName,' This row has a duplicated combination of primary entity or virtual entity']
				data.append(entry)
			print('The duplicate combination of primary entity or virtual entity in the file '+fleName+' are:')
			print(duplicatedRowsDF)
				
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)