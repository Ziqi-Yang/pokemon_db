# Pokemon Database Base Tables

Note:
1. the names of the headers with the third level indentation are also the table names (i.e. All headers that begins with a lowercase character).
2. `the_order` is named because `order` is a keyword in MySQL, and cannot be used as an column name. Also `index` -> `game_index`


## Pokemon

### pokemon

| COLUMN_NAME               | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|---------------------------|-----------|-------------|----------------|------------|-------------|
| id                        | SMALLINT  | no          |                | primary    |             |
| name                      | CHAR(60)  | no          |                |            |             |
| the_order                 | SMALLINT  | no          |                |            |             |
| height                    | SMALLINT  | yes         |                |            |             |
| weight                    | SMALLINT  | yes         |                |            |             |
| base_experience           | SMALLINT  | yes         |                |            |             |
| sprite_front_default      | CHAR(255) | yes         |                |            |             |
| sprite_front_female       | CHAR(255) | yes         |                |            |             |
| sprite_front_shiny        | CHAR(255) | yes         |                |            |             |
| sprite_front_shiny_female | CHAR(255) | yes         |                |            |             |
| sprite_back_default       | CHAR(255) | yes         |                |            |             |
| sprite_back_female        | CHAR(255) | yes         |                |            |             |
| sprite_back_shiny         | CHAR(255) | yes         |                |            |             |
| sprite_back_shiny_female  | CHAR(255) | yes         |                |            |             |
| species_id                | CHAR(255) | no          |                |            | species(id) |

### pokemon_types

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|-------------|-----------|-------------|----------------|------------|-------------|
| pokemon_id  | SMALLINT  | no          |                | primary    | pokemon(id) |
| type_id     | SMALLINT  | no          |                | primary    | type(id)    |

### pokemon_abilities

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|-------------|-----------|-------------|----------------|------------|-------------|
| pokemon_id  | SMALLINT  | no          |                | primary    | pokemon(id) |
| ability_id  | SMALLINT  | no          |                | primary    | ability(id) |
| is_hidden   | BOOLEAN   | no          |                |            |             |

### pokemon_forms

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|-------------|-----------|-------------|----------------|------------|-------------|
| pokemon_id  | SMALLINT  | no          |                | primary    | pokemon(id) |
| name        | CHAR(60)  | no          |                | primary    |             |

### pokemon_game_indices

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|-------------|-----------|-------------|----------------|------------|-------------|
| pokemon_id  | SMALLINT  | no          |                | primary    | pokemon(id) |
| game_id     | SMALLINT  | no          |                | primary    | game(id)    |
| the_index   | SMALLINT  | no          |                |            |             |

### pokemon_held_items

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|-------------|-----------|-------------|----------------|------------|-------------|
| pokemon_id  | SMALLINT  | no          |                | primary    | pokemon(id) |
| item_id     | SMALLINT  | no          |                | primary    | item(id)    |

### pokemon_moves

| COLUMN_NAME       | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE      |
|-------------------|-----------|-------------|----------------|------------|----------------|
| pokemon_id        | SMALLINT  | no          |                | primary    | pokemon(id)    |
| move_id           | SMALLINT  | no          |                | primary    | move(id)       |
| game_group_id     | SMALLINT  | no          |                | primary    | game_group(id) |
| level_learned_at  | TINYINT   | no          |                |            |                |
| move_learn_method | CHAR(60)  | no          |                |            |                |

### pokemon_stats

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|-------------|-----------|-------------|----------------|------------|-------------|
| pokemon_id  | SMALLINT  | no          |                | primary    | pokemon(id) |
| stat_id     | SMALLINT  | no          |                | primary    | stat(id)    |
| base_start  | SMALLINT  | no          |                |            |             |
| effort      | SMALLINT  | no          |                |            |             |

## Stat

### stat

| COLUMN_NAME    | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|----------------|-----------|-------------|----------------|------------|-----------|
| id             | SMALLINT  | no          |                | primary    |           |
| name           | CHAR(60)  | no          |                |            |           |
| is_battle_only | BOOLEAN   | no          |                |            |           |

### stat_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|---------------|-----------|-------------|----------------|------------|-----------|
| stat_id       | SMALLINT  | no          |                | primary    | stat(id)  |
| language_code | CHAR(60)  | no          |                | primary    |           |
| name          | CHAR(60)  | no          |                |            |           |

## Species

### species

| COLUMN_NAME            | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|------------------------|-----------|-------------|----------------|------------|-----------|
| id                     | SMALLINT  | no          |                | primary    |           |
| name                   | CHAR(60)  | no          |                |            |           |
| the_order              | SMALLINT  | no          |                |            |           |
| gender_rate            | SMALLINT  | no          |                |            |           |
| capture_rate           | SMALLINT  | no          |                |            |           |
| base_happiness         | SMALLINT  | yes         |                |            |           |
| is_baby                | BOOLEAN   | no          |                |            |           |
| is_legendary           | BOOLEAN   | no          |                |            |           |
| is_mythical            | BOOLEAN   | no          |                |            |           |
| hatch_counter          | MEDIUMINT | yes         |                |            |           |
| has_gender_differences | BOOLEAN   | no          |                |            |           |
| forms_switchable       | BOOLEAN   | no          |                |            |           |
| growth_rate            | ENUM      | no          |                |            |           |
| generation             | CHAR(60)  | no          |                |            |           |

the detailed ENUM type for `growth` is `ENUM('slow', 'medium', 'fast', 'medium-slow', 'slow-then-very-fast', 'fast-then-very-slow')` (the separated description is mainly for better rendering markdown table using my emacs editor)

### species_egg_group

| COLUMN_NAME  | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE     |
|--------------|-----------|-------------|----------------|------------|---------------|
| species_id   | SMALLINT  | no          |                | primary    | species(id)   |
| egg_group_id | SMALLINT  | no          |                | primary    | egg_group(id) |

### species_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|---------------|-----------|-------------|----------------|------------|-------------|
| species_id    | SMALLINT  | no          |                | primary    | species(id) |
| language_code | CHAR(60)  | no          |                | primary    |             |
| name          | CHAR(60)  | no          |                |            |             |

### species_flavor_text

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|---------------|-----------|-------------|----------------|------------|-------------|
| species_id    | SMALLINT  | no          |                | primary    | species(id) |
| language_code | CHAR(60)  | no          |                | primary    |             |
| text          | TEXT      | no          |                |            |             |
| game_id       | SMALLINT  | no          |                |            | game(id)    |

### species_form_descriptions

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|---------------|-----------|-------------|----------------|------------|-------------|
| species_id    | SMALLINT  | no          |                | primary    | species(id) |
| language_code | CHAR(60)  | no          |                | primary    |             |
| description   | TEXT      | no          |                |            |             |

## Egg Group

### egg_group

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| id          | SMALLINT  | no          |                | primary    |           |
| name        | CHAR(60)  | no          |                |            |           |

### egg_group_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE     |
|---------------|-----------|-------------|----------------|------------|---------------|
| egg_group_id  | SMALLINT  | no          |                | primary    | egg_group(id) |
| language_code | CHAR(60)  | no          |                | primary    |               |
| name          | CHAR(60)  | no          |                |            |               |

## Move

### move

| COLUMN_NAME          | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE             |
|----------------------|-----------|-------------|----------------|------------|-----------------------|
| id                   | SMALLINT  | no          |                | primary    |                       |
| name                 | CHAR(60)  | no          |                |            |                       |
| power                | SMALLINT  | yes         |                |            |                       |
| accuracy             | SMALLINT  | yes         |                |            |                       |
| pp                   | SMALLINT  | yes         |                |            |                       |
| priority             | SMALLINT  | yes         |                |            |                       |
| generation           | CHAR(60)  | no          |                |            |                       |
| type_id              | SMALLINT  | no          |                |            | type(id)              |
| move_damage_class_id | SMALLINT  | no          |                |            | move_damage_class(id) |

### move_effects

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|---------------|-----------|-------------|----------------|------------|-----------|
| move_id       | SMALLINT  | no          |                | primary    | move(id)  |
| language_code | CHAR(60)  | no          |                | primary    |           |
| effect        | TEXT      | no          |                |            |           |
| short_effect  | TINYTEXT  | yes         |                |            |           |

### move_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|---------------|-----------|-------------|----------------|------------|-----------|
| move_id       | SMALLINT  | no          |                | primary    | move(id)  |
| language_code | CHAR(60)  | no          |                | primary    |           |
| name          | CHAR(60)  | no          |                |            |           |

### move_flavor_text

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE      |
|---------------|-----------|-------------|----------------|------------|----------------|
| move_id       | SMALLINT  | no          |                | primary    | move(id)       |
| language_code | CHAR(60)  | no          |                | primary    |                |
| text          | TEXT      | no          |                |            |                |
| game_group_id | SMALLINT  | no          |                |            | game_group(id) |

## Move Damage Class

### move_damage_class
	
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| id          | SMALLINT  | no          |                | primary    |           |
| class_name  | CHAR(60)  | no          |                |            |           |

### move_damage_class_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE             |
|---------------|-----------|-------------|----------------|------------|-----------------------|
| class_id      | SMALLINT  | no          |                | primary    | move_damage_class(id) |
| language_code | CHAR(60)  | no          |                | primary    |                       |
| name          | CHAR(60)  | no          |                |            |                       |

### move_damage_class_descriptions

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE             |
|---------------|-----------|-------------|----------------|------------|-----------------------|
| class_id      | SMALLINT  | no          |                | primary    | move_damage_class(id) |
| language_code | CHAR(60)  | no          |                | primary    |                       |
| description   | TEXT      | no          |                |            |                       |

## Ability

### ability

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| id          | SMALLINT  | no          |                | primary    |           |
| name        | CHAR(60)  | no          |                |            |           |
| generation  | CHAR(60)  | no          |                |            |           |

### ability_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|---------------|-----------|-------------|----------------|------------|-------------|
| ability_id    | SMALLINT  | no          |                | primary    | ability(id) |
| language_code | CHAR(60)  | no          |                | primary    |             |
| name          | CHAR(60)  | no          |                |            |             |

### ability_effects

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|---------------|-----------|-------------|----------------|------------|-------------|
| ability_id    | SMALLINT  | no          |                | primary    | ability(id) |
| language_code | CHAR(60)  | no          |                | primary    |             |
| effect        | TEXT      | no          |                |            |             |
| short_effect  | TINYTEXT  | yes         |                |            |             |

### ability_flavor_text

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE      |
|---------------|-----------|-------------|----------------|------------|----------------|
| ability_id    | SMALLINT  | no          |                | primary    | ability(id)    |
| language_code | CHAR(60)  | no          |                | primary    |                |
| text          | TEXT      | no          |                |            |                |
| game_group_id | SMALLINT  | no          |                |            | game_group(id) |

## Type

### type
| COLUMN_NAME          | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE             |
|----------------------|-----------|-------------|----------------|------------|-----------------------|
| id                   | SMALLINT  | no          |                | primary    |                       |
| name                 | CHAR(60)  | no          |                |            |                       |
| generation           | CHAR(60)  | no          |                |            |                       |
<!-- the move_damage_class of type 18 is null -->
<!-- | move_damage_class_id | SMALLINT  | no          |                |            | move_damage_class(id) | -->

### type_relation

**NOTE**: 'normal' damage is omitted by default when getting data from `pokeapi`

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| from_id     | SMALLINT  | no          |                | primary    | type(id)  |
| to_id       | SMALLINT  | no          |                | primary    | type(id)  |
| damage      | ENUM      | no          |                |            |           |

**NOTE**: detailed version of `ENUM` type of the `damage` column is `ENUM('no', 'half', 'normal', 'double')`

### type_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|---------------|-----------|-------------|----------------|------------|-----------|
| type_id       | SMALLINT  | no          |                | primary    | type(id)  |
| language_code | CHAR(60)  | no          |                | primary    |           |
| name          | CHAR(60)  | no          |                |            |           |

## Item

### item

| COLUMN_NAME    | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|----------------|-----------|-------------|----------------|------------|-----------|
| id             | SMALLINT  | no          |                | primary    |           |
| name           | CHAR(60)  | no          |                |            |           |
| cost           | INT       | no          |                |            |           |
| category       | CHAR(60)  | no          |                |            |           |
| default_sprite | CHAR(255) | yes         |                |            |           |
| fling_power    | SMALLINT  | yes         |                |            |           |

### item_effects

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|---------------|-----------|-------------|----------------|------------|-----------|
| item_id       | SMALLINT  | no          |                | primary    | item(id)  |
| language_code | CHAR(60)  | no          |                | primary    |           |
| effect        | TEXT      | no          |                |            |           |
| short_effect  | TINYTEXT  | yes         |                |            |           |

### item_flavor_text

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE      |
|---------------|-----------|-------------|----------------|------------|----------------|
| item_id       | SMALLINT  | no          |                | primary    | item(id)       |
| language_code | CHAR(60)  | no          |                | primary    |                |
| game_group_id | SMALLINT  | no          |                |            | game_group(id) |
| text          | TEXT      | no          |                |            |                |

### item_game_indices

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| item_id     | SMALLINT  | no          |                | primary    | item(id)  |
| generation  | CHAR(60)  | no          |                | primary    |           |
| game_index  | SMALLINT  | no          |                |            |           |

### item_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|---------------|-----------|-------------|----------------|------------|-----------|
| item_id       | SMALLINT  | no          |                | primary    | item(id)  |
| language_code | CHAR(60)  | no          |                | primary    |           |
| name          | CHAR(60)  | no          |                |            |           |
	
## Location

### region

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| id          | SMALLINT  | no          |                | primary    |           |
| name        | CHAR(60)  | no          |                |            |           |

### location

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE  |
|-------------|-----------|-------------|----------------|------------|------------|
| id          | SMALLINT  | no          |                | primary    |            |
| name        | CHAR(60)  | no          |                |            |            |
| region_id   | SMALLINT  | yes         |                |            | region(id) |

`region_id` is nullable, see: https://pokeapi.co/api/v2/location/265 or https://pokeapi.co/api/v2/location/299

### area

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE    |
|-------------|-----------|-------------|----------------|------------|--------------|
| id          | SMALLINT  | no          |                | primary    |              |
| name        | CHAR(60)  | no          |                |            |              |
| location_id | SMALLINT  | no          |                |            | location(id) |

### region_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE  |
|---------------|-----------|-------------|----------------|------------|------------|
| region_id     | SMALLINT  | no          |                | primary    | region(id) |
| language_code | CHAR(60)  | no          |                | primary    |            |
| name          | CHAR(60)  | no          |                |            |            |

### location_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE    |
|---------------|-----------|-------------|----------------|------------|--------------|
| location_id   | SMALLINT  | no          |                | primary    | location(id) |
| language_code | CHAR(60)  | no          |                | primary    |              |
| name          | CHAR(60)  | no          |                |            |              |

### area_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|---------------|-----------|-------------|----------------|------------|-----------|
| area_id       | SMALLINT  | no          |                | primary    | area(id)  |
| language_code | CHAR(60)  | no          |                | primary    |           |
| name          | CHAR(60)  | no          |                |            |           |

## Encounter

### encounter

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE   |
|-------------|-----------|-------------|----------------|------------|-------------|
| id          | SMALLINT  | no          |                | primary    |             |
| area_id     | SMALLINT  | no          |                | primary    | area(id)    |
| pokemon_id  | SMALLINT  | no          |                | primary    | pokemon(id) |
| game_id     | SMALLINT  | no          |                | primary    | game(id)    |
| max_chance  | SMALLINT  | no          |                |            |             |
max_change can greater than 100 :<

### encounter_method

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| id          | SMALLINT  | no          |                | primary    |           |
| name        | CHAR(60)  | no          |                |            |           |
| the_order   | SMALLINT  | no          |                |            |           |

### encounter_condition

**NOTE**: insert condition with id equals to 0 as `no condition`

| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| id          | SMALLINT  | no          |                | primary    |           |
| name        | CHAR(60)  | no          |                |            |           |

### encounter_detail

| COLUMN_NAME            | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE               |
|------------------------|-----------|-------------|----------------|------------|-------------------------|
| encounter_id           | SMALLINT  | no          |                | primary    | encounter(id)           |
| encounter_method_id    | SMALLINT  | no          |                | primary    | encounter_method(id)    |
| encounter_condition_id | SMALLINT  | no          |                | primary    | encounter_condition(id) |
| max_level              | TINYINT   | no          |                |            |                         |
| min_level              | TINYINT   | no          |                |            |                         |
| chance                 | SMALLINT  | no          |                |            |                         |

### encounter_method_names

| COLUMN_NAME         | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE            |
|---------------------|-----------|-------------|----------------|------------|----------------------|
| encounter_method_id | SMALLINT  | no          |                | primary    | encounter_method(id) |
| language_code       | CHAR(60)  | no          |                | primary    |                      |
| name                | CHAR(255) | no          |                |            |                      |

### encounter_condition_names

| COLUMN_NAME            | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE               |
|------------------------|-----------|-------------|----------------|------------|-------------------------|
| encounter_condition_id | SMALLINT  | no          |                | primary    | encounter_condition(id) |
| language_code          | CHAR(60)  | no          |                | primary    |                         |
| name                   | CHAR(255) | no          |                |            |                         |

## Game

### game_group
    
| COLUMN_NAME | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|-------------|-----------|-------------|----------------|------------|-----------|
| id          | SMALLINT  | no          |                | primary    |           |
| name        | CHAR(60)  | no          |                |            |           |
| generation  | CHAR(60)  | no          |                |            |           |

### game

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE      |
|---------------|-----------|-------------|----------------|------------|----------------|
| id            | SMALLINT  | no          |                | primary    |                |
| name          | CHAR(60)  | no          |                |            |                |
| game_group_id | SMALLINT  | no          |                |            | game_group(id) |

### game_names

| COLUMN_NAME   | DATA_TYPE | IS_NULLABLE | COLUMN_DEFAULT | COLUMN_KEY | REFERENCE |
|---------------|-----------|-------------|----------------|------------|-----------|
| game_id       | SMALLINT  | no          |                | primary    | game(id)  |
| language_code | CHAR(60)  | no          |                | primary    |           |
| name          | CHAR(60)  | no          |                |            |           |
