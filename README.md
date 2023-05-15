# Pokemon DB

*Notice*: secrets included in the code!!!.

Convert data from Pokemon-api into MySQL.

## Database Design

**db_name**: `pokemondb`   

### Base Tables

#### Pokemon

##### pokemon

| COLUMN_NAME     | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-----------------|-----------|-------------|----------------|------------|----------------------|-------|
| id              | SMALLINT  | no          |                | primary    |                      |       |
| name            | CHAR(60)  | no          |                |            |                      |       |
| order           | SMALLINT  | no          |                |            |                      |       |
| base_experience | SMALLINT  | no          |                |            |                      |       |
| height          | SMALLINT  | no          |                |            |                      |       |
| weight          | SMALLINT  | no          |                |            |                      |       |
| type_id         | SMALLINT  | no          |                |            | type                 |       |

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
| effort      | SMALLINT  | no          |                |            |                      |       |

#### Move

##### move

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    |                      | AUTO_INCREMENT |
| name        | CHAR(60)  | no          |                |            |                      |                |
| power       | SMALLINT  | no          |                |            |                      |                |
| accuracy    | SMALLINT  | no          |                |            |                      |                |
| pp          | SMALLINT  | no          |                |            |                      |                |
| priority    | SMALLINT  | no          |                |            |                      |                |
| generation  | CHAR(60)  | no          |                |            |                      |                |
| category    | CHAR(60)  | no          |                |            |                      |                |
| type_id     | SHORTINT  | no          |                |            | type                 |                |

##### move_damage_class

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | move                 |       |
| class_name  | CHAR(60)  | no          |                |            | move_damage_class    |       |

##### move_effects

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | move                 |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| effect        | TEXT      | no          |                |            |                      |       |
| short_effect  | TINYTEXT  | yes         |                |            |                      |       |

##### move_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | move                 |       |
| language_code | CHAR(60)  |             |                |            |                      |       |
| name          | CHAR(60)  | no          |                |            |                      |       |

#### Move Damage Class

##### move_damage_class
	
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| class_name  | CHAR(60)  | no          |                | primary    |                      |       |
| description | TEXT      | no          |                |            |                      |       |

##### move_damage_class_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| class_name    | CHAR(60)  | no          |                | multiple   | move_damage_class    |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| name          | CHAR(60)  | no          |                |            |                      |       |

##### move_damage_class_descriptions

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| class_name    | CHAR(60)  | no          |                | multiple   | move_damage_class    |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| description   | TEXT      | no          |                |            |                      |       |

#### Ability

##### ability

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    |                      | AUTO_INCREMENT |
| name        | CHAR(60)  | no          |                |            |                      |                |
| generation  | CHAR(60)  | no          |                |            |                      |       |

##### ability_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | ability              |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| name          | CHAR(60)  | no          |                |            |                      |       |

##### ability_effects

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | ability              |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| effect        | TEXT      | no          |                |            |                      |       |
| short_effect  | TINYTEXT  | yes         |                |            |                      |       |

##### ability_flavor_text

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | ability              |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| text          | TEXT      | no          |                |            |                      |       |
| version_group | CHAR(60)  | no          |                |            |                      |       |

#### Type

##### type
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    |                      | AUTO_INCREMENT |
| name        | CHAR(60)  | no          |                |            |                      |                |
| generation  | CHAR(60)  | no          |                |            |                      |                |

##### type_relation
**NOTE**: 'normal' damage is omitted by default when getting data from `pokeapi`
| COLUMN_NAME | DATA_TYPE                              | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|----------------------------------------|-------------|----------------|------------|----------------------|-------|
| from_id     | SMALLINT                               | no          |                | primary    | type                 |       |
| to_id       | SMALLINT                               | no          |                | primary    | type                 |       |
| damage      | ENUM('no', 'half', 'normal', 'double') | no          |                |            |                      |       |

##### type_move_damage_class

| COLUMN_NAME       | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------------|-----------|-------------|----------------|------------|----------------------|-------|
| id                | SMALLINT  | no          |                | primary    | type                 |       |
| class_name        | CHAR(60)  | no          |                |            | move_damage_class    |       |

##### type_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | type                 |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| name          | CHAR(60)  | no          |                |            |                      |       |

#### Item

##### item

| COLUMN_NAME    | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|----------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id             | SMALLINT  | no          |                | primary    |                      | AUTO_INCREMENT |
| name           | CHAR(60)  | no          |                |            |                      |                |
| cost           | INT       | no          |                |            |                      |                |
| category       | CHAR(60)  | no          |                |            |                      |                |
| default_sprite | CHAR(255) | yes         |                |            |                      |                |

##### item_fling

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | primary    | item                 |       |
| fling_power | SMALLINT  | no          |                |            |                      |       |

##### item_effects

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | type                 |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| effect        | TEXT      | no          |                |            |                      |       |
| short_effect  | TINYTEXT  | yes         |                |            |                      |       |

##### item_flavor_text

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | type                 |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| version_group | CHAR(60)  | no          |                |            |                      |       |
| text          | TEXT      | no          |                |            |                      |       |

##### item_game_indices

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|-------------|-----------|-------------|----------------|------------|----------------------|-------|
| id          | SMALLINT  | no          |                | multiple   | item                 |       |
| game_id     | SMALLINT  | no          |                |            | game                 |       |

##### item_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra |
|---------------|-----------|-------------|----------------|------------|----------------------|-------|
| id            | SMALLINT  | no          |                | multiple   | item                 |       |
| language_code | CHAR(60)  | no          |                |            |                      |       |
| name          | CHAR(60)  | no          |                |            |                      |       |
	
#### Location

#### Game

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | foreign_key_to_table | extra          |
|-------------|-----------|-------------|----------------|------------|----------------------|----------------|
| id          | SMALLINT  | no          |                | primary    | type                 | AUTO_INCREMENT |
| name        | CHAR(60)  | no          |                |            |                      |                |

### Advanced Table
The query result.

#### Item -> Pokemon Owners


## Related Resources

1. https://github.com/PokeAPI/pokeapi
2. https://github.com/beastmatser/aiopokeapi
