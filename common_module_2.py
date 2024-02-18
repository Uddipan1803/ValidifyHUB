from flask import request
import extract_module
import logic_module_2
import database_module_2

def upload_and_process(pdf_file, process_function, send_function, sl_no):
    if pdf_file:
        status, extracted_text = extract_module.upload_and_extract_text(pdf_file)
        if status == 'FAILED' or status == 'PARTIAL_SUCCESS':
            return 'Extraction Failed'
        else:
            result = process_function(extracted_text)
            if result[0] == 'FAILED':
                return 'Incorrect PDF'
            else:
                if send_function:
                    send_function(result, sl_no)
                return 'Successfully Uploaded'
    return 'No File Uploaded'

def process_aadhar(extracted_text):
    return logic_module_2.aadhar_details(extracted_text)

def process_pan(extracted_text):
    return logic_module_2.pan_details(extracted_text)

def process_marksheet(extracted_text):
    return logic_module_2.marksheet_details(extracted_text)

def send_to_database_aadhar(result, sl_no):
    name, dob, gender, num = result[1], result[2], result[3], result[4]
    database_module_2.send_to_database_aadhar(name, dob, gender, num, sl_no)

def send_to_database_pan(result, sl_no):
    name, dob, pan = result[1], result[2], result[3]
    database_module_2.send_to_database_pan(name, dob, pan, sl_no)
    
def send_to_database_marksheet(result, sl_no):
    name = result[1]
    subjects_and_marks = result[2]
    database_module_2.send_to_database_marksheet(name, subjects_and_marks, sl_no)