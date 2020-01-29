import os
import re
import mysql.connector
from mysql.connector import Error

db_username = os.environ['USERNAME']
db_password = os.environ['PASSWORD']
database = os.environ['DATABASE']
host = os.environ['HOST']
port = '37306'


def get_cart_details():
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        print(connection)
        cursor = connection.cursor()
        print(cursor)
        cursor.execute('SELECT * FROM tblGuestCart')
        cart_details = cursor.fetchall()
        print(cart_details)
        return cart_details
    except Error as e:
        print( 'Error getting cart info')


def get_product_by_id(ProductID):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tblProduct')
        product_details = cursor.fetchall()

        for prod in product_details:
            if prod[0]==int(ProductID):
                details=prod
        return  details
    except Error as e:
        print( 'Error getting product info')


def get_users(user_email, user_password):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password, port=port)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tblCustomer WHERE email = %s AND password = %s', (user_email, user_password))
        account = cursor.fetchone()
        return account

    except Error as e:
        print("Error while connecting to MySQL.", e)

    finally:
        try:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        except Error as e:
            print("No connection exists to the MySQL server.", e)


def registeruser(firstname, lastname, email, telephone, password, address1, address2, city, postcode, country):
    try:
        message = ""
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password, port=port)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tblCustomers WHERE email = %s', (email))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', firstname):
            message = 'First name must contain only characters!'
        elif not re.match(r'[A-Za-z0-9]+', lastname):
            message = 'Last name must contain only characters and numbers!'
        elif not any([firstname, lastname, email, telephone, password, address1, city, postcode, country]):
            message = 'Please fill out the form!'
        else:
            # tblCustomers ( email, password, firstname, lastname, dob, userID )
            cursor.execute('INSERT INTO tblCustomers VALUES (%s, %s, %s, %s, NULL)', (email, password, firstname, lastname, userID))
            connection.commit()

            #tblAddress ( streetname, streetnumber, postcode, city, country, email, telephone )
            cursor.execute('INSERT INTO tblAddress VALUES (%s, %s, %s, %s, %s, %s, %s )', (address1, address2, postcode, city, country, email, telephone))
            connection.commit()

            message = 'You have successfully registered!'

        return message



    except



def retrieve_address():
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password, port=port)
        sql_select_Query = "select * from tblAddress"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchone()
        print("Total number Addresses: ", cursor.rowcount)
        print("\nPrinting each Address record")

        for row in records:
            print("Streetname= ", row[0], )
            print("Streetno = ", row[1])
            print("postcode  = ", row[2])
            print("city  = ", row[3])
            print("country  = ", row[4])
            print("email = ", row[5])
            print("phoneNo  = ", row[6], "\n")

        return records

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
