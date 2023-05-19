# Pokemon DB

Convert data from [pokeapi](https://github.com/PokeAPI/pokeapi) into MySQL database.

## Related Resources

1. https://github.com/PokeAPI/pokeapi
2. https://github.com/beastmatser/aiopokeapi

## database connection

I use `mariadb`, here is the connection detail(in the file `db.py`):

``` python
class Conn:
    def __init__(self):
        self.conn = connector.connect(
            user='root',
            password='root',
            host='127.0.0.1'
        )
        self.cursor = self.conn.cursor()
```

