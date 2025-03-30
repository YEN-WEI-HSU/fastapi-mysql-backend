import mysql.connector

db_config = {
    "host": "127.0.0.1",
    "user": "testuser",
    "password": "test123",
    "database": "testdb",
    "port": 3306
}

def get_connection():
    return mysql.connector.connect(**db_config)
