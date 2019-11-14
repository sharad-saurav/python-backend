#Rule 6 - VOICE and VOICE ONLY Column should not contain numbering or bullet points.
def numbering_bullet_points(fle, fleName, target):
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

	file_name="Numbering_bullet_points.py"
	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Numbering_bullet_points"

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
		bullet_point = re.compile(r"\u2022")

		def find_bullet_point(string):
			result = re.search(bullet_point, string)
			if(result != None):
				return True
			else:
				return False
			
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index, row in df.iterrows():
			for column_name in columns_to_apply:
				column_value=row[column_name]
				if(pd.notnull(row[column_name])):
					if(find_bullet_point(column_value)):
						entry=[index,fleName,column_name+' contains bullet points/Numbering in its contents']
						print('The row '+str(index)+' in the file '+fleName+' contains bullent points/Numbering in the'+column_name+' column')
						data.append(entry)
			
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)


		         
    	
			
        
			