# NOTE: Pokemon id >= 10001 is the one variant (from) of the origin Pokemon
# NOTE: no network condition judge
import requests
import asyncio
import aiopoke
from aiopoke import AiopokeClient
from json import loads as json
from urllib.parse import urljoin
from db import Conn, drop_db, create_db, create_tables, insert_into_table

INFINITY = 1000000
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

cn = Conn()

def fetch_resources(url: str) -> list[str]:
    resp = requests.get(url)
    resp.raise_for_status()
    res = json(resp.content)["results"]
    return [v["name"] for v in res]

async def fw_all_stats(client: AiopokeClient):
    # res = fetch_resources(ALL_STATS_URL)
    await fw_stat(client, "hp")
    

async def fw_stat(client: AiopokeClient, stat_name: str):
    stat = await client.get_stat(stat_name)
    insert_into_table(cn, "stat", stat.id, stat.name, stat.is_battle_only)

async def fw_pokemon(client: AiopokeClient, pokemon_name: str) -> bool:
    """fetch and store pokemon information into mysql database"""
    pokemon = await client.get_pokemon(pokemon_name)
    values = []
    return True

async def main():
    # await fw_all_stats()
    client = aiopoke.AiopokeClient()
    await fw_all_stats(client)
    res = await asyncio.gather(*())
    await client.close()
    return res

if __name__ == "__main__":
    create_db(cn)
    create_tables(cn)

    res = asyncio.run(main())
