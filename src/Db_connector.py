import mysql.connector
from dotenv import load_dotenv
from os import getenv

#load .env file
load_dotenv()

class Db_connector:
    instance = None
    
    
    def __init__(self):
        if Db_connector.instance == None:
            Db_connector.instance = mysql.connector.connect(
                host=getenv('DB_HOST'),
                port=getenv('DB_PORT'),
                user=getenv('DB_USER'),
                database=getenv('DB_DATABASE'),
                password=getenv('DB_PASSWORD'),
                use_pure=True
            )