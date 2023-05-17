Hi, chatgpt. This is a slice of one mysql design documentation written in markdown: 

```markdown
## Pokemon

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
```
I want you to help me convert tables like this into this python code form (note: some notice are in the python code comments):

```python
## pokemon
### pokemon_types
create_table(
	cursor, "pokemon_types",
	["pokemon_id", "ability_id", "is_hidden"],
	["SMALLINT", "SMALLINT", "BOOLEAN"], 
	[False, False, False],
	[None, None, None],
	["pokemon_id", "ability_id"],
	["pokemon(id)", "ability(id)", None])

### pokemon_types
create_table(
	cursor, "pokemon_types",
	["pokemon_id", "ability_id", "is_hidden"],
	["SMALLINT", "SMALLINT", "BOOLEAN"], 
	[False, False, False],
	[None, None, None],
	["pokemon_id", "ability_id"],
	["pokemon(id)", "ability(id)", None])
```

Note that the any comments that are in the same line with the code in the above example shouldn't be included in your answer.  
Also Note you should also include the header line into python code as the comments.  
Finally, remember that the header lines that begins with a lowercase character also stand for the mysql table name.
