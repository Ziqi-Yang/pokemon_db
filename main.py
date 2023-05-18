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

def fetch_resources(url: str, use_name = False):
    resp = requests.get(url)
    resp.raise_for_status()
    res = json(resp.content)["results"]
    if use_name:
        res = [v["name"] for v in res]
    else:
        res = [get_id(v["url"]) for v in res]
    return res

async def fw_all_stats(client: AiopokeClient):
    res = fetch_resources(ALL_STATS_URL)
    info("[*] fetch and write all STATS")
    await asyncio.gather(*(fw_stat(client, id) for id in res))
    
async def fw_all_egg_groups(client: AiopokeClient):
    res = fetch_resources(ALL_EGG_GROUPS_URL)
    info("[*] fetch and write all EGG GROUPS")
    await asyncio.gather(*(fw_egg_group(client, id) for id in res))

async def fw_all_species(client: AiopokeClient):
    res = fetch_resources(ALL_SPECIES_URL)
    info("[*] fetch and write all SPECIES")
    await asyncio.gather(*(fw_species(client, id) for id in res))

async def fw_all_move_damage_classes(client: AiopokeClient):
    res = fetch_resources(ALL_MOVE_DAMAGE_CLASSES_URL)
    info("[*] fetch and write all MOVE_DAMAGE_CLASSES")
    await asyncio.gather(*(fw_move_damage_class(client, id) for id in res))

async def fw_all_abilities(client: AiopokeClient):
    res = fetch_resources(ALL_ABILITIES_URL)
    info("[*] fetch and write all ABILITIES")
    await asyncio.gather(*(fw_ability(client, id) for id in res))

async def fw_all_game_groups(client: AiopokeClient):
    res = fetch_resources(ALL_GAME_GROUPS_URL, use_name = True)
    info("[*] fetch and write all GAME_GROUPS")
    await asyncio.gather(*(fw_game_group(client, name) for name in res))

async def fw_all_games(client: AiopokeClient):
    res = fetch_resources(ALL_GAMES_URL, use_name = True)
    info("[*] fetch and write all GAMES")
    await asyncio.gather(*(fw_game(client, name) for name in res))

async def fw_stat(client: AiopokeClient, id: int):
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- stat {id} already exists")
        return
    stat = await client.get_stat(id)
    # stat
    insert_into_table(cn, "stat", stat.id, stat.name, stat.is_battle_only)
    # stat_names
    for n in stat.names:
        insert_into_table(cn, "stat_names", stat.id, n.language.name, n.name)
    print(f"+ FW stat {id} done")

async def fw_species(client: AiopokeClient, id: int):
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- species {id} already exists")
        return
    species = await client.get_pokemon_species(id)
    # species
    insert_into_table(cn, "species", species.id, species.name, species.order, species.gender_rate,
                      species.capture_rate, species.base_happiness, species.is_baby, species.is_legendary,
                      species.is_mythical, species.hatch_counter, species.has_gender_differences,
                      species.forms_switchable, species.growth_rate.name, species.generation.name)
    # species_names
    for n in species.names:
        insert_into_table(cn, "species_names", species.id, n.language.name, n.name)
    # TODO 
    # for e in species.egg_groups:
    #     insert_into_table(cn, "species_egg_group", species.id, e., n.name)
    print(f"+ FW species {id} done")

async def fw_egg_group(client: AiopokeClient, id: int):
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- egg_group {id} already exists")
        return
    egg_group = await client.get_egg_group(id)
    # egg_group
    insert_into_table(cn, "egg_group", egg_group.id, egg_group.name)
    # egg_group_names
    for n in egg_group.names:
        insert_into_table(cn, "egg_group_names", egg_group.id, n.language.name, n.name)
    print(f"+ FW egg_group {id} done")

async def fw_move_damage_class(client: AiopokeClient, id: int):
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- move_damage_class {id} already exists")
        return
    mdc = await client.get_move_damage_class(id)
    # move_damage_class
    insert_into_table(cn, "move_damage_class", mdc.id, mdc.name)
    # move_damage_class_names
    for n in mdc.names:
        insert_into_table(cn, "move_damage_class_names", mdc.id, n.language.name, n.name)
    # move_damage_class_descriptions
    for d in mdc.descriptions:
        insert_into_table(cn, "move_damage_class_descriptions", mdc.id, d.language.name, d.description)
    print(f"+ FW move_damage_class {id} done")

async def fw_ability(client: AiopokeClient, id: int):
    """NOTE: after GAME_GROUP"""
    # TODO 
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- ability {id} already exists")
        return
    ab = await client.get_ability(id)
    # ability
    insert_into_table(cn, "ability", ab.id, ab.name, ab.generation.name)
    # ability_names
    for n in ab.names:
        insert_into_table(cn, "ability_names", ab.id, n.language.name, n.name)
    # ability_effects
    for e in ab.effect_entries:
        insert_into_table(cn, "ability_effects", ab.id, e.language.name, e.effect, e.short_effect)
    # ability_flavor_text
    for t in ab.flavor_text_entries:
        insert_into_table(cn, "ability_flavor_text", ab.id, t.language.name, t.flavor_text, t.version_group.id)
    print(f"+ FW ability {id} done")

async def fw_game_group(client: AiopokeClient, name: str):
    if query_data_existence(cn, "game_group", f"name='{name}'"):
        print(f"- game_group {name} already exists")
        return
    gp = await client.get_version_group(name)
    # game_group
    insert_into_table(cn, "game_group", gp.id, gp.name, gp.generation.name)
    print(f"+ FW game_group {name} done")

async def fw_game(client: AiopokeClient, name: str):
    if query_data_existence(cn, "game", f"name='{name}'"):
        print(f"- game {name} already exists")
        return
    game = await client.get_version(name)
    # game
    insert_into_table(cn, "game", game.id, game.name, game.version_group.id)
    # game_names
    for n in game.names:
        insert_into_table(cn, "game_names", game.id, n.language.name, n.name)
    print(f"+ FW game {name} done")


async def fw_pokemon(client: AiopokeClient, pokemon_name: str) -> bool:
    """fetch and store pokemon information into mysql database"""
    pokemon = await client.get_pokemon(pokemon_name)
    values = []
    return True

async def main():
    # await fw_all_stats()
    client = aiopoke.AiopokeClient()
    
    # await fw_all_stats(client)
    # await fw_all_species(client) # TODO 
    # await fw_all_egg_groups(client)
    # await fw_all_move_damage_classes(client)
    # await fw_all_abilities(client)
    await fw_all_game_groups(client)
    await fw_all_games(client)

    res = await asyncio.gather(*())
    await client.close()
    return res

# async def fw_all_PROTO(client: AiopokeClient):
#     res = fetch_resources(XXXXX)
#     info("[*] fetch and write all XXXXX")
#     await asyncio.gather(*(fw_XXXXX(client, id) for id in res))

# async def fw_XXXXX(client: AiopokeClient, id: int):
#     if query_data_existence(cn, "XXXXX", f"id={id}"):
#         print(f"- XXXXX {id} already exists")
#         return
#     XXXXX = await client.get_XXXXX(id)
#     # XXXXX
#     insert_into_table(cn, "XXXXX", XXXXX.id, XXXXX.name, XXXXX.is_battle_only)
#     # XXXXX_names
#     for n in XXXXX.names:
#         insert_into_table(cn, "NOTE", XXXXX.id, n.language.name, n.name)
#     print(f"+ FW XXXXX {id} done")

if __name__ == "__main__":
    drop_db(cn)
    create_db(cn)
    create_tables(cn)

    info("[-------------------- fetch and write datas --------------------]")
    res = asyncio.run(main())
