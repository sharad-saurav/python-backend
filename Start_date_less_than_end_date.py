#Rule 16 - Start Date and Time should always be less than End Data and Time.
def start_date_less_than_end_date(fle, fleName, target):
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
	from datetime import date
	from datetime import time
	import datetime

	configFile ='https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Start_date_less_than_end_date"

	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']

	data=[]
	if(files_to_apply=='ALL' or fleName in files_to_apply):
		def validate_date(date_text):
			try:
				datetime.datetime.strptime(date_text, '%Y-%m-%d')
				return True
			except:
				return False

		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index,row in df.iterrows():
			start_date=row['START_DATE']
			end_date=row['END_DATE']
			
			if(pd.notnull(row['START_DATE']) and pd.notnull(row['END_DATE'])): 
				if(validate_date(start_date) and validate_date(end_date)):		
					if(start_date > end_date):
						entry=[index,fleName,'START_DATE has start date greater than end date']
						print('The row '+str(index)+' in the file '+fleName+' has start date greater than end date')
						data.append(entry)
				
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
