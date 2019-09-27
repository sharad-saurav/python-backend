#Rule 26 - In contact data file, the VOICE column must not contain any phone number or email ID
def no_phone_url_in_voice(fle, fleName, target):
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

	file_name="No_phone_url_in_voice.py"
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

	def search_email(string): 
		email = re.findall(r'[\w\.-]+@[\w\.-]+', string) 
		if(len(email)!= 0):
			return True
		else:
			return False
		
	def find_phone(string):
		phone = re.findall('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}', string)
		if(len(phone)!= 0):
			return True
		else:
			return False

	data=[]

	for file in files:
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index,row in df.iterrows():
			for column_name in columns_to_apply:
				column_value=row[column_name]
				#print(voice)
				if(pd.notnull(row[column_name])):
					if(search_email(column_value)):
						entry=[index,file,column_name+' has EMAIL in its contents']
						print('The row '+str(index)+' in the file '+file+' has url in the '+column_name+' column')
						data.append(entry)
					if(find_phone(column_value)):
						#print(index)
						entry=[index,file,column_name+' has phone number in its contents']
						print('The row '+str(index)+' in the file '+file+' has phone number in the '+column_name+' column')
						data.append(entry)

	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)