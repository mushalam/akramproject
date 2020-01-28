import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(host='localhost',
                                     database='webApp_DB',
                                     user='root',
                                     password='Av136.356hP0x')

cursor = connection.cursor()
cursor.execute("SELECT `tblGuestCart`.`productID`, `tblGuestCart`.`quan`, `tblGuestCart`.`total`, `tblProduct`.`productName` FROM `tblProduct' LEFT JOIN `tblGuestCart` ON `tblGuestCart`.`productID` = `tblProduct`.`productID`")
databases = cursor.fetchall()

for database in databases:
    print(database)
