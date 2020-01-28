import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(host='localhost',
                                     database='webApp_DB',
                                     user='root',
                                     password='Av136.356hP0x')

cursor = connection.cursor()
cursor.execute("SELECT * FROM tblGuestCart")
databases = cursor.fetchall()

for database in databases:
    print(database)
