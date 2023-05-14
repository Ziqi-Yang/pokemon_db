# Pokemon DB

*Notice*: secrets included in the code!!!.

Convert data from Pokemon-api into MySQL.

## Database Design

**db_name**: `pokemondb`   
**categories**: `pokemon`, `moves`, `ability`, `type`, `item`, `location`  

### Base Tables

#### Pokemon

1. **pokemon**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    |                      |       |
| name        | CHAR(40)  | no          |                |            |                      |       |

2. **pokemon_ability**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| ability_id  | SMALLINT  | no          |                |            | ability              |       |
| is_hidden   | BOOLEAN   | no          |                |            |                      |       |

3. **pokemon_type**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | pokemon              |       |
| type_id     | SMALLINT  | no          |                |            | type                 |       |


3. **pokemon_forms**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | pokemon              |       |
| name        | CHAR(40)  | no          |                |            |                      |       |
| is_hidden   | BOOLEAN   | no          |                |            |                      |       |

4. **pokemon_indices**

#### Move

1. **Move**



#### Ability

1. **ability**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    |                      | AUTO_INCREMENT |
| name        | CHAR(40)  | no          |                |            |                      |                |

2. **ability_generation**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | ability              |       |
| generation  | CHAR(40)  | no          |                |            |                      |       |

#### Type

1. **type**
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    |                      | AUTO_INCREMENT |
| name        | CHAR(40)  | no          |                |            |                      |                |

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
| generation  | CHAR(40)  | no          |                |            |                      |       |

4. **type_move_damage_class**
TODO 
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | type                 |       |
|   | CHAR(40)  | no          |                |            |                      |       |


#### Location

### Advanced Table
The query result.



## Related Resources

1. https://github.com/PokeAPI/pokeapi
2. https://github.com/beastmatser/aiopokeapi
