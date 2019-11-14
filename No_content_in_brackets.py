#Rule - No content in brackets should be there in VOICE_ONLY column. 
'''
Example:  
To complete the Master Promissory Note (M.P.N) and entrance counseling, students must go to the Federal Student Aid website. ----- Incorrect 
To complete the Master Promissory Note and entrance counseling, students must go to the Federal Student Aid website. ------------- Correct.
'''
def no_content_in_brackets(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="No_content_in_brackets"

	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']

	regex = r'\[(.+)\]|\((.+)\)|\{(.+)\}'

	def check_content_in_bracket(string):   
		if(re.search(regex,string)): 
			return True
		else:  
			return False

	if(files_to_apply=='ALL' or fleName in files_to_apply):
		data=[]	
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		
		for index, row in df.iterrows():
			for column_name in columns_to_apply:
				column_value=row[column_name]
				if(pd.notnull(row[column_name])):
					if(check_content_in_bracket(column_value)):
						#print(index)
						entry=[index,fleName,column_name+' has contents inside the brackets']
						print('The row ' + str(index) + ' in the file ' + fleName + ' has content inside brackets in the '+ column_name +' column')
						data.append(entry)
					
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)