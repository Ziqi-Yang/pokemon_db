import mysql.connector as connector
from mysql.connector.cursor import MySQLCursor
import logging
from logging import info 
from mysql.connector import errorcode

# NOTE: use info level logging
logging.getLogger().setLevel(logging.INFO)

POKEMON_DB_NAME = "pokemondb"

def create_db() -> MySQLCursor:
    """Create db and return cursor to that db"""
    cn = connector.connect(
        user='root',
        password='root',
        host='127.0.0.1'
    )

    cursor = cn.cursor()

    # create database
    try:
        cursor.execute(f"CREATE DATABASE {POKEMON_DB_NAME};")
    except connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            info(f"Database {POKEMON_DB_NAME} already exists.")
        else:
            print(err)
            exit(1)

    # use database
    cursor.execute(f"USE {POKEMON_DB_NAME};")
    info(f"use database {POKEMON_DB_NAME}")

    return cursor

def create_table(cursor: MySQLCursor, table_name: str,
                 column_names: tuple[str],
                 data_types: tuple[str],
                 ):
    # TODO 
    if len(column_names) != len(data_types):
        raise Exception("")
    cursor.execute(f"""CREATE TABLE {table_name}(

)""")
