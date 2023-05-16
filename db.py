import mysql.connector as connector
from mysql.connector.cursor import MySQLCursor
import logging
from logging import info 
from mysql.connector import errorcode

# NOTE: use info level logging
logging.getLogger().setLevel(logging.INFO)

POKEMON_DB_NAME = "pokemondb"

class IllegalArgumentError(ValueError):
    pass

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
                 column_names: list[str],
                 data_types: list[str],
                 data_nullable: list[bool],
                 data_default: list, # can also be None
                 pri_keys: list[str], # NOTE: list of columns that are set as primary keys
                 reference: list[str | None] # None means it is not a foreign key
                 ):

    def format_columns(column_names: list[str],
                       data_types: list[str],
                       data_nullable: list[bool],
                       data_default: list):
        format_nullable = lambda x: " NOT NULL" if not x else ""
        format_default = lambda x: f" {x}" if x is not None else ""
        return ",\n".join(
            [f"{name} {type}{format_nullable(isNull)}{format_default(default_value)}"
             for name, type, isNull, default_value in
             zip(column_names, data_types, data_nullable, data_default)]) + ","

    if not (len(column_names) == len(data_types) == len(data_nullable) == len(data_default) == len(reference)):
        raise IllegalArgumentError("List type arguments length Error!")

    formated_foreign_keys = ",\n".join(
        [f"FOREIGN KEY ({name}) REFERENCES {target}" for name, target
         in zip(column_names, reference) if target is not None ]) + ","

    formated_primary_keys = "PRIMARY KEY ({})".format(",".join(pri_keys))

    command = f"""CREATE TABLE {table_name}(
{format_columns(column_names, data_types, data_nullable, data_default)}
{formated_foreign_keys}
{formated_primary_keys}
);"""
    cursor.execute(command);

def create_base_tables():
    pass

if __name__ == "__main__":
    # create db
    cursor = create_db()

    # create table
    res = create_table(
        cursor, "tableName",
        ["id", "name"],
        ["INT", "CHAR(60)"],
        [False, True],
        [None, None],
        ["id", "name"],
        ["pokemon(id)", None],
    )
    print(res)

