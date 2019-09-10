from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import json
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
import Summary
import Time_in_HH_MM_SS_format
import uploadFile
import requests
import urllib.request

app = Flask(__name__, static_url_path='')
CORS(app)
ALLOWED_EXTENSIONS = set([ 'xls', 'xlsx'])

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 5002))

@app.route('/')
def root():
    return app.send_static_file('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/parse_table', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
        uploaded_files = request.files.getlist("file")
        milliseconds = request.args.get("milliseconds")
        print(milliseconds)
        for file in uploaded_files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                
                filename = secure_filename(file.filename)
                link = 'https://s3.us-east.cloud-object-storage.appdomain.cloud/sharad-saurav-bucket/DataFiles_Rules_Report.xlsx'
                target, headers = urllib.request.urlretrieve(link)
                print(target, headers)
                
                newTar = target + ".xlsx"
                os.rename(target, newTar)
                
                Allowed_intents_in_Unstructured.rule_unstructured(file, filename, newTar)
                Check_for_capitalization.rule_capitalization(file, filename, newTar)
                Check_for_duplicates.rule_duplicates(file, filename, newTar)
                Check_for_missing_Keyword.rule_missing_keyword(file, filename, newTar)
                Check_for_capitalization.rule_capitalization(file, filename, newTar)
                Correctness_of_MAP_URL.rule_map_url(file, filename, newTar)
                Correctness_of_Short_Ref_URL.short_ref_url(file, filename, newTar)
                Date_in_YYYY_MM_DD_format.date_format(file, filename, newTar)
                Description_text_not_same.description_text(file, filename, newTar)
                Duplicate_in_Entity_Interactn.duplicate_entity_interaction(file, filename, newTar)
                Email_id_validity.email_id_validity(file, filename, newTar)
                Exact_dates_available.exact_dates_available(file, filename, newTar)
                Exceeding_500_characters.exceeding_500_characters(file, filename, newTar)
                Latitude_Longitude.latitide_longitude(file, filename, newTar)
                Multiple_Spaces_in_txt.multiple_spaces_in_txt(file, filename, newTar)
                No_content_in_brackets.no_content_in_brackets(file, filename, newTar)
                No_AcadEvents_in_Timing.no_acadEvents_in_timing(file, filename, newTar)
                No_date_special_characters.No_date_special_characters(file, filename, newTar)
                No_phone_url_in_voice.no_phone_url_in_voice(file, filename, newTar)
                No_preceeding_0_in_room_no.no_preceeding_0_in_room_no(file, filename, newTar)
                No_Ref_URL_in_text.no_ref_url_in_text(file, filename, newTar)
                No_sentence_in_virtual_entity.no_sentence_in_virtual_entity(file, filename, newTar)
                No_timing_for_acad_events.no_timing_for_acad_events(file, filename, newTar)
                No_timings_values_in_txt.no_timings_values_in_txt(file, filename, newTar)
                Numbering_bullet_points.numbering_bullet_points(file, filename, newTar)
                Perfect_Excel_format.perfect_excel_format(file, filename, newTar)
                Process_ID.process_id(file, filename, newTar)
                Special_Char_in_Entity_Name.special_char_in_entity_name(file, filename, newTar)
                Start_date_less_than_end_date.start_date_less_than_end_date(file, filename, newTar)
                Start_time_less_than_end_time.start_time_less_than_end_time(file, filename, newTar)
                Time_in_HH_MM_SS_format.time_in_hh_mm_ss_format(file, filename, newTar)
                Summary.summary(file, filename, newTar)
                test.var = True
        uploadFile.multi_part_upload("sharad-saurav-bucket", "DataFiles_Rules_Report" + milliseconds + ".xlsx", newTar)
        return  getJson.get_Json_data(newTar)
    else:
        print('check---------------------------------------------------------------------------------------------------------------------------')
        return jsonify(result={"status": 400})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port, debug=True)
