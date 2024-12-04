# Isabella Persky
# Flask app to manage user login and access level display on the dashboard page

from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = 'mocha'  # Not sure when I need to use this key?

# Function to establish database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function for custom hash verification
def verify_password(stored_hash, input_password):
    # Extract the salt and hashed password
    salt = stored_hash[:40]  # The first 40 characters are the salt
    expected_hash = stored_hash[40:]  # The remainder is the SHA-1 hash

    # Combine the salt with the input password and hash it
    hashable = (salt + input_password).encode('utf-8')
    input_hash = hashlib.sha1(hashable).hexdigest()

    # Password verfication, compares expected hash with the computed hash
    return input_hash == expected_hash
    
# Home route to check for successful user login
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard')) # Redirects to dashboard if user is logged in
    return redirect(url_for('login')) # Redirects to login page if not logged in successfully

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] # Get the username from the form
        password = request.form['password'] # Get the password from the form
        
        # Query database to get user credentials based on username
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone() # Gets the first matching user
        conn.close()
        
        # Check if the user exists and the password matches
        if user and verify_password(user['password'], password):
            session['username'] = username
            session['access_level'] = user['access_level']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Invalid username or password', 'danger')  # Display error message if invalid login
    
    return render_template('login.html', title="Login")
    
# Dashboard route, displayed after successful login
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard', 'danger')
        return redirect(url_for('login'))
    
    username = session['username']  # Gets the logged in username from the session
    access_level = session['access_level']  # Gets the access level from the session
    
    # Define menu options based on the user's access level
    menu_options = {
        'admin': ["Time Reporting", "Accounting", "Register New User"],
        'manager': ["Time Reporting", "Register New User"],
        'employee': ["Time Reporting"]
    }
    
    return render_template('dashboard.html', username=username, menu_options=menu_options[access_level])

# Logout route, clears session and logs user out of system
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))  # Redirect to the home page when clicked

if __name__ == '__main__':
    app.run(debug=True)
