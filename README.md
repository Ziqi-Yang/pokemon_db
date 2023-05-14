# Pokemon DB

*Notice*: secrets included in the code!!!.

Convert data from Pokemon-api into MySQL.

## Database Design

**db_name**: `pokemondb`   
**categories**: `pokemon`, `moves`, `ability`, `type`, `item`, `location`, `game`  

### Base Tables

#### Pokemon

##### pokemon
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    |                      |       |
| name        | CHAR(60)  | no          |                |            |                      |       |

##### pokemon_base_information

| COLUMN_NAME     | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-----------------|-----------|-------------|----------------|------------|----------------------|-------|
| id              | SMALLINT  | no          |                | multiple   | pokemon              |       |
| base_experience | SMALLINT  | no          |                |            |                      |       |
| height          | SMALLINT  | no          |                |            |                      |       |
| weight          | SMALLINT  | no          |                |            |                      |       |
| order           | SMALLINT  | no          |                |            |                      |       |

##### pokemon_abilities
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| ability_id  | SMALLINT  | no          |                |            | ability              |       |
| is_hidden   | BOOLEAN   | no          |                |            |                      |       |

##### pokemon_forms
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| name        | CHAR(60)  | no          |                |            |                      |       |
| is_hidden   | BOOLEAN   | no          |                |            |                      |       |

##### pokemon_game_indices
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| game_id     | SMALLINT  | no          |                |            | game                 |       |

##### pokemon_held_items

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| item_id     | SMALLINT  | no          |                |            | item                 |       |

##### pokemon_location_area_encounters
TODO 
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| location_id | SMALLINT  | no          |                |            | location             |       |

##### pokemon_moves

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| move_id     | SMALLINT  | no          |                |            | move                 |       |


##### pokemon_species

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | pokemon              |       |
| species_id  | SMALLINT  | no          |                |            | species              |       |

##### pokemon_sprite

| COLUMN_NAME                    | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|--------------------------------|-----------|-------------|----------------|------------|----------------------|-------|
| id                             | SMALLINT  | no          |                | multiple   | pokemon              |       |
| front_default                  | CHAR(255) | yes         |                |            |                      |       |
| front_female                   | CHAR(255) | yes         |                |            |                      |       |
| front_shiny                    | CHAR(255) | yes         |                |            |                      |       |
| front_shiny_female             | CHAR(255) | yes         |                |            |                      |       |
| back_default                   | CHAR(255) | yes         |                |            |                      |       |
| back_female                    | CHAR(255) | yes         |                |            |                      |       |
| back_shiny                     | CHAR(255) | yes         |                |            |                      |       |
| back_shiny_female              | CHAR(255) | yes         |                |            |                      |       |

##### pokemon_stats

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| stat_name   | CHAR(60)  | no          |                |            |                      |       |
| base_start  | SMALLINT  | no          |                |            |                      |       |
| effort      | SMALLINT  | no            |                |            |                      |       |

##### pokemon_type
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | pokemon              |       |
| type_id     | SMALLINT  | no          |                |            | type                 |       |



#### Move

1. **Move**



#### Ability

1. **ability**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    |                      | AUTO_INCREMENT |
| name        | CHAR(60)  | no          |                |            |                      |                |

2. **ability_generation**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | ability              |       |
| generation  | CHAR(60)  | no          |                |            |                      |       |

#### Type

1. **type**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    |                      | AUTO_INCREMENT |
| name        | CHAR(60)  | no          |                |            |                      |                |

2. **type_relation**
**NOTE**: 'normal' damage is omitted by default when getting data from `pokeapi`
| COLUMN_NAME | DATA_TYPE                              | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|----------------------------------------|-------------|----------------|------------|----------------------|-------|
| from_id     | SMALLINT                               | no          |                | primary    | type                 |       |
| to_id       | SMALLINT                               | no          |                | primary    | type                 |       |
| damage      | ENUM('no', 'half', 'normal', 'double') | no          |                |            |                      |       |

3. **type_generation**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | type                 |       |
| generation  | CHAR(60)  | no          |                |            |                      |       |

4. **type_move_damage_class**
TODO 
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | type                 |       |
|             | CHAR(60)  | no          |                |            |                      |       |

#### Item

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    | type                 | AUTO_INCREMENT |
| name        | CHAR(60)  | no          |                |            |                      |                |
	
#### Location

#### Game

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    | type                 | AUTO_INCREMENT |
| name        | CHAR(60)  | no          |                |            |                      |                |


### Advanced Table
The query result.



## Related Resources

1. https://github.com/PokeAPI/pokeapi
2. https://github.com/beastmatser/aiopokeapi
