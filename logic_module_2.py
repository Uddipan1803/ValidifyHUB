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
        

        
def marksheet_details(extracted_text):
        pattern_1 = r'COUNCIL FOR THE INDIAN SCHOOL CERTIFICATE EXAMINATIONS'
        pattern_3 = r'\b(\d{7})\b'
        pattern_2 = r'CENTRAL BOARD OF SECONDARY EDUCATION'
        pattern_4 = r'\b(\d{8})\b'
        
        match_1 = re.search(pattern_1, extracted_text)
        match_3 = re.search(pattern_3, extracted_text)
        match_2 = re.search(pattern_2, extracted_text)
        match_4 = re.search(pattern_4, extracted_text)

        if match_1 and match_3:
            status = 'SUCCEEDED'
            # 1. Extract Name
            name_pattern = r'Name ([A-Z\s]+)'
            name_match = re.search(name_pattern, extracted_text)
            name = name_match.group(1).strip()

            # 2. Find the index of the line containing the word "ENGLISH"
            
            english_line_number = None
            lines = extracted_text.split('\n')
            for i, line in enumerate(lines):
                if 'ENGLISH' in line:
                    english_line_number = i  # Adding 1 to convert from zero-based index to line number
                    break
             
            # 3. Extract subjects and marks
            subjects_and_marks = []
            for i in range(english_line_number, english_line_number+12, 2):
                subject_line = lines[i].strip()
                marks_line = lines[i + 1].strip() if i + 1 < len(lines) else None

                subjects_and_marks.append({
                    'subject': subject_line,
                    'marks': marks_line
                })   

            return status, name, subjects_and_marks

        elif match_2 and match_4:
            status = 'SUCCEEDED'
            # 1. Extract Name
            name_pattern = r'This is to certify that ([A-Z\s]+)'
            name_match = re.search(name_pattern, extracted_text)
            name = name_match.group(1).strip()
            name = name[:-1]
            
            # 2. Find the index of the line containing the word "ENGLISH"
            english_line_number = None
            lines = extracted_text.split('\n')
            for i, line in enumerate(lines):
                if 'ENGLISH CORE' in line:
                    english_line_number = i  # Adding 1 to convert from zero-based index to line number
                    break
             
            # 3. Extract subjects and marks
            subjects_and_marks = []
            for i in range(english_line_number, english_line_number+42, 7):
                subject_line = lines[i].strip()
                marks_line = lines[i + 3].strip() if i + 3 < len(lines) else None

                subjects_and_marks.append({
                    'subject': subject_line,
                    'marks': marks_line
                })
                
            return status, name, subjects_and_marks
        
        else:
            status = 'FAILED'
            return status, "", ""