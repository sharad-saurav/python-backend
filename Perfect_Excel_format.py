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
	rule="Perfect_Excel_format"

	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_match=to_check['columns_to_match']

	if(files_to_apply=='ALL' or fleName in files_to_apply):
		data=[]
		regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
		cols = {}

		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		
		columns=df.columns
		for col in columns:
			if(col.startswith(' ')):
				entry=[index,fleName,col+' has leading spaces']
				print('Column name '+col+' in the file '+fleName+' has leading spaces')
				data.append(entry)
			if(col.endswith(' ')):
				entry=[index,fleName,col+' has trailing spaces']
				print('Column name '+col+' in the file '+fleName+' has trailing spaces')
				data.append(entry)
			if(regex.search(col) != None):
				entry=[index,fleName,col+' has special characters']
				print('Column name '+col+' in the file '+fleName+' has special characters')
				data.append(entry)
			if(col.startswith('0')):
				entry=[index,fleName,col+' has leading zeros']
				print('Column name '+col+' in the file '+fleName+' has leading zeros')
				data.append(entry)
			if(col.endswith('0')):
				entry=[index,fleName,col+' has trailing zeros']
				print('Column name '+col+' in the file '+fleName+' has trailing zeros')
				data.append(entry)
				
	#Rule - Check if the columns satisfies the data structure of all the data files
		for key,value in cols.items():
			cols_value=columns_to_match[key]
			if(sorted(cols_value)!=sorted(value.to_list())):
				entry=[index,fleName,key+' does not match the structure of the data file']
				print('The columns of the '+key+' does not match the structure of the data file')
		
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)