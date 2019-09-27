def No_date_special_characters(fle, fleName, target):
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

	file_name="No_date_special_characters.py"
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
	regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')

	def search_url(string): 
		url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
		if(len(url)!= 0):
			return True
		else:
			return False

	def has_date(string,fuzzy=False):
		try: 
			parse(string, fuzzy=fuzzy)
			return True
		except ValueError:
			return False
		
	data=[]

	for file in files:
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index, row in df.iterrows():
			for column_name in columns_to_apply:
				column_value=row[column_name]
				if(pd.notnull(row[column_name])):
					if(has_date(column_value)):
						entry=[index,file,column_name+' has date']
						print('The row '+str(index)+' in the file '+file+' has date in the '+column_name+' column')
						data.append(entry)
					if(regex.search(column_value)!=None):
						entry=[index,file,column_name+' has special characters']
						print('The row '+str(index)+' in the file '+file+' has special characters in the '+column_name+' column')
						data.append(entry)
					if(search_url(column_value)):
						#print(index)
						entry=[index,file,column_name+' has url in its contents']
						print('The row '+str(index)+' in the file '+file+' has url in the '+column_name+' column')
						data.append(entry)
					
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)