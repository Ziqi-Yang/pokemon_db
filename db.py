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

    # pokemon
    info("[*] creating table 'pokemon'...")
    create_table(
        cursor, "pokemon",
        ["id", "name", "the_order", "height", "weight", "base_experience", "sprite_front_default", 
         "sprite_front_female", "sprite_front_shiny", "sprite_front_shiny_female", "sprite_back_default", 
         "sprite_back_female", "sprite_back_shiny", "sprite_back_shiny_female"],
        ["SMALLINT", "CHAR(60)", "SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT", "CHAR(255)",
         "CHAR(255)", "CHAR(255)", "CHAR(255)", "CHAR(255)", "CHAR(255)", "CHAR(255)", "CHAR(255)"],
        [False, False, False, False, False, False, True, True, True, True, True, True, True, True],
        None, ["id"], None)

    # stat
    info("[*] creating table 'stat'...")
    create_table(
        cursor, "stat",
        ["id", "name", "is_battle_only"],
        ["SMALLINT", "CHAR(60)", "BOOLEAN"],
        False, None, ["id"], None)

    # species
    info("[*] creating table 'species'...")
    create_table(
        cursor, "species",
        ["id", "name", "the_order", "gender_rate", "capture_rate", "base_happiness", "is_baby", 
         "is_legendary", "is_mythical", "hatch_counter", "has_gender_differences", "forms_switchable", 
         "growth_rate", "generation"],
        ["SMALLINT", "CHAR(60)", "SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT", "BOOLEAN", "BOOLEAN",
         "BOOLEAN", "MEDIUMINT", "BOOLEAN", "BOOLEAN", "ENUM('slow', 'medium', 'fast', 'medium-slow', 'slow-then-very-fast', 'fast-then-very-slow')", "CHAR(60)"],
        False, None, ["id"], None)

    # egg_group
    info("[*] creating table 'egg_group'...")
    create_table(
        cursor, "egg_group",
        ["id", "name"],
        ["SMALLINT", "CHAR(60)"],
        False, None, ["id"], None)

    # move_damage_class 
    info("[*] creating table 'move_damage_class'...")
    create_table(
        cursor, "move_damage_class",
        ["id", "class_name", "description"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], None)
    
    # ability
    info("[*] creating table 'ability'...")
    create_table(
        cursor, "ability",
        ["id", "name", "generation"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)"],
        False, None, ["id"], None)

    # type NOTE: after creating move_damage_class
    info("[*] creating table 'type'...")
    create_table(
        cursor, "type",
        ["id", "name", "generation", "move_damage_class_id"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], {"move_damage_class_id": "move_damage_class(id)"})

    # move NOTE: after creating type
    info("[*] creating table 'move'...")
    create_table(
        cursor, "move",
        ["id", "name", "power", "accuracy", "pp", "priority", "generation", "category", "type_id"],
        ["SMALLINT", "CHAR(60)", "SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT", "CHAR(60)", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], {"type_id": "type(id)"})

    # item
    info("[*] creating table 'item'...")
    create_table(
        cursor, "item",
        ["id", "name", "cost", "category", "default_sprite", "fling_power"],
        ["SMALLINT", "CHAR(60)", "INT", "CHAR(60)", "CHAR(255)", "SMALLINT"],
        [False, False, False, False, True, False],
        None,  ["id"], None)

    # table 'region'
    info("[*] creating table 'region'...")
    create_table(
        cursor, "region",
        ["id", "name"],  
        ["SMALLINT", "CHAR(60)"],
        False, None, ["id"], None)

    # location
    info("[*] creating table 'location'...")
    create_table(
        cursor, "location",
        ["id", "name", "region_id"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], {"region_id": "region(id)"})

    # area
    info("[*] creating table 'area'...")
    create_table(
        cursor, "area",
        ["id", "name", "location_id"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], {"location_id": "location(id)"})

    # game_group
    info("[*] creating table 'game_group'...")
    create_table(
        cursor, "game_group",
        ["id", "name", "generation"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)"],
        False, None, ["id"], None)

    # game
    info("[*] creating table 'game'...")
    create_table(
        cursor, "game",
        ["id", "name", "game_group_id"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], None)

    # encounter NOTE: after creating pokemon, area and game tables
    info("[*] creating table 'encounter'...")
    create_table(
        cursor, "encounter",
        ["id", "area_id", "pokemon_id", "game_id", "max_chance"],
        ["SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT", "TINYINT"],
        False, None,
        ["id", "area_id", "pokemon_id", "game_id"],
        {"area_id": "area(id)", "pokemon_id": "pokemon(id)", "game_id": "game(id)"})

    # encounter_method
    info("[*] creating table 'encounter_method'...")
    create_table(
        cursor, "encounter_method",
        ["id", "name", "the_order"],
        ["SMALLINT", "CHAR(60)", "SMALLINT"],
        False, None, ["id"], None)

    # encounter_condition
    info("[*] creating table 'encounter_condition'...")
    create_table(
        cursor, "encounter_condition",
        ["id", "name"],
        ["SMALLINT", "CHAR(60)"],
        False, None, ["id"], None)

def create_other_tables(cn: Conn):
    create_other_tables_pokemon(cn)
    create_other_tables_stat(cn)
    create_other_tables_species(cn)
    create_other_tables_egg_group(cn)
    create_other_tables_move(cn)
    create_other_tables_move_damage_class(cn)
    create_other_tables_ability(cn)
    create_other_tables_type(cn)
    create_other_tables_item(cn)
    create_other_tables_location(cn)
    create_other_tables_encounter(cn)
    create_other_tables_game(cn)


def create_other_tables_pokemon(cn: Conn):
    """Create other tables."""
    cursor = cn.cursor

    # pokemon_types
    info("[*] creating table 'pokemon_types'...")
    create_table(
        cursor, "pokemon_types",
        ["pokemon_id", "type_id"],
        ["SMALLINT", "SMALLINT"],
        False, None, ["pokemon_id", "type_id"], {"pokemon_id": "pokemon(id)", "type_id": "type(id)"})

    # pokemon_abilities
    info("[*] creating table 'pokemon_abilities'...")
    create_table(
        cursor, "pokemon_abilities",
        ["pokemon_id", "ability_id", "is_hidden"],
        ["SMALLINT", "SMALLINT", "BOOLEAN"],
        False, None, ["pokemon_id", "ability_id"], {"pokemon_id": "pokemon(id)", "ability_id": "ability(id)"})

    # pokemon_forms
    info("[*] creating table 'pokemon_forms'...")
    create_table(
        cursor, "pokemon_forms",
        ["pokemon_id", "name"],
        ["SMALLINT", "CHAR(60)"],
        False, None, ["pokemon_id", "name"], None)
    
    # pokemon_game_indices
    info("[*] creating table 'pokemon_game_indices'...")
    create_table(
        cursor, "pokemon_game_indices",
        ["pokemon_id", "game_id"],
        ["SMALLINT", "SMALLINT"],
        False, None, ["pokemon_id", "game_id"], {"pokemon_id": "pokemon(id)", "game_id": "game(id)"})
    
    # pokemon_held_items
    info("[*] creating table 'pokemon_held_items'...")
    create_table(
        cursor, "pokemon_held_items",
        ["pokemon_id", "item_id"],
        ["SMALLINT", "SMALLINT"],
        False, None, ["pokemon_id", "item_id"], {"pokemon_id": "pokemon(id)", "item_id": "item(id)"})
    
    # pokemon_moves
    info("[*] creating table 'pokemon_moves'...")
    create_table(
        cursor, "pokemon_moves",
        ["pokemon_id", "move_id", "game_group_id", "level_learned_at", "move_learn_method"],
        ["SMALLINT", "SMALLINT", "SMALLINT", "TINYINT", "CHAR(60)"],
        False, None, ["pokemon_id", "move_id", "game_group_id"],
        {"pokemon_id": "pokemon(id)", "move_id": "move(id)", "game_group_id": "game_group(id)"})
    
    # pokemon_stats
    info("[*] creating table 'pokemon_stats'...")
    create_table(
        cursor, "pokemon_stats",
        ["pokemon_id", "stat_id", "base_start", "effort"],
        ["SMALLINT", "SMALLINT", "SMALLINT", "SMALLINT"],
        False, None, ["pokemon_id", "stat_id"], {"pokemon_id": "pokemon(id)", "stat_id": "stat(id)"})

def create_other_tables_stat(cn: Conn):
    cursor = cn.cursor

    # stat_names
    info("[*] creating table 'stat_names'...")
    create_table(
        cursor, "stat_names",
        ["stat_id", "language_code", "name"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)"],
        False, None, ["stat_id", "language_code"], {"stat_id": "stat(id)"})

def create_other_tables_species(cn: Conn):
    cursor = cn.cursor

    # species_egg_group
    info("[*] creating table 'species_egg_group'...")
    create_table(
        cursor, "species_egg_group",
        ["species_id", "egg_group_id"],
        ["SMALLINT", "SMALLINT"],
        False, None, ["species_id", "egg_group_id"], {"species_id": "species(id)", "egg_group_id": "egg_group(id)"})
    
    # species_names
    info("[*] creating table 'species_names'...")
    create_table(
        cursor, "species_names",
        ["species_id", "language_code", "name"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)"],
        False, None, ["species_id", "language_code"], {"species_id": "species(id)"})
    
    # species_flavor_text
    info("[*] creating table 'species_flavor_text'...")
    create_table(
        cursor, "species_flavor_text",
        ["species_id", "language_code", "text", "game_group_id"],
        ["SMALLINT", "CHAR(60)", "TEXT", "SMALLINT"],
        False, None, ["species_id", "language_code"], {"species_id": "species(id)", "game_group_id": "game_group(id)"})
    
    # species_form_descriptions
    info("[*] creating table 'species_form_descriptions'...")
    create_table(
        cursor, "species_form_descriptions",
        ["species_id", "language_code", "description"],
        ["SMALLINT", "CHAR(60)", "TEXT"],
        False, None, ["species_id", "language_code"], {"species_id": "species(id)"})

def create_other_tables_egg_group(cn: Conn):
    cursor = cn.cursor

    # egg_group_names
    info("[*] creating table 'egg_group_names'...")
    create_table(
        cursor, "egg_group_names",
        ["egg_group_id", "language_code", "name"],
        ["SMALLINT", "CHAR(60)", "CHAR(60)"],
        False, None, ["id"], None)

def create_other_tables_move(cn: Conn):
    cursor = cn.cursor
    pass

def create_other_tables_move_damage_class(cn: Conn):
    cursor = cn.cursor
    pass

def create_other_tables_ability(cn: Conn):
    cursor = cn.cursor
    pass

def create_other_tables_type(cn: Conn):
    cursor = cn.cursor
    pass

def create_other_tables_item(cn: Conn):
    cursor = cn.cursor
    pass

def create_other_tables_location(cn: Conn):
    cursor = cn.cursor
    pass

def create_other_tables_encounter(cn: Conn):
    cursor = cn.cursor
    pass

def create_other_tables_game(cn: Conn):
    cursor = cn.cursor
    pass

if __name__ == "__main__":
    # create db
    cn = Conn()
    cn.cursor.execute(f"DROP DATABASE {POKEMON_DB_NAME}") # FIXME dangerous
    info("[-------------------- create db --------------------]")
    create_db(cn)
    info("[-------------------- create basic tables --------------------]")
    create_basic_tables(cn)
    info("[-------------------- create other tables --------------------]")
    create_other_tables(cn)
