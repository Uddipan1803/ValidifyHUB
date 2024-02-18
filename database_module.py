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
