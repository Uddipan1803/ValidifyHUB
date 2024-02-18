from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import webbrowser
import os

app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "Uddipan",
    "password": "Dipto#1803",
    "database": "ericsson_project"
}

# Full path to appcom3.py
appcom3_path = r'"D:\Ericsson Project\appcom3.py"'

@app.route("/", methods=["GET", "POST"])
def admin_panel():
    users = []

    if request.method == "POST" and "see_users" in request.form:
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # SQL query to fetch records from email_sample table
            query = "SELECT sl_no, name, email FROM email_sample"
            cursor.execute(query)
            users = cursor.fetchall()

            # Close the database connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template("admin_sample.html", users=users)

@app.route("/generate_url/<int:sl_no>")
def generate_url(sl_no):
    # Generate a unique URL for the user
    unique_url = f"http://localhost:5000/user/{sl_no}"

    # Start appcom3.py using the full path
    os.system(f"python {appcom3_path}")

    # Open the web browser to the unique URL
    webbrowser.open(unique_url)

    return f"Generated URL for user with ID {sl_no}: <a href='{unique_url}'>{unique_url}</a>"

if __name__ == "__main__":
    app.run(debug=True)
