Isabella Persky

Catamount Company Intranet System Program
-------------------------------
Overview: 
The Catamount Company Intranet System is a program that simulates a company intranet login system. Employees, managers, and admin can log in with their credentials, and based on their role (access level), they'll get access to different parts of the system. A Flask-based web interface complements the system, providing a secure and user friendly login page.

Access levels:
1. Admin (full access) - Time Reporting, Accounting, Register New User
2. Manager (limited access) - Time Reporting, Register New User
3. Employee (most limited access) - Time Reporting

How it works:
- Users log into the system (3 attempts).
- After successfully logging in, the system identifies the user's access level and displays a menu based on their role.
- The user can then navigate through the system and perform actions permitted by their access level (the only menu item that can actually be executed is registering a new user).

Testing instructions:
1. Navigate to the correct directory where program is located.
2. Run the flask app by executing command "python app.py". Go to browser and open up local server URL.
3. Log onto the system using the sample credentials I provided below.
4. If you would like to test the functionality of adding a user, run the intranet_system.py script by executing the command "python intranet_system.py". Then, log in using the admin or manager credentials listed below (as employees cannot register new users), and follow the given prompts. Test the system by attempting to log in with the newly created user credentials in your browser.

User credentials to test system (access level, username, password):
admin, ipersky, Simba7!?
manager, jeddy, R7w!F12Av77v=K+))W2,t
employee, tester, Ihatecheesecake123!

Notes:
- Original user credentials were transferred from the users CSV file to the users.db file. This step ensured that I was able to log on first and then add more users afterward.
- The 3 login attempts only works when logging onto the system via the intranet_system.py script (it does not apply to the browser-based login, whoops).

Citations
Flask Documentation: https://flask.palletsprojects.com/
SQLite Documentation: https://www.sqlite.org/docs.html
Python hashlib library: https://docs.python.org/3/library/hashlib.html
Python re library: https://docs.python.org/3/library/re.html
General Python built-in functions: https://docs.python.org/3/library/functions.html
HTML files: https://www.w3schools.com/html/html_intro.asp and I used Jim Eddy's files from the Catamount Bank program as an outline.
