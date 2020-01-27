import os
import mysql.connector
from mysql.connector import Error

username = os.environ['USERNAME']
password = os.environ['PASSWORD']
database = os.environ['DATABASE']
host = os.environ['HOST']


def retrieve_user():
    try:
        connection = mysql.connector.connect(host=host, database=database, user=username, password=password)

        sql_select_Query = "select * from tblCustomer"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchone()
        print("Total number customers: ", cursor.rowcount)
        print("\nPrinting each customer record")

        # for row in records:
        #     print("Streetname= ", row[0], )
        #     print("Streetno = ", row[1])
        #     print("postcode  = ", row[2])
        #     print("city  = ", row[3])
        #     print("country  = ", row[4])
        #     print("email = ", row[5])
        #     print("phoneNo  = ", row[6], "\n")

        return records

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def retrieve_address():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='webApp_DB',
                                             user='root',
                                             password='Av136.356hP0x')

        sql_select_Query = "select * from tblAddress"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchone()
        print("Total number Addresses: ", cursor.rowcount)
        print("\nPrinting each Address record")

        for row in records:
            print("Streetname= ", row[0],)
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













# print("\nPrinting each Address record")
#     for row in records:
#         print("Streetname= ", row[0],)
#         print("Streetno = ", row[1])
#         print("postcode  = ", row[2])
#         print("city  = ", row[3])
#         print("country  = ", row[4])
#         print("email = ", row[5])
#         print("phoneNo  = ", row[6], "\n")