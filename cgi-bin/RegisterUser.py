            #!/usr/bin/env python3

print('Content-Type:text/html')
print("")

import mysql.connector
from mysql.connector import Error
import cgi
import cgitb

cgitb.enable()
input_data=cgi.FieldStorage()
print("<p>Made it</p>")
conn = None
cursor = None

profile_script_1 = '''
    <!doctype html>
    <html lang="en" class="no-js">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="canonical" href="https://html5-templates.com/" />
        <title>Hen Events</title>
        <meta name="description" content="Hen Events">
        <link rel="stylesheet" href="/WebContent/styles/style.css" />
        <script src="/WebContent/scripts/script.js"></script>
    </head>

    <body>
        <header>
            <div id="logo"><img src="/WebContent/images/flower-logo.png">Hen Events</div>
            <nav>  
                <ul>
                    <li><a href="/">Home</a>
                    <li><a href="/WebContent/services.html">Services</a>
                    <li><a href="/WebContent/booking.html">Booking</a>
                    <li><a href="/WebContent/about.html">About</a>
                    <li><a href="/WebContent/profile.html">Profile</a>
                </ul>
            </nav>
        </header>
        <section>
            <strong>Profile</strong>
        </section>
        <section id="pageContent">
            <div class="card rounded">'''

profile_script_2 = '''
    </div>
	</section>
	<footer>
		<p>&copy; 2020 by Hen Events | 3607 Trousdale Pkwy Los Angeles, CA 90089 | info@henevents.com</p>
	</footer>
</body>

</html>'''

try:
    conn = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password='password')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hen")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS 'users' (
                user_id INT(6) NOT NULL AUTO_INCREMENT,
                fname VARCHAR(20)  NOT NULL,
                lname VARCHAR(20) NOT NULL,
                email VARCHAR(30) NOT NULL,
                password VARCHAR(20) NOT NULL,
                CONSTRAINT user_pk PRIMARY KEY (user_id))
            ''')
        try:
            fname = input_data["fname"].value
            lname = input_data["lname"].value
            email = input_data["email"].value
            password = input_data["password"].value
            confpassword = input_data["confpassword"].value
            try:
                if fname is None:
                    print("<p>First name cannot be blank</p>")
                if lname is None:
                    print("<p>Last name cannot be blank</p>")
                if email is None:
                    print("<p>Email cannot be blank</p>")
                if password is None:
                    print("<p>Password cannot be blank</p>")
                elif password == confpassword:
                    cursor.execute("INSERT INTO users (fname, lname, email, password) VALUES ({0}, {1}, {2}, {3})".format(fname, lname, email, password))
                    print(profile_script_1)
                    print("<p>Hello {0} {1}!</p>".format(fname, lname))
                    print("<p>Your email is: {0}</p><br>".format(email))
                    print("<p><a href='/'><button type='button' class='button'>Logout</button></a></p>")
                    print(profile_script_2)
                else:
                    print("<p>Passwords do not match</p>")

        else:
            print("<p>Error reading the form</p>")
    else:
        print('<p>Unable to connect to MySQL database</p>')
except Error as e:
    print('<p>',e,'</p>')

finally:
    if conn is not None and conn.is_connected():
        conn.close()

