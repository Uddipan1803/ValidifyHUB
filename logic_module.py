import re

def aadhar_details(extracted_text):
        pattern = r'\d{4} \d{4} \d{4}'  
        has_12_digit_number = re.search(pattern, extracted_text)

        if has_12_digit_number:
                    status = 'SUCCEEDED'
                    num = has_12_digit_number.group()
                    date_pattern = r'\d{2}/\d{2}/\d{4}'
                    dob_match = re.search(date_pattern, extracted_text)

                    lines = extracted_text.split('\n')
                    dob = dob_match.group()
                    name_index = None
                    for i, line in enumerate(lines):
                        if re.search(date_pattern, line) and i > 0:
                            name_index = i-1
                            break
                                    
                    name = lines[name_index]
                    gender_pattern = r'\b(MALE|FEMALE)\b'
                    gender_match = re.search(gender_pattern, extracted_text, re.IGNORECASE)
                    gender = gender_match.group().upper()
                    return status, name, dob, gender, num
        else:
                    status = 'FAILED'
                    return status,"","","",""

def pan_details(extracted_text):
        pattern = r'[A-Z]{5}\d{4}[A-Z]{1}'  
        has_pan = re.search(pattern, extracted_text)

        if has_pan:
                    status = 'SUCCEEDED'
                    pan = has_pan.group()
                    date_pattern = r'\b(\d{2})[-/](\d{2})[-/](\d{4})\b'
                    date_match = re.search(date_pattern, extracted_text)
                    day, month, year = date_match.groups()
                    dob = f"{day}/{month}/{year}"

                    lines = extracted_text.split('\n')
                    name_index = None
                    i=0
                    for i, line in enumerate(lines):
                        if re.search('NAME', line) or re.search('Name',line):
                            name_index=i+1
                            break
                                    
                    name = lines[name_index]
                    return status, name, dob, pan
        else:
                    status = 'FAILED'
                    return status,"","",""
                

                

        

        
        