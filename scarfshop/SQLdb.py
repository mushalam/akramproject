import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='webApp_DB',
                                         user='root',
                                         password='Av136.356hP0x')

    sql_select_Query = "SELECT `tblProduct`.`productID`, `tblProduct`.`productName`, `tblProduct`.`quantity`, `tblCustomer`.`email`, `tblTransactions`.`totalPrice`
FROM `tblCustomer`
    LEFT JOIN `tblTransactions` ON `tblTransactions`.`email` = `tblCustomer`.`email`
    LEFT JOIN `tblProduct` ON `tblTransactions`.`productID` = `tblProduct`.`productID`"

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number Addresses: ", cursor.rowcount)

    print("\nPrinting each Address record")
    for row in records:
        print("pID= ", row[0],)
        print("pName = ", row[1])
        print("quan  = ", row[2])
        print("email  = ", row[3])
        print("tPrice  = ", row[4], "\n")


except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

#query for returning all records in address tbl with all fields
# print("\nPrinting each Address record")
#     for row in records:
#         print("Streetname= ", row[0],)
#         print("Streetno = ", row[1])
#         print("postcode  = ", row[2])
#         print("city  = ", row[3])
#         print("country  = ", row[4])
#         print("email = ", row[5])
#         print("phoneNo  = ", row[6], "\n")