#!/usr/bin/env python3

print('Content-Type:text/html')
print("")

import mysql.connector
from mysql.connector import Error
import cgi
import cgitb

cgitb.enable(display=0, logdir="/logs")
input_data=cgi.FieldStorage()
conn = None
cursor = None

profile_script_1 = '''
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
</body>'''
print(profile_script_1)
error = False
try:
    conn = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password='password')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hen")
        cursor.execute("USE hen")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                fname VARCHAR(20)  NOT NULL,
                lname VARCHAR(20) NOT NULL,
                email VARCHAR(30) NOT NULL,
                pw VARCHAR(20) NOT NULL)
            ''')
        try:
            try:
                if not input_data["email"]:
                    print("<p>Email cannot be blank</p>")
                    error = True
                if not input_data["password"]:
                    print("<p>Password cannot be blank</p>")
                    error = True
                if error == False:
                    sql = "SELECT * FROM users WHERE email='" + input_data["email"].value + "' AND email='" + input_data["email"].value + "'"
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    if row is None:
                        print("<p>User not found</p>")
                    else:
                        print("<p>Hello {0} {1}!</p>".format(row["fname"], row["lname"]))
                        print("<p>Your email is: {0}</p><br>".format(row["email"]))
                        print("<p><a href='/'><button type='button' class='button'>Logout</button></a></p>")
            except KeyError as ke:
                print("<p>Form values cannot be blank!</p>")
                error = True
            except Error as e:
                print("<p>", e, "</p>")
            finally:
                cursor.close()
        except Error as e:
                print("<p>Error reading the form</p>")
                error = True
    else:
        print('<p>Unable to connect to MySQL database</p>')
        error = True
except Error as e:
    print('<p>',e,'</p>')
    error = True
finally:
    if conn is not None and conn.is_connected():
        conn.close()
    if error == True:
        print("<br><p><a href='/WebContent/register.html'><button type='button' class='button'>Return to Form</button></a></p>")
    print(profile_script_2)
