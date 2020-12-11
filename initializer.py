import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=""
)
db_cursor = db_connection.cursor()
db_cursor.execute("CREATE DATABASE restaurant_customer")
