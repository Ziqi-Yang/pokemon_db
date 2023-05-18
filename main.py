# NOTE: Pokemon id >= 10001 is the one variant (from) of the origin Pokemon
# NOTE: no network condition judge
import requests
import asyncio
import aiopoke
from json import loads as json
from urllib.parse import urljoin
from db import Conn, drop_db, create_db, create_tables

INFINITY = 100000000
API_BASE = "https://pokeapi.co/api/v2/"
ALL_POKEMONS_URL = urljoin(API_BASE, f"pokemon?limit={INFINITY}")
ALL_STATS_URL = urljoin(API_BASE, f"stat?limit={INFINITY}")
ALL_SPECIES_URL = urljoin(API_BASE, f"pokemon-species?limit={INFINITY}")
ALL_EGG_GROUPS_URL = urljoin(API_BASE, f"egg-group?limit={INFINITY}")
ALL_MOVES_URL = urljoin(API_BASE, f"move?limit={INFINITY}")
ALL_MOVE_DAMAGE_CLASSES_URL = urljoin(API_BASE, f"move-damage-class?limit={INFINITY}")
ALL_ABILITIES_URL = urljoin(API_BASE, f"ability?limit={INFINITY}")
ALL_TYPES_URL = urljoin(API_BASE, f"type?limit={INFINITY}")
ALL_ITEMS_URL = urljoin(API_BASE, f"item?limit={INFINITY}")
ALL_REGIONS_URL = urljoin(API_BASE, f"region?limit={INFINITY}")
ALL_LOCATIONS_URL = urljoin(API_BASE, f"location?limit={INFINITY}")
ALL_AREAS_URL = urljoin(API_BASE, f"location-area?limit={INFINITY}")
ALL_GAMES_URL = urljoin(API_BASE, f"version?limit={INFINITY}")
ALL_GAME_GROUPS_URL = urljoin(API_BASE, f"version-group?limit={INFINITY}")

client = aiopoke.AiopokeClient()

def fetch_all_resources(url: str) -> list[str]:
    resp = requests.get(url)
    resp.raise_for_status()
    res = json(resp.content)["results"]
    return [v["name"] for v in res]

async def fw_pokemon_information(pokemon_name: str) -> bool:
    """fetch and store pokemon information into mysql database"""
    pokemon = await client.get_pokemon(pokemon_name)
    values = []

    return True

async def main():
    # pokemon = [ pokemon["name"] for pokemon in fetch_pokemon_list(1010)["results"]]
    res = await asyncio.gather(*())
    return res

if __name__ == "__main__":
    res = asyncio.run(main())

    cn = Conn()

    # drop_db(cn) 
    # create_db(cn)
    # create_tables(cn)
