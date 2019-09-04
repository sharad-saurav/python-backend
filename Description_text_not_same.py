#Rule 24 - Description and text cannot be same.
def description_text(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	file_name="Description_text_not_same.py"
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
			text=row['TEXT']			
			description=row['DESCRIPTION']
			if(description==text):
				entry=[index,file,'Both description and text have same contents']
				print('The row '+str(index)+' in the file '+file+' have same contents in both description and text')
				data.append(entry)
				
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)