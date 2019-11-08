
from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import json
from collections import OrderedDict
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from flask import jsonify
import getJson
import Allowed_intents_in_Unstructured
import Check_for_capitalization
import Check_for_duplicates
import Check_for_missing_Keyword
import Check_for_capitalization
import Correctness_of_MAP_URL
import Correctness_of_Short_Ref_URL
import Date_in_YYYY_MM_DD_format
import Description_text_not_same
import Duplicate_in_Entity_Interactn
import Email_id_validity
import Exact_dates_available
import Exceeding_500_characters
import Latitude_Longitude
import Multiple_Spaces_in_txt
import No_content_in_brackets
import No_AcadEvents_in_Timing
import No_date_special_characters
import No_phone_url_in_voice
import No_preceeding_0_in_room_no
import No_Ref_URL_in_text
import No_sentence_in_virtual_entity
import No_sentence_in_voice_column
import No_timing_for_acad_events
import No_timings_values_in_txt
import Numbering_bullet_points
import Perfect_Excel_format
import Process_ID
import Special_Char_in_Entity_Name
import Start_date_less_than_end_date
import Start_time_less_than_end_time
import Check_if_date_time_are_blank
import Summary
import Time_in_HH_MM_SS_format
import uploadFile
import requests
import urllib.request
import traceback
import Check_Columns
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl

app = Flask(__name__, static_url_path='')
CORS(app)
ALLOWED_EXTENSIONS = set([ 'xls', 'xlsx'])


port = int(os.getenv('PORT', 5002))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/parse_table', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        uploaded_files = request.files.getlist("file")
        milliseconds = request.args.get("milliseconds")
        rules = request.args.get("rules")
        rules = rules.split(',')
        link = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/DataFiles_Rules_Report.xlsx'
        target, headers = urllib.request.urlretrieve(link)
        print(target, headers)

        newTar = target + ".xlsx"
        os.rename(target, newTar)
        length = len(rules)
        numberOfFiles = len(uploaded_files)
        fileNames = []        
        for file in uploaded_files:
            fileNames.append(file.filename)

        for file in uploaded_files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                Check_Columns.checkColumn(file, filename) 
                if("Allowed_intents_in_Unstructured" in rules):
                    Allowed_intents_in_Unstructured.rule_unstructured(file, filename, newTar)
                if("Check_for_duplicates" in rules):
                    Check_for_duplicates.rule_duplicates(file, filename, newTar)  
                if("Check_for_missing_Keyword" in rules):
                    Check_for_missing_Keyword.rule_missing_keyword(file, filename, newTar) 
                if("Check_for_capitalization" in rules):
                    Check_for_capitalization.rule_capitalization(file, filename, newTar) 
                if("Check_if_date_time_are_blank" in rules):
                    Check_if_date_time_are_blank.rule_date_time_blank(file, filename, newTar) 
                if("Correctness_of_MAP_URL" in rules):
                    Correctness_of_MAP_URL.rule_map_url(file, filename, newTar)
                if("Correctness_of_Short_Ref_URL" in rules):
                    Correctness_of_Short_Ref_URL.short_ref_url(file, filename, newTar)
                if("Date_in_YYYY_MM_DD_format" in rules):
                    Date_in_YYYY_MM_DD_format.date_format(file, filename, newTar)
                if("Description_text_not_same" in rules):
                    Description_text_not_same.description_text(file, filename, newTar)
                if("Duplicate_in_Entity_Interactn" in rules):
                    Duplicate_in_Entity_Interactn.duplicate_entity_interaction(file, filename, newTar)
                if("Email_id_validity" in rules):
                    Email_id_validity.email_id_validity(file, filename, newTar)
                if("Exact_dates_available" in rules):
                    Exact_dates_available.exact_dates_available(file, filename, newTar)
                if("Exceeding_500_characters" in rules):
                    Exceeding_500_characters.exceeding_500_characters(file, filename, newTar)
                if("Latitude_Longitude" in rules):
                    Latitude_Longitude.latitide_longitude(file, filename, newTar)
                if("Multiple_Spaces_in_txt" in rules):
                    Multiple_Spaces_in_txt.multiple_spaces_in_txt(file, filename, newTar)
                if("No_content_in_brackets" in rules):
                    No_content_in_brackets.no_content_in_brackets(file, filename, newTar)
                if("No_AcadEvents_in_Timing" in rules):
                    No_AcadEvents_in_Timing.no_acadEvents_in_timing(file, filename, newTar)
                if("No_date_special_characters" in rules):
                    No_date_special_characters.No_date_special_characters(file, filename, newTar)
                if("No_phone_url_in_voice" in rules):
                    No_phone_url_in_voice.no_phone_url_in_voice(file, filename, newTar)
                if("No_preceeding_0_in_room_no" in rules):
                    No_preceeding_0_in_room_no.no_preceeding_0_in_room_no(file, filename, newTar)
                if("No_Ref_URL_in_text" in rules):
                    No_Ref_URL_in_text.no_ref_url_in_text(file, filename, newTar)
                if("No_sentence_in_voice_column" in rules):
                # No_sentence_in_virtual_entity.no_sentence_in_virtual_entity(file, filename, newTar)
                    No_sentence_in_voice_column.no_sentence_in_voice_column(file, filename, newTar)
                if("No_timing_for_acad_events" in rules):
                    No_timing_for_acad_events.no_timing_for_acad_events(file, filename, newTar)
                if("No_timings_values_in_txt" in rules):
                    No_timings_values_in_txt.no_timings_values_in_txt(file, filename, newTar)
                if("Numbering_bullet_points" in rules):
                    Numbering_bullet_points.numbering_bullet_points(file, filename, newTar)
                if("Process_ID" in rules):
                # Perfect_Excel_format.perfect_excel_format(file, filename, newTar)
                    Process_ID.process_id(file, filename, newTar)
                if("Special_Char_in_Entity_Name" in rules):
                    Special_Char_in_Entity_Name.special_char_in_entity_name(file, filename, newTar)
                if("Start_date_less_than_end_date" in rules):
                    Start_date_less_than_end_date.start_date_less_than_end_date(file, filename, newTar)
                if("Start_time_less_than_end_time" in rules):
                    Start_time_less_than_end_time.start_time_less_than_end_time(file, filename, newTar)
                if("Time_in_HH_MM_SS_format" in rules):
                    Time_in_HH_MM_SS_format.time_in_hh_mm_ss_format(file, filename, newTar)
        Summary.summary(newTar, numberOfFiles, rules, fileNames)
        uploadFile.multi_part_upload("sharad-saurav-bucket", "DataFiles_Rules_Report" + milliseconds + ".xlsx", newTar)
        return getJson.get_Json_data(newTar, length)
    except Exception as e:
        traceback.print_exc()
        return str(e)

@app.route('/changeConfig', methods=['POST'])
def changeConfig():
    try:
        print(request.data)
        configArray = json.loads(request.data.decode("utf-8"))
        configArray = configArray['configArray']
        config_file = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
        target, headers = urllib.request.urlretrieve(config_file)
        df=pd.read_excel(config_file)
        for data in configArray:
            for index,row in df.iterrows():
                if(row['RULE'] == data['rule']):
                    if(data['filesToApply'] == "ALL"):
                        data["columnsToApply"] = json.dumps(data["columnsToApply"])
                        data["filesToApply"] = json.dumps(data["filesToApply"])
                        df.at[index, "TO_CHECK"] = "{" + '"files_to_apply"' + ":" + '"ALL"' + "," + '"columns_to_apply"' + ":" + str(data["columnsToApply"]) + "}"
                    else:
                        data["columnsToApply"] = json.dumps(data["columnsToApply"])
                        data["filesToApply"] = json.dumps(data["filesToApply"])
                        df.at[index, "TO_CHECK"] = "{" + '"files_to_apply"' + ":" + str(data["filesToApply"]) + "," + '"columns_to_apply"' + ":" + str(data["columnsToApply"]) + "}" 
        with ExcelWriter(target,engine='openpyxl',mode='w') as writer:
            df.to_excel(writer,sheet_name="Sheet1",index=False)
        
        uploadFile.multi_part_upload("sharad-saurav-bucket", "Configuration.xlsx", target)
        os.remove(target)
        return "Succesfull"
    except Exception as e:
        traceback.print_exc()
        return str(e)

@app.route('/downloadConfig', methods=['GET'])
def downloadConfig():
    try:
        config_file = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/Configuration.xlsx'
        df = pd.read_excel(config_file, sheet_name="Sheet1")
        json_data = df.to_json(orient='records')
        return json_data
    except Exception as e:
        traceback.print_exc()
        return str(e)

@app.route('/uploadFileAndColumn', methods=['POST'])
def uploadFileAndColumn():
    try:
        print(request.data)
        fileName = json.loads(request.data.decode("utf-8"))['fileName']
        fileName = fileName + ".xlsx"
        columnNames = json.loads(request.data.decode("utf-8"))['columnNames']
        columnName = ''
        ctr = 0
        for col in columnNames:
            ctr = ctr + 1
            if(ctr == len(columnNames)):
                columnName  = columnName + '"'+ col +'"'
            else:
                columnName  = columnName + '"'+ col +'"' + ","
            
        checkColumn = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/checkColumn.xlsx'
        
        target1, headers = urllib.request.urlretrieve(checkColumn)
        df1 = pd.read_excel(checkColumn)
        
        fileList = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/fileList.xlsx'
        
        target2, headers = urllib.request.urlretrieve(fileList)
        
        df2=pd.read_excel(fileList)

        columnList = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/columnList.xlsx'
        target3, headers = urllib.request.urlretrieve(columnList)
        df3=pd.read_excel(columnList)


        if(fileName not in df2.values):
           row = [fileName]
           df2.loc[len(df2)] = row

        for columnNam in columnNames:
            if columnNam not in df3.values:
                row = [columnNam]
                df3.loc[len(df3)] = row
        
        if(fileName in df1.values):
            for index,row in df1.iterrows():
                if(row['File'] == fileName):
                    df1.at[index, "Columns"] = columnName
        else:
            row = [fileName, columnName]
            df1.loc[len(df1)] = row

        with ExcelWriter(target1,engine='openpyxl',mode='w') as writer:
            df1.to_excel(writer,sheet_name="Sheet1",index=False)
        
        with ExcelWriter(target2,engine='openpyxl',mode='w') as writer:
            df2.to_excel(writer,sheet_name="Sheet1",index=False)

        with ExcelWriter(target3,engine='openpyxl',mode='w') as writer:
            df3.to_excel(writer,sheet_name="Sheet1",index=False)

        uploadFile.multi_part_upload("sharad-saurav-bucket", "checkColumn.xlsx", target1)
        uploadFile.multi_part_upload("sharad-saurav-bucket", "fileList.xlsx", target2)
        uploadFile.multi_part_upload("sharad-saurav-bucket", "columnList.xlsx", target3)

        os.remove(target1)
        os.remove(target2)
        os.remove(target3)
        return "Succesfull"
    except Exception as e:
        traceback.print_exc()
        return str(e)

@app.route('/downloadFileAndColumnNames', methods=['GET'])
def downloadFileAndColumnNames():
    try:
        fileList = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/fileList.xlsx'
        df2=pd.read_excel(fileList)

        columnList = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/columnList.xlsx'
        df3=pd.read_excel(columnList)

        fileArray = df2.to_json(orient='values')
        columnNames = df3.to_json(orient='values')
        return {"fileArray": fileArray, "columnNames": columnNames}
    except Exception as e:
        traceback.print_exc()
        return str(e)

@app.route('/checkFile', methods=['GET'])
def checkFile():
    try:
        fileName = request.args.get("fileName")
        print('fileName--',fileName)
        fileName = fileName + ".xlsx"
        columns = []
        checkColumn = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/checkColumn.xlsx'
        df1 = pd.read_excel(checkColumn)
        if(fileName in df1.values):
            for index,row in df1.iterrows():
                if(row['File'] == fileName):
                    columns = row["Columns"]
        print(columns)
        columns = json.loads("[" + columns + "]")
        print(columns)
        array = []
        for col in columns:
            array.append({"name":col})
        return jsonify(array)    
    except Exception as e:
        traceback.print_exc()
        return str(e)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port, debug=True)
