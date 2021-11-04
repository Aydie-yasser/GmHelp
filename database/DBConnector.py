# import MySQLdb
# import MySQLdb.cursors
import pymysql
pymysql.install_as_MySQLdb()
import mysql.connector
from flask import current_app as app

from app import ResponseHandler as Helper


class DBConnector:
    """
    Database Connector Class
    """

    def db_connection_factory(self, connection_type: str, query_type: str):
        """
        Create database connection based on query type and connection type
        - connection_type string database cluster type (old/legacy or new)
        - query type string query string type (read, write, update, delete, ..etc)
        """
        # handle db connection credentials
        if connection_type == 'old':
            # connect to old database
            hostname = app.config['OLD_DB_HOSTNAME']
            username = app.config['OLD_DB_USERNAME']
            password = app.config['OLD_DB_PASSWORD']
            db_name = app.config['OLD_DB_NAME']
        else:
            # connect to new cluster
            if query_type == 'write':
                # connect to master cluster
                hostname = app.config['MASTER_DB_HOSTNAME']
                username = app.config['MASTER_DB_USERNAME']
                password = app.config['MASTER_DB_PASSWORD']
                db_name = app.config['MASTER_DB_NAME']
            else:
                # connect to slave cluster
                hostname = app.config['SLAVE_DB_HOSTNAME']
                username = app.config['SLAVE_DB_USERNAME']
                password = app.config['SLAVE_DB_PASSWORD']
                db_name = app.config['SLAVE_DB_NAME']

        # connect to db
        return self.__connect_to_db(hostname, username, password, db_name)

    def __connect_to_db(self, hostname: str, username: str, password: str, db_name: str, db_port: int = 3306):
        """
        Connect to database cluster
        - return db cursor
        """
        hostname = app.config['OLD_DB_HOSTNAME']
        username = app.config['OLD_DB_USERNAME']
        password = app.config['OLD_DB_PASSWORD']
        db_name = app.config['OLD_DB_NAME']
        # Connect to DB
        try:
            mysql_connection = pymysql.connect(
                host=hostname,
                user=username,
                passwd=password,
                db=db_name,
                port=db_port,
                cursorclass=pymysql.cursors.DictCursor,
                charset='utf8'

            )
            mysql_cursor = mysql_connection.cursor()
        except:
            Helper.handle_error_response("Error in connecting to database. Try again later")
        else:
            return mysql_connection, mysql_cursor

    def connect_database(self):
        # Connect to DB
        hostname = app.config['OLD_DB_HOSTNAME']
        username = app.config['OLD_DB_USERNAME']
        password = app.config['OLD_DB_PASSWORD']
        db_name = app.config['OLD_DB_NAME']

        database_connector = mysql.connector.connect(host=hostname, user=username, password=password, database=db_name)
        return database_connector

