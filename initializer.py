import mysql.connector

db_connection = mysql.connector.connect(
    host="mysql",
    user="root",
    passwd="123456"
)
db_cursor = db_connection.cursor()
db_cursor.execute("CREATE DATABASE restaurant_customer")
