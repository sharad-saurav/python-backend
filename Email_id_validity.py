#Rule 27 - Email ID should be complete, it should not contain any space.
def email_id_validity(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	file_name="Email_id_validity.py"
	regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
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

# def validate_email(string):
# 	pattern = '/\S+@\S+\.\S+/'1
# 	result = re.match(pattern, string)
# 	print('result------------',result)
# 	return result

	
      
# Define a function for 
# for validating an Email 
	def validate_email(email):   
		if(re.search(regex,email)): 
			return True
		else:  
			return False
		
	for file in files:
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		for index,row in df.iterrows():
			for column_name in columns_to_apply:
				email=row['EMAIL']
				if(pd.notnull(row['EMAIL'])):
					if(not validate_email(email)):
						entry=[index,file,column_name+'column ' + email + ' is not a valid email id']
						print('The row '+str(index)+' in the file '+file+' does not have a proper email id')
						data.append(entry)

	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)