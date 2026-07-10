from src.Db_connector import Db_connector

#connect to database
Db_connector()
connection = Db_connector.instance

#load ddl file
with open('database/ddl.sql') as ddl_file:
    ddl = ddl_file.read()

#migrate
connection.cursor().execute(ddl)

#!WARNING if you run migrate you lose all your data