#Rule 22 - Latitude and Longitude values must have a precision of 6 digits after the decimal point. They should not contain special characters, including spaces
def latitide_longitude(fle, fleName, target):
	import re
	import os
	import sys
	import json
	import openpyxl
	import pandas as pd
	from pandas import ExcelWriter
	from pandas import ExcelFile

	file_name="Latitude_Longitude.py"
	configFile =  'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule=file_name[:file_name.find('.py')]
	# file_directory= 'C:/uploads'
	
	config_file=configFile
	# target= 'C:/Users/105666/projects/pythonProject/angular-python-flask-demo/DataFiles_Rules_Report.xlsx'
	fles = []
	fles.append(fleName)
	all_files= fles
	files=[]

	regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')

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
			latitude=str(row['LATITUDE'])
			longitude=str(row['LONGITUDE'])

			if(len(latitude)==3):
				entry=[index,file,'This row does not have latitude value']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx does not have latitude value')
				data.append(entry)
			elif(len(longitude)==3):
				entry=[index,file,'This row does not have longitude value']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx does not have longitude value')
				data.append(entry)
			elif(len(latitude.split('.')[1])<6):
				entry=[index,file,'Latitude value '+latitude+' has less than 6 digits after decimal point']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has less or more than 6 digits after decimal point in latitude')
				data.append(entry)
			elif(len(longitude.split('.')[1])<6):
				entry=[index,file,'Longitude value '+longitude+' has less than 6 digits after decimal point']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has less or more than 6 digits after decimal point in longitude')
				data.append(entry)
			elif(len(latitude.split('.')[1])>6):
				entry=[index,file,'Latitude value '+latitude+' has more than 6 digits after decimal point']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has less or more than 6 digits after decimal point in latitude')
				data.append(entry)
			elif(len(longitude.split('.')[1])>6):
				entry=[index,file,'Longitude value '+longitude+' has more than 6 digits after decimal point']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has less or more than 6 digits after decimal point in longitude')
				data.append(entry)
			elif((regex.search(latitude)!=None)):
				entry=[index,file,'Latitude value '+latitude+' has special characters']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has special characters in latitude')
				data.append(entry)
			elif((regex.search(longitude)!= None)):
				entry=[index,file,'Longitude value '+longitude+' has special characters']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has special characters in longitude')
				data.append(entry)
				
	df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
	with ExcelWriter(target,engine='openpyxl',mode='a') as writer:
		df1.to_excel(writer,sheet_name=rule,index=False)
