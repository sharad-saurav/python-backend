#Rule 1 - Perfect excel format no extra spaces. - No leading and trailing spaces in the column names. No leading and trailing zeros. Please make sure you delete any unwanted spaces in TEXT .
def perfect_excel_format(fle, fleName, target):
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

	file_name="Perfect_Excel_format.py"
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
	columns_to_match=to_check['columns_to_match']

	if(to_check['files_to_apply']=='ALL'):
		files = all_files
	else:
		for f in files_to_apply:
			for file in all_files:
				if(file.startswith(f)):
					files.append(file)

	data=[]

	regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
	cols = {}

	for file in files:
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		#print("Column headings:")
		res = re.search(r"[a-zA-z]+",file)
		cols[res.group(0)+'_cols']=df.columns
		#print(cols[res.group(0)+'_cols'])
		
		columns=df.columns
		for col in columns:
			if(col.startswith(' ')):
				entry=[index,file,col+' has leading spaces']
				print('Column name '+col+' in the file '+file+' has leading spaces')
				data.append(entry)
			if(col.endswith(' ')):
				entry=[index,file,col+' has trailing spaces']
				print('Column name '+col+' in the file '+file+' has trailing spaces')
				data.append(entry)
			if(regex.search(col) != None):
				entry=[index,file,col+' has special characters']
				print('Column name '+col+' in the file '+file+' has special characters')
				data.append(entry)
			if(col.startswith('0')):
				entry=[index,file,col+' has leading zeros']
				print('Column name '+col+' in the file '+file+' has leading zeros')
				data.append(entry)
			if(col.endswith('0')):
				entry=[index,file,col+' has trailing zeros']
				print('Column name '+col+' in the file '+file+' has trailing zeros')
				data.append(entry)
				
	#Rule - Check if the columns satisfies the data structure of all the data files
	for key,value in cols.items():
		cols_value=columns_to_match[key]
		print('value',value)
		print('cols_value',cols_value)
		if(sorted(cols_value)!=sorted(value.to_list())):
			entry=[index,file,key+' does not match the structure of the data file']
			print('The columns of the '+key+' does not match the structure of the data file')
	'''	
	#Rule - Academic event must have the same data file format as timing.
	if(cols['Academic_cols']!=cols['Timings_cols']):
		print("The structure of Academic event does not have the same data file format as timing.")
		
	#Rule - Location must have the same data file format as Contact.
	if(cols['Location_cols']!=cols['Contact_cols']):
		print("The structure of Academic event does not have the same data file format as timing.")
		
	#Rule - Unstructured file contains below columns only - Subject_Area, Sample_Question, INTENT, ENTITY_NAME, SECONDARY_ENTITY_NAME, KEYWORD, TEXT, VOICE, VOICE_ONLY, REF_URL, MEDIA, LANGUAGES, COPIED_FROM, ROCESS_AGENT_ID, PROCESS_ID 
	cols=['SUBJECT_AREA','SAMPLE_QUESTION','INTENT','ENTITY_NAME','COPIED_FROM','SECONDARY_ENTITY_NAME','KEYWORD','TEXT','VOICE','VOICE_ONLY','REF_URL','MEDIA','LANGUAGES','PROCESS_AGENT_ID','PROCESS_ID']
	if(sorted(Unstructured_cols)!=sorted(cols)):
		print('The file '+file+' does not match the data structure defined')
	'''

	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)