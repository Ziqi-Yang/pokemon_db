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
                 foreign_key_target_names: list[str | None], # None means it is not a foreign key
                 key_names: list[str], # custom length
                 key_types: list[str], # PRI, MUL
                 extra: list[str | None]):

    def format_columns(column_names: list[str],
                       data_types: list[str],
                       data_nullable: list[bool],
                       data_default: list,
                       extra: list[str | None]):
        format_nullable = lambda x: " NOT NULL" if not x else ""
        format_default = lambda x: f" {x}" if x is not None else ""
        format_extra_info = lambda x: f" {x}" if x is not None else ""
        return ",\n".join(
            [f"{name} {type}{format_nullable(isNull)}{format_default(default_value)}{format_extra_info(e)}"
             for name, type, isNull, default_value, e in
             zip(column_names, data_types, data_nullable, data_default, extra)]) + ","

    def format_keys(key_names: list[str], key_types: list[str]):
        pri_keys = []
        mul_keys = []
        for index, key in enumerate(key_names):
            match key_types[index]:
                case "pri" | "PRI":
                    pri_keys.append(key)
                case "mul" | "MUL":
                    mul_keys.append(key)
                case _:
                    raise IllegalArgumentError("Unknown type in parameter 'key_types'")
        res = ""
        if len(pri_keys) != 0:
            res += "PRIMARY KEY({})".format(",".join(pri_keys))
        if len(mul_keys) != 0:
            if len(res) != 0:
                res += ",\n"
                res += "KEY({})".format(",".join(mul_keys))
        return res

    if not (len(column_names) == len(data_types) == len(data_nullable) == len(data_default) == len(foreign_key_target_names)
            == len(extra)):
        raise IllegalArgumentError("List type arguments length Error!")

    if len(key_names) != len(key_types):
        raise IllegalArgumentError("List type arguments length Error!")

    formated_foreign_keys = ",\n".join(
        [f"FOREIGN KEY ({name}) REFERENCES {target}" for name, target
         in zip(column_names, foreign_key_target_names) if target is not None ]) + ","

    return f"""CREATE TABLE {table_name}(
{format_columns(column_names, data_types, data_nullable, data_default, extra)}
{formated_foreign_keys}
{format_keys(key_names, key_types)}
);"""
#     # TODO 
#     cursor.execute(f"""CREATE TABLE {table_name}(
#     {format_columns(column_names, data_types)}
# )""")

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
        ["pokemon", None],
        ["id", "name"],
        ["PRI", "mul"],
        ["AUTO_INCREMENT", None]
    )
    print(res)

