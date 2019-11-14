#Rule 23 - Check for Reference link for each entity and Ref URLs should not be there in Text.
def no_ref_url_in_text(fle, fleName, target):
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

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="No_Ref_URL_in_text"

	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']


	if(files_to_apply=='ALL' or fleName in files_to_apply):
		def find_url(string):
			url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
			if(len(url)!= 0):
				return True
			else:
				return False

		data=[]

		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		for column_name in columns_to_apply:
			for index,row in df.iterrows():
				text=row[column_name]
				#print(text)
				if(pd.notnull(row[column_name])):
					#print('t:'+text)
					if(find_url(text)):
						#print(index)
						entry=[index,fleName,' has Reference URL in its contents']
						print('The row '+str(index)+' in the file '+fleName+' has url in the text column')
						data.append(entry)
					
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)