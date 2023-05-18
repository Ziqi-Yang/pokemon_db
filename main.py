# NOTE: Pokemon id >= 10001 is the one variant (from) of the origin Pokemon
# NOTE: no network condition judge
import requests
import asyncio
import aiopoke
from aiopoke import AiopokeClient
from json import loads as json
from urllib.parse import urlparse, urljoin
from db import Conn, drop_db, create_db, create_tables, insert_into_table, query_data_existence
import logging
from logging import info 

logging.getLogger().setLevel(logging.INFO)

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

def get_id(url: str):
    id_str = urlparse(url).path.rstrip('/').split('/')[-1]
    return int(id_str)

def fetch_resources(url: str) -> list[int]:
    resp = requests.get(url)
    resp.raise_for_status()
    res = json(resp.content)["results"]
    return [get_id(v["url"]) for v in res]

async def fw_all_stats(client: AiopokeClient):
    res = fetch_resources(ALL_STATS_URL)
    info("[*] fetch and write all STATS")
    await asyncio.gather(*(fw_stat(client, id) for id in res))
    

async def fw_stat(client: AiopokeClient, id: int):
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- stat {id} already exists")
        return
    stat = await client.get_stat(id)
    insert_into_table(cn, "stat", stat.id, stat.name, stat.is_battle_only)
    for n in stat.names:
        insert_into_table(cn, "stat_names", stat.id, n.language.name, n.name)
    print(f"+ FW {id} done")

async def fw_all_species(client: AiopokeClient):
    res = fetch_resources(ALL_SPECIES_URL)
    info("[*] fetch and write all SPECIES")
    await asyncio.gather(*(fw_species(client, id) for id in res))

async def fw_species(client: AiopokeClient, id: int):
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- species {id} already exists")
        return
    species = await client.get_pokemon_species(id)
    insert_into_table(cn, "species", species.id, species.name, species.order, species.gender_rate,
                      species.capture_rate, species.base_happiness, species.is_baby, species.is_legendary,
                      species.is_mythical, species.hatch_counter, species.has_gender_differences,
                      species.forms_switchable, species.growth_rate.name, species.generation.name)
    for n in species.names:
        insert_into_table(cn, "species_names", species.id, n.language.name, n.name)
    # TODO 
    # for e in species.egg_groups:
    #     insert_into_table(cn, "species_egg_group", species.id, e., n.name)
    print(f"+ FW {id} done")

async def fw_all_egg_groups(client: AiopokeClient):
    res = fetch_resources(ALL_EGG_GROUPS_URL)
    info("[*] fetch and write all EGG GROUPS")
    await asyncio.gather(*(fw_egg_group(client, id) for id in res))

async def fw_egg_group(client: AiopokeClient, id: int):
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- egg_group {id} already exists")
        return
    egg_group = await client.get_egg_group(id)
    insert_into_table(cn, "egg_group", egg_group.id, egg_group.name)
    for n in egg_group.names:
        insert_into_table(cn, "egg_group_names", egg_group.id, n.language.name, n.name)
    print(f"+ FW {id} done")

async def fw_pokemon(client: AiopokeClient, pokemon_name: str) -> bool:
    """fetch and store pokemon information into mysql database"""
    pokemon = await client.get_pokemon(pokemon_name)
    values = []
    return True

async def main():
    # await fw_all_stats()
    client = aiopoke.AiopokeClient()
    
    # await fw_all_stats(client)
    # await fw_all_species(client)
    await fw_all_egg_groups(client)

    res = await asyncio.gather(*())
    await client.close()
    return res

if __name__ == "__main__":
    drop_db(cn)
    create_db(cn)
    create_tables(cn)

    info("[-------------------- fetch and write datas --------------------]")
    res = asyncio.run(main())
