from flask import Flask, render_template, request, redirect, url_for, session
import socket
import sys
import pandas as pd
# import yagmail
import numpy as np

app = Flask(__name__)
app.secret_key = 'honeypot'

# Employee


@app.route('/emp/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        password = request.form['Password']
        last_name = request.form['Last_name']
        sex = request.form['gender']
        city = request.form['city']
        country = request.form['country']

        # Load the existing users data from the Excel file
        try:
            df = pd.read_excel('employee.xlsx')
        except FileNotFoundError:
            # If the file doesn't exist, create an empty DataFrame
            df = pd.DataFrame()

        # Create column names if they don't exist
        if df.empty:
            column_names = ['name', 'last_name', 'gender',
                            'email', 'password', 'city', 'country']
            df = pd.DataFrame(columns=column_names)

        # Add the new user to the DataFrame
        new_user = pd.DataFrame({'name': [name],
                                 'last_name': [last_name],
                                 'gender': [sex],
                                 'email': [email],
                                 'password': [password],
                                 'city': [city],
                                 'country': [country]})
        df = df.append(new_user, ignore_index=True)

        # Write the DataFrame back to the Excel file
        df.to_excel('employee.xlsx', index=False)

        if sex == 'Male':
            msg = "Hello Mr. {} !! You can login Here !!!".format(name)
        else:
            msg = "Hello Ms. {} !! You can login Here !!!".format(name)
        return render_template('emp/login.html', msg=msg, email=email)

    return render_template('emp/register.html')


@app.route('/')
@app.route('/home')
def home():
    return render_template('emp/home.html')


@app.route('/emp/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        # Load the existing users data from the Excel file
        try:
            df = pd.read_excel('employee.xlsx')
        except FileNotFoundError:
            return "User data file not found"

        # Check if the email and password match any row in the Excel sheet
        user = df[(df['email'] == email) & (df['password'] == password)]
        if not user.empty:
            # Set email in the session
            session['email'] = email

            return redirect(url_for('index'))
        else:
            msg = 'Invalid Login Details. Please Try Again.'
            return render_template('emp/login.html', msg=msg, email=email)
    return render_template('emp/login.html')


@app.route('/emp/password', methods=['POST', 'GET'])
def emppassword():
    if 'email' in session:
        email = session['email']  # Retrieve email from session

        if request.method == 'POST':
            current_pass = request.form['current']
            new_pass = request.form['new']
            verify_pass = request.form['verify']
            # email = request.form['email']  # No need to get email from form since we have it in session

            # Load user data from the Excel file
            try:
                df = pd.read_excel('employee.xlsx')
            except FileNotFoundError:
                return "User data file not found"

            # Check if the email exists and if the current password matches
            user = df[df['email'] == email]
            if not user.empty:
                if user['password'].iloc[0] == current_pass:
                    if new_pass == verify_pass:
                        # Update the password in the DataFrame
                        df.loc[df['email'] == email, 'password'] = new_pass
                        # Write the updated DataFrame back to the Excel file
                        df.to_excel('employee.xlsx', index=False)
                        msg1 = 'Password changed successfully'
                        return render_template('emp/password.html', msg1=msg1)
                    else:
                        msg2 = 'Re-entered password does not match'
                        return render_template('emp/password.html', msg2=msg2)
                else:
                    msg3 = 'Incorrect current password'
                    return render_template('emp/password.html', msg3=msg3)
            else:
                msg3 = 'User not found'
                return render_template('emp/password.html', msg3=msg3)

        return render_template('emp/password.html')
    return render_template('emp/login.html')


@app.route('/emp/logout')
def logout():
    # Clear the session data
    session.pop('email', None)
    # Redirect the user to the login page
    return redirect(url_for('login'))


@app.route("/emp/index")
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("emp/index.html")

# Admin


@app.route('/admin/register', methods=['POST', 'GET'])
def a_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        password = request.form['Password']
        last_name = request.form['Last_name']
        sex = request.form['gender']
        city = request.form['city']
        country = request.form['country']

        # Load the existing users data from the Excel file
        try:
            df = pd.read_excel('admin.xlsx')
        except FileNotFoundError:
            # If the file doesn't exist, create an empty DataFrame
            df = pd.DataFrame()

        # Create column names if they don't exist
        if df.empty:
            column_names = ['name', 'last_name', 'gender',
                            'email', 'password', 'city', 'country']
            df = pd.DataFrame(columns=column_names)

        # Add the new user to the DataFrame
        new_user = pd.DataFrame({'name': [name],
                                 'last_name': [last_name],
                                 'gender': [sex],
                                 'email': [email],
                                 'password': [password],
                                 'city': [city],
                                 'country': [country]})
        df = df.append(new_user, ignore_index=True)

        # Write the DataFrame back to the Excel file
        df.to_excel('admin.xlsx', index=False)

        if sex == 'Male':
            msg = "Hello Mr. {} !! You can login Here !!!".format(name)
        else:
            msg = "Hello Ms. {} !! You can login Here !!!".format(name)
        return render_template('admin/login.html', msg=msg, email=email)

    return render_template('admin/register.html')


@app.route('/admin/login', methods=['POST', 'GET'])
def a_login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        # Load the existing users data from the Excel file
        try:
            df = pd.read_excel('admin.xlsx')
        except FileNotFoundError:
            return "User data file not found"

        # Check if the email and password match any row in the Excel sheet
        user = df[(df['email'] == email) & (df['password'] == password)]
        if not user.empty:
            return redirect(url_for('all_ip'))
        else:
            msg = 'Invalid Login Details. Please Try Again.'
            return render_template('admin/login.html', msg=msg, email=email)
    return render_template('admin/login.html')


@app.route('/admin/password', methods=['POST', 'GET'])
def adminpassword():

    if request.method == 'POST':
        current_pass = request.form['current']
        new_pass = request.form['new']
        verify_pass = request.form['verify']
        email = request.form['email']

        # Load user data from the Excel file
        try:
            df = pd.read_excel('admin.xlsx')
        except FileNotFoundError:
            return "User data file not found"

        # Check if the email exists and if the current password matches
        user = df[df['email'] == email]
        if not user.empty:
            if user['password'].iloc[0] == current_pass:
                if new_pass == verify_pass:
                    # Update the password in the DataFrame
                    df.loc[df['email'] == email, 'password'] = new_pass
                    # Write the updated DataFrame back to the Excel file
                    df.to_excel('admin.xlsx', index=False)
                    msg1 = 'Password changed successfully'
                    return render_template('admin/password.html', msg1=msg1)
                else:
                    msg2 = 'Re-entered password does not match'
                    return render_template('admin/password.html', msg2=msg2)
            else:
                msg3 = 'Incorrect current password'
                return render_template('admin/password.html', msg3=msg3)
        else:
            msg3 = 'User not found'
            return render_template('admin/password.html', msg3=msg3)

    return render_template('admin/password.html')


port = 5003


class Client:
    def __init__(self, ip):
        self.content = None
        self.ip = ip
        self.port = port

    def send_file(self, file):
        self.content = file.read()
        return self.content

    def connect(self, selected_file, filename, email):
        try:
            s = socket.socket()
            s.connect((self.ip, self.port))
            print("Connected to server")

            s.recv(1024)

            content = self.send_file(selected_file)
            s.send(content)
            print("File content sent")

            s.recv(2048)

            s.send(filename.encode("utf-8"))
            print("Filename sent")

            s.recv(1024)

            s.send(email.encode("utf-8"))
            print("Email sent")

            s.recv(1024)

            s.close()

        except Exception as e:
            print("[ERROR] Oops something went wrong, check below error message")
            print("[ERROR MESSAGE] ", e)


@app.route('/emp/submit', methods=['POST'])
def submit():
    ip = request.form['ip']
    filename = request.form['filename']
    email = request.form['email']
    selected_file = request.files['option']

    client = Client(ip)
    client.connect(selected_file, filename, email)

    print("Successfully Shared.")

    message = "File Shared Successfully."

    return render_template('emp/index.html', msg=message)


def read_excel(file):
    df = pd.read_excel(file)
    cols = list(df.columns)
    df1 = np.asarray(df)
    length = len(df1)
    df2 = []
    count = length
    for i in range(length):
        df2.append(df1[count - 1])
        count -= 1
    print("df2: ", df2)
    return cols, df2


@app.route("/clear_data", methods=['GET', 'POST'])
def clear_data():
    df1 = pd.read_excel('ip_log.xlsx')
    df1.drop(df1.index, inplace=True)
    df1.to_excel('ip_log.xlsx', index=False)
    return redirect(url_for('home'))


@app.route("/admin/all_ip", methods=['GET', 'POST'])
def all_ip():
    data = read_excel(
        'C:/MyProject/Abishek_Delivery/honeypot_K/server/ip_log.xlsx')
    title = "List of All Clients"
    return render_template("admin/index.html", title=title, cols=data[0], values=data[1])


if __name__ == '__main__':
    app.run(debug=True, port=4892)
