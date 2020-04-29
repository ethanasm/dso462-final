#!/usr/bin/env python3

print('Content-Type:text/html')
print("")

import mysql.connector
from mysql.connector import Error
import cgi
import cgitb
import traceback

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
        try:
            try:
                user_id = input_data["user_id"].value
                prod_id = input_data["prod_id"].value
                ename = input_data["ename"].value
                date = input_data["date"].value
                time = input_data["time"].value
                cursor.execute("INSERT INTO orders (user_id, product_id, name, date, time, pay_status) VALUES ({0},{1},'{2}','{3}','{4}',0)".format(user_id, int(prod_id) + 1, ename, date, time,))
                conn.commit()
                cursor.execute("SELECT * FROM users WHERE user_id={0}".format(user_id))
                row = cursor.fetchone()
                print("<p>Hello {0} {1}!</p>".format(row[1], row[2]))
                print("<p>Your email is: {0}</p><br><br>".format(row[3]))
                print("<p>My events: </p><br>")
                cursor.execute("SELECT * FROM orders WHERE user_id={0}".format(user_id))
                records = cursor.fetchall()
                if records is None:
                    print("<p>No events scheduled yet.</p>")
                else:
                    for row in records:
                        print("<p>Event {0} -- {1} -- {2} on {3} -- Bundle not yet shipped</p><br>".format(row[0], row[3], row[5], row[4]))
                print("<p><a href='/'><button type='button' class='button'>Logout</button></a></p>")
            except KeyError as ke:
                print("<p>Form values cannot be blank!</p>")
                error = True
            except Error as e:
                print("<p>", traceback.format_exc(), "</p>")
            finally:
                cursor.close()
        except Error as e:
                print("<p>Error reading the form</p>")
                error = True
    else:
        print('<p>Unable to connect to MySQL database</p>')
        error = True
except Error as e:
    print('<p>',traceback.format_exc(),'</p>')
    error = True
finally:
    if conn is not None and conn.is_connected():
        conn.close()
    if error == True:
        print("<br><p><a href='/WebContent/register.html'><button type='button' class='button'>Return to Registration</button></a></p>")
    print(profile_script_2)
