#!/usr/bin/env python3

###########################################################################
print('Content-Type:text/html') #HTML is following
print("")                          #Leave a blank line

###########################################################################

import mysql.connector
from mysql.connector import Error

conn = None
try:
    conn = mysql.connector.connect(host='localhost',
                                   database='python_mysql',
                                   user='root',
                                   password='alexander')
    if conn.is_connected():
        print('<p>Connected to MySQL database</p>')
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            row = cursor.fetchone()
            while row is not None:
                print('<p>',row,'</p>')
                row = cursor.fetchone()
        except Error as e:
            print('<p>',e,'</p>')
        finally:
            cursor.close()
            print('<p>Cursor closed</p>')
########        
    else:
        print('<p>Unable to connect to MySQL database</p>')

except Error as e:
        print('<p>',e,'</p>')

finally:
    if conn is not None and conn.is_connected():
        conn.close()
        print('<p>Connection closed</p>')

###########################################################################

import cgi
import cgitb
cgitb.enable()

input_data=cgi.FieldStorage()

print('<h1>Addition Results</h1>')
try:
  num1=int(input_data["num1"].value)
  num2=int(input_data["num2"].value)
except:
  print('<p>Sorry, we cannot turn your inputs into numbers (integers).</p>')
#  return(1)
sum=num1+num2
print('<p>{0} + {1} = {2}</p>'.format(num1,num2,sum))

