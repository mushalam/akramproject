import os
import mysql.connector
from mysql.connector import Error
from flask import redirect

db_username = os.environ['USERNAME_2']
db_password = os.environ['PASSWORD']
database = os.environ['DATABASE']
host = os.environ['HOST']
port = '37306'


def delete_cart_entry(productID):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        delquery='DELETE FROM tblGuestCart WHERE productID = '+str(productID)
        cursor.execute(delquery)
        connection.commit()
    except Error as e:
        print( 'Error deleting cart item')

def add_product_to_cart(product):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        query='INSERT INTO tblGuestCart VALUES '+str(product)
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print( 'Error deleting cart item')


def update_cart(productID,quantity):
    prod_details = get_product_by_id(productID)
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        query='UPDATE tblGuestCart SET quan = '+str(quantity)+' WHERE productID = '+str(productID)
        cursor.execute(query)

        price=float(prod_details[2])
        total=round(price*quantity,2)
        query2='UPDATE tblGuestCart SET total = '+str(total)+' WHERE productID = '+str(productID)
        cursor.execute(query2)
        cursor.execute('SELECT * FROM tblGuestCart')

        c=cursor.fetchall()

        connection.commit()

        print(str(c))
    except Error as e:
        print( 'Error updating cart')


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

def get_all_products():
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tblProduct')
        product_list = cursor.fetchall()
        return product_list
    except Error as e:
        print( 'Error getting product list')

def get_users(user_email, user_password):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password, port=port)
        cursor = connection.cursor()
        # cursor = connection.cursor(MySQLdb.cursors.DictCursor)
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


#