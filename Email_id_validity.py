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

	regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
	configFile = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Email_id_validity"


	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']

	def validate_email(email):   
		if(re.search(regex,email)): 
			return True
		else:  
			return False

	if(files_to_apply=='ALL' or fleName in files_to_apply):
		data=[]
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)
		for index,row in df.iterrows():
			for column_name in columns_to_apply:
				email=row['EMAIL']
				if(pd.notnull(row['EMAIL'])):
					if(not validate_email(email)):
						entry=[index,fleName,column_name+'column ' + email + ' is not a valid email id']
						print('The row '+str(index)+' in the file '+ fleName +' does not have a proper email id')
						data.append(entry)

		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)