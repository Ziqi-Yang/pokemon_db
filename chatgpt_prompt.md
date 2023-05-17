Hi, chatgpt. This is a slice of one mysql design documentation written in markdown: 

```markdown
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
I want you to help me convert tables(only the first and second column) like this into this python code form:

```python
# pokemon_types
create_table(
	cursor, "pokemon_types",
	["pokemon_id", "ability_id", "is_hidden"],
	["SMALLINT", "SMALLINT", "BOOLEAN"]
	False, None, ["id"], None)

# pokemon_types
create_table(
	cursor, "pokemon_types",
	["pokemon_id", "ability_id", "is_hidden"],
	["SMALLINT", "SMALLINT", "BOOLEAN"]
	False, None, ["id"], None)
```

Note you should also include the header line into python code as the comments.  
Also note that the line `False, None, ["id"], None)` is always the same, and it has no relationship with the table.
Finally, remember that the header lines that begins with a lowercase character also stand for the mysql table name.
