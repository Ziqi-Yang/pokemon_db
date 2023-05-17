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

class Conn:
    def __init__(self):
        self.conn = connector.connect(
            user='root',
            password='root',
            host='127.0.0.1'
        )
        self.cursor = self.conn.cursor()

def create_db(cn: Conn):
    """Create db and return cursor to that db"""
    cursor = cn.cursor

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

def create_table(cursor: MySQLCursor, table_name: str,
                 column_names: list[str],
                 data_types: list[str],
                 data_nullable: list[bool] | bool, 
                 data_default: list | None, 
                 pri_keys: list[str], # NOTE: list of columns that are set as primary keys
                 reference: dict[str, str] | None
                 ):

    def format_columns(column_names: list[str],
                       data_types: list[str],
                       data_nullable: list[bool] | bool,
                       data_default: list | None):
        if isinstance(data_nullable, bool):
            data_nullable = [data_nullable] * len(column_names)
        if data_default is None:
            data_default = [None] * len(column_names)

        format_nullable = lambda x: " NOT NULL" if not x else ""
        format_default = lambda x: f" {x}" if x is not None else ""

        format_default = lambda x: f" {x}" if x is not None else ""
        return ",\n".join(
            [f"{name} {type}{format_nullable(isNull)}{format_default(default_value)}"
             for name, type, isNull, default_value in
             zip(column_names, data_types, data_nullable, data_default)]) + ","

    column_len = len(column_names)
    if (column_len != len(data_types)) or (not isinstance(data_nullable, bool) and column_len != len(data_nullable)) or (data_default is not None and column_len != len(data_default)):
        raise IllegalArgumentError("List type arguments length Error!")

    formated_foreign_keys = ""
    if reference is not None:
        formated_foreign_keys = ",\n".join([f"FOREIGN KEY ({name}) REFERENCES {target}"
                                            for name, target in reference.items() ])
        formated_foreign_keys += ",\n" if formated_foreign_keys != "" else ""

    formated_primary_keys = "PRIMARY KEY ({})".format(",".join(pri_keys))

    command = f"""CREATE TABLE {table_name}(
{format_columns(column_names, data_types, data_nullable, data_default)}
{formated_foreign_keys}{formated_primary_keys}
);"""
    cursor.execute(command)

def create_basic_tables(cn: Conn):
    """Create a couple of tables that will be refered in the other tables."""
    cursor = cn.cursor

    create_table(
        cursor, "pokemon",
        ["id", "name", "the_order", "height", "weight", "base_experience", "sprite_front_default", 
         "sprite_front_female", "sprite_front_shiny", "sprite_front_shiny_female", "sprite_back_default", 
         "sprite_back_female", "sprite_back_shiny", "sprite_back_shiny_female"],
        ["SMALLINT", "CHAR(60)", "SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT", "CHAR(255)",
         "CHAR(255)", "CHAR(255)", "CHAR(255)", "CHAR(255)", "CHAR(255)", "CHAR(255)", "CHAR(255)"],
        [False, False, False, False, False, False, True, True, True, True, True, True, True, True],
        None, ["id"], None)
    info("[*] create table 'pokemon'")

    # stat
    create_table(
        cursor, "stat",
        ["id", "name", "is_battle_only"],
        ["SMALLINT", "CHAR(60)", "BOOLEAN"],
        False, None, ["id"], None)
    info("[*] create table 'stat'")

    # species
    create_table(
        cursor, "species",
        ["id", "name", "the_order", "gender_rate", "capture_rate", "base_happiness", "is_baby", 
         "is_legendary", "is_mythical", "hatch_counter", "has_gender_differences", "forms_switchable", 
         "growth_rate", "generation"],
        ["SMALLINT", "CHAR(60)", "SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT", "BOOLEAN", "BOOLEAN",
         "BOOLEAN", "MEDIUMINT", "BOOLEAN", "BOOLEAN", "ENUM('slow', 'medium', 'fast', 'medium-slow', 'slow-then-very-fast', 'fast-then-very-slow')", "CHAR(60)"],
        False, None, ["id"], None)
    info("[*] create table 'species'")

    # egg_group
    create_table(
        cursor, "egg_group",
        ["id", "name"],
        ["SMALLINT", "CHAR(60)"],
        False, None, ["id"], None)
    info("[*] create table 'egg_group'")

    # move_damage_class 
    create_table(
        cursor, "move_damage_class",
        ["id", "class_name", "description"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], None)
    info("[*] create table 'move_damage_class'")
    
    # ability
    create_table(
        cursor, "ability",
        ["id", "name", "generation"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)"],
        False, None, ["id"], None)
    info("[*] create table 'ability'")

    # type NOTE: after creating move_damage_class
    create_table(
        cursor, "type",
        ["id", "name", "generation", "move_damage_class_id"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], {"move_damage_class_id": "move_damage_class(id)"})
    info("[*] create table 'type'")

    # move NOTE: after creating type
    create_table(
        cursor, "move",
        ["id", "name", "power", "accuracy", "pp", "priority", "generation", "category", "type_id"],
        ["SMALLINT", "CHAR(60)", "SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT", "CHAR(60)", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], {"type_id": "type(id)"})
    info("[*] create table 'move'")

    # item
    create_table(
        cursor, "item",
        ["id", "name", "cost", "category", "default_sprite", "fling_power"],
        ["SMALLINT", "CHAR(60)", "INT", "CHAR(60)", "CHAR(255)", "SMALLINT"],
        [False, False, False, False, True, False],
        None,  ["id"], None)
    info("[*] create table 'item'")

    # table 'region'
    create_table(
        cursor, "region",
        ["id", "name"],  
        ["SMALLINT", "CHAR(60)"],
        False, None, ["id"], None)
    info("[*] create table 'region'")

    # location
    create_table(
        cursor, "location",
        ["id", "name", "region_id"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], {"region_id": "region(id)"})
    info("[*] create table 'location'")

    # area
    create_table(
        cursor, "area",
        ["id", "name", "location_id"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], {"location_id": "location(id)"})
    info("[*] create table 'area'")

    # game_group
    create_table(
        cursor, "game_group",
        ["id", "name", "generation"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)"],
        False, None, ["id"], None)
    info("[*] create table 'game_group'")

    # game
    create_table(
        cursor, "game",
        ["id", "name", "game_group_id"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], None)
    info("[*] create table 'game'")

    # encounter NOTE: after creating pokemon, area and game tables
    create_table(
        cursor, "encounter",
        ["id", "area_id", "pokemon_id", "game_id", "max_chance"],
        ["SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT", "TINYINT"],
        False, None,
        ["id", "area_id", "pokemon_id", "game_id"],
        {"area_id": "area(id)", "pokemon_id": "pokemon(id)", "game_id": "game(id)"})
    info("[*] create table 'encounter'")

    # encounter_method
    create_table(
        cursor, "encounter_method",
        ["id", "name", "the_order"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], None)
    info("[*] create table 'encounter_method'")

    # encounter_condition
    create_table(
        cursor, "encounter_condition",
        ["id", "name"],
        ["SMALLINT", "CHAR(60)"],
        False, None, ["id"], None)
    info("[*] create table 'encounter_condition'")


if __name__ == "__main__":
    # create db
    cn = Conn()
    cn.cursor.execute(f"DROP DATABASE {POKEMON_DB_NAME}") # FIXME dangerous
    create_db(cn)
    create_basic_tables(cn)

