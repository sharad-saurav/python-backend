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

	configFile =  'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
	rule="Latitude_Longitude"

	regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')

	config=pd.read_excel(configFile)
	newdf=config[config['RULE']==rule]
	to_check=''
	for index,row in newdf.iterrows():
		to_check=row['TO_CHECK']
	to_check=json.loads(to_check)
	files_to_apply=to_check['files_to_apply']
	columns_to_apply=to_check['columns_to_apply']
	
	if(files_to_apply=='ALL' or fleName in files_to_apply):
		data=[]
	
		df = pd.read_excel(fle)
		df.index = range(2,df.shape[0]+2)

		for index,row in df.iterrows():
			latitude=str(row['LATITUDE'])
			longitude=str(row['LONGITUDE'])

			if(len(latitude)==3):
				entry=[index,fleName,'This row does not have latitude value']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx does not have latitude value')
				data.append(entry)
			elif(len(longitude)==3):
				entry=[index,fleName,'This row does not have longitude value']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx does not have longitude value')
				data.append(entry)
			elif(len(latitude.split('.')[1])<6):
				entry=[index,fleName,'Latitude value '+latitude+' has less than 6 digits after decimal point']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has less or more than 6 digits after decimal point in latitude')
				data.append(entry)
			elif(len(longitude.split('.')[1])<6):
				entry=[index,fleName,'Longitude value '+longitude+' has less than 6 digits after decimal point']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has less or more than 6 digits after decimal point in longitude')
				data.append(entry)
			elif(len(latitude.split('.')[1])>6):
				entry=[index,fleName,'Latitude value '+latitude+' has more than 6 digits after decimal point']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has less or more than 6 digits after decimal point in latitude')
				data.append(entry)
			elif(len(longitude.split('.')[1])>6):
				entry=[index,fleName,'Longitude value '+longitude+' has more than 6 digits after decimal point']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has less or more than 6 digits after decimal point in longitude')
				data.append(entry)
			elif((regex.search(latitude)!=None)):
				entry=[index,fleName,'Latitude value '+latitude+' has special characters']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has special characters in latitude')
				data.append(entry)
			elif((regex.search(longitude)!= None)):
				entry=[index,fleName,'Longitude value '+longitude+' has special characters']
				print('The row '+str(index)+' in the file Location_v1.40.xlsx has special characters in longitude')
				data.append(entry)
				
		df1 = pd.DataFrame(data, columns = ['ROW_NO', 'FILE_NAME', 'COMMENTS'])
		if(ExcelFile(target).sheet_names[0] == 'Sheet1'):
			with ExcelWriter(target, engine='openpyxl', mode='w') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
		else:
			with ExcelWriter(target, engine='openpyxl', mode='a') as writer:
				df1.to_excel(writer,sheet_name=rule,index=False)
