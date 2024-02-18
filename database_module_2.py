import mysql.connector

def send_to_database_aadhar(name, dob, gender, num, sl_no):
    host = "localhost"
    user = "Uddipan"
    password = "Dipto#1803"
    database = "ericsson_project"

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected")

    cursor = connection.cursor()

    insert_query = "INSERT INTO aadhar2 (name, user_sl_no, date_birth, gender, aadhar_no) VALUES (%s, %s, %s, %s, %s)"
    data_to_insert = ( name, sl_no,  dob, gender, num)

    cursor.execute(insert_query, data_to_insert)
    connection.commit()
    cursor.close()
    connection.close()

def send_to_database_pan(name, dob, pan, sl_no):
    host = "localhost"
    user = "Uddipan"
    password = "Dipto#1803"
    database = "ericsson_project"

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected")

    cursor = connection.cursor()

    insert_query = "INSERT INTO pan2 (name, user_sl_no, date_birth, pan_no) VALUES (%s, %s, %s, %s)"
    data_to_insert = ( name, sl_no, dob, pan)

    cursor.execute(insert_query, data_to_insert)
    connection.commit()
    cursor.close()
    connection.close()

def send_to_database_marksheet(name, subjects_and_marks, sl_no):
    host = "localhost"
    user = "Uddipan"
    password = "Dipto#1803"
    database = "ericsson_project"

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected")

    cursor = connection.cursor()
    insert_query = "INSERT INTO marksheet_users (name, user_sl_no) VALUES (%s, %s)"
    data_to_insert = (name, sl_no)
    cursor.execute(insert_query, data_to_insert)
    connection.commit()
    
    for entry in subjects_and_marks:
        subject = entry['subject']
        marks = entry['marks']

        # SQL query to insert values into the database
        insert_query = "INSERT INTO user_marks (user_sl_no, subject, marks) VALUES (%s, %s, %s)"
        
        # Execute the query with the values
        cursor.execute(insert_query, (sl_no, subject, marks))
        connection.commit()
    
    cursor.close()
    connection.close()    