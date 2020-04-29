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

def setLoggedIn(user_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM loggedin_user")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO loggedin_user (zero,id) VALUES (0,{0})".format(user_id))
    else:
        cursor.execute("UPDATE loggedin_user SET id={0} WHERE zero=0".format(user_id))
    conn.commit()
    cursor.close()

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

def checkTableExists(conn, tablename):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'".format(tablename))
    if cursor.fetchone()[0] == 1:
        cursor.close()
        return True
    cursor.close()
    return False

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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loggedin_user (
                zero INT(1) PRIMARY KEY,
                id INT(6),
                CONSTRAINT fk_id FOREIGN KEY (id) REFERENCES users(user_id)
            )''')
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(30)  NOT NULL,
                    price INT(3) NOT NULL)
                ''')
        cursor.execute("INSERT INTO products (name, price) VALUES ('{0}', {1})".format("Full Package", 150))
        cursor.execute("INSERT INTO products (name, price) VALUES ('{0}', {1})".format("Partial Package", 100))
        cursor.execute("INSERT INTO products (name, price) VALUES ('{0}', {1})".format("Simple Package", 80))
        cursor.execute("INSERT INTO products (name, price) VALUES ('{0}', {1})".format("The Basics", 70))
        conn.commit()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                user_id INT(6) NOT NULL,
                product_id INT(6) NOT NULL,
                name VARCHAR(50) NOT NULL,
                date VARCHAR(10) NOT NULL,
                time VARCHAR(10) NOT NULL,
                pay_status INT(1) NOT NULL,
                CONSTRAINT fk_userid FOREIGN KEY (user_id) REFERENCES users(user_id),
                CONSTRAINT fk_productid FOREIGN KEY (product_id) REFERENCES products(product_id))
                ''')
        conn.commit()
        try:
            try:
                email = input_data["email"].value
                password = input_data["password"].value
                cursor.execute("SELECT * FROM users WHERE email='" + input_data["email"].value + "'")
                row = cursor.fetchone()
                if row is None:
                    print("<p>No user registered with that email</p>")
                    error = True
                elif row[4] != password:
                    print("<p>Incorrect password</p>")
                    error = True
                else:
                    setLoggedIn(row[0], conn)
                    print("<p>Hello {0} {1}!</p>".format(row[1], row[2]))
                    print("<p>Your email is: {0}</p><br>".format(row[3]))
                    print("<p>My events: ")
                    cursor.execute("SELECT * FROM orders WHERE user_id={0}".format(row[0]))
                    records = cursor.fetchall()
                    if len(records) == 0:
                        print("<b>No events scheduled yet.</b></p><br>")
                    else:
                        print("</p><br>")
                        for row in records:
                            print("<p>Event {0} -- {1} -- {2} on {3} -- Bundle not yet shipped</p><br>".format(row[0] + 1, row[2], row[4], row[3]))
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
        print("<br><p><a href='/WebContent/login.html'><button type='button' class='button'>Return to Login</button></a></p>")
    print(profile_script_2)
