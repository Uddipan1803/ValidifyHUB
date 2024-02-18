from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import mysql.connector
import os
import common_module_2

app = Flask(__name__)
app.secret_key = "abcd"

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "Uddipan",
    "password": "Dipto#1803",
    "database": "ericsson_project"
}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            query = "SELECT username FROM user WHERE username = %s"
            cursor.execute(query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Username is already taken. Please choose a different one.", 'danger')
            else:
                query = "INSERT INTO user (username, password) VALUES (%s, %s)"
                cursor.execute(query, (username, password))
                conn.commit()
                cursor.close()
                conn.close()
                flash("Registration successful! You can now log in.", 'success')
                return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('register.html')

# Define a route for user login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            query = "SELECT username, password FROM user WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and user['password'] == password:
                session['logged_in'] = True
                session['username'] = user['username']
                flash("Login successful!", 'success')
                return redirect(url_for('admin_panel'))
            else:
                flash("Login failed. Please check your credentials.", 'danger')

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('login.html')

@app.route("/admin_panel", methods=["GET", "POST"])
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    users = []

    if request.method == "POST" and "see_users" in request.form:
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # SQL query to fetch records from email_sample_1 table with initial status as 'not verified'
            query = "SELECT sl_no, name, email, status FROM email_sample_1"
            cursor.execute(query)
            users = cursor.fetchall()

            # Close the database connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template("admin_sample_1.html", users=users)

@app.route('/user_registration')
def user_registration():
    return render_template('add_user.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert the user's name and email into table
            query = "INSERT INTO email_sample_1 (name, email, status) VALUES (%s, %s, 'not verified')"
            cursor.execute(query, (name, email))

            # Commit the changes to the database
            conn.commit()

            # Close the database connection
            cursor.close()
            conn.close()

            # Redirect to the admin panel
            return redirect(url_for('admin_panel'))

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return "Invalid request"

@app.route("/generate_url/<int:sl_no>")
def generate_url(sl_no):
    # Store the user's sl_no and email in the session
    session['sl_no'] = sl_no

    # Generate a unique URL for the user
    unique_url = url_for("user_page", sl_no=sl_no, _external=True)

    # Return the generated URL as text
    return f"Generated URL for user with ID {sl_no} : <a href='{unique_url}'>{unique_url}</a>"


@app.route('/user/<int:sl_no>')
def user_page(sl_no):
    return render_template('upload2_2.html', sl_no=sl_no)

@app.route('/upload_aadhar', methods=['POST'])
def upload_aadhar_file():
    pdf_file = request.files.get('pdf_file') 
    sl_no = session.get('sl_no')

    if pdf_file:
        status_message = common_module_2.upload_and_process(pdf_file, common_module_2.process_aadhar, common_module_2.send_to_database_aadhar, sl_no)
        if status_message == "Successfully Uploaded":
            session['aadhar_submitted'] = True
            error_message_aadhar = ""
        else:
            error_message_aadhar = f'Aadhar Error: {status_message}'
    else:
        # No file was uploaded, set an error message
        error_message_aadhar = "No Aadhar file uploaded"

    aadhar_submitted = not bool(error_message_aadhar)
    session['pan_submitted'] = session.get('pan_submitted', False)
    session['marksheet_submitted'] = session.get('marksheet_submitted', False)

    response_data = {
        'aadhar_submitted': aadhar_submitted,
        'pan_submitted': session.get('pan_submitted', False),
        'marksheet_submitted': session.get('marksheet_submitted', False),
        'error_message_aadhar': error_message_aadhar,
        'error_message_pan': session.get('error_message_pan', ''),
        'error_message_marksheet': session.get('error_message_marksheet', ''),
        'sl_no': sl_no
    }

    return jsonify(response_data)


@app.route('/upload_pan', methods=['POST'])
def upload_pan_file():
    pdf_file = request.files.get('pdf_file') 
    sl_no = session.get('sl_no')

    if pdf_file:
        status_message = common_module_2.upload_and_process(pdf_file, common_module_2.process_pan, common_module_2.send_to_database_pan, sl_no)
        if status_message == "Successfully Uploaded":
            session['pan_submitted'] = True
            error_message_pan = ""
        else:
            error_message_pan = f'PAN Error: {status_message}'
    else:
        # No file was uploaded, set an error message
        error_message_pan = "No PAN file uploaded"

    pan_submitted = not bool(error_message_pan)
    session['aadhar_submitted'] = session.get('aadhar_submitted', False)
    session['marksheet_submitted'] = session.get('marksheet_submitted', False)

    response_data = {
        'aadhar_submitted': session.get('aadhar_submitted', False),
        'pan_submitted': pan_submitted,
        'marksheet_submitted': session.get('marksheet_submitted', False),
        'error_message_aadhar': session.get('error_message_aadhar', ''),
        'error_message_marksheet': session.get('error_message_marksheet',''),
        'error_message_pan': error_message_pan,
        'sl_no': sl_no
    }

    return jsonify(response_data)

@app.route('/upload_marksheet', methods=['POST'])
def upload_marksheet_file():
    pdf_file = request.files.get('pdf_file') 
    sl_no = session.get('sl_no')

    if pdf_file:
        status_message = common_module_2.upload_and_process(pdf_file, common_module_2.process_marksheet, common_module_2.send_to_database_marksheet, sl_no)
        if status_message == "Successfully Uploaded":
            session['marksheet_submitted'] = True
            error_message_marksheet = ""
        else:
            error_message_marksheet = f'Marksheet Error: {status_message}'
    else:
        # No file was uploaded, set an error message
        error_message_marksheet = "No Marksheet file uploaded"

    marksheet_submitted = not bool(error_message_marksheet)
    session['aadhar_submitted'] = session.get('aadhar_submitted', False)
    session['pan_submitted'] = session.get('pan_submitted', False)

    response_data = {
        'aadhar_submitted': session.get('aadhar_submitted', False),
        'marksheet_submitted': marksheet_submitted,
        'pan_submitted': session.get('pan_submitted', False),
        'error_message_aadhar': session.get('error_message_aadhar', ''),
        'error_message_pan': session.get('error_message_pan',''),
        'error_message_marksheet': error_message_marksheet,
        'sl_no': sl_no
    }

    return jsonify(response_data)


@app.route('/update_status', methods=['POST'])
def update_status():
    if session.get('aadhar_submitted') and session.get('pan_submitted') and session.get('marksheet_submitted'):
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            sl_no = session.get('sl_no')

            # Update the status of the user with the given sl_no to 'verified'
            query = "UPDATE email_sample_1 SET status = 'verified' WHERE sl_no = %s"
            cursor.execute(query, (sl_no,))

            # Commit the changes to the database
            conn.commit()

            # Close the database connection
            cursor.close()
            conn.close()

            # Reset the session flags
            session.pop('aadhar_submitted', None)
            session.pop('pan_submitted', None)
            session.pop('marksheet_submitted', None)

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)
