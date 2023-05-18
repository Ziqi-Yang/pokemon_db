# NOTE: Pokemon id >= 10001 is the one variant (from) of the origin Pokemon
# NOTE: no network condition judge
import requests
import asyncio
import aiopoke
from aiopoke import AiopokeClient
from aiopoke.objects.resources.pokemon.natural_gift_type import TypeRelations
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
errorSet = set()
type_damage_relationship = dict()

def get_id(url: str):
    id_str = urlparse(url).path.rstrip('/').split('/')[-1]
    return int(id_str)

def fetch_resources(url: str):
    resp = requests.get(url)
    resp.raise_for_status()
    res = json(resp.content)["results"]
    # NOTE: since the pokeapi has some errors like ['version/28' error, but 'version/28/' ok and 'version/name' ok] (vice versa, we need to try both methods)
    res = [(get_id(v["url"]), v["name"]) for v in res] 
    return res

async def fw_all_stats(client: AiopokeClient):
    res = fetch_resources(ALL_STATS_URL)
    info("[*] fetch and write all STATS")
    await asyncio.gather(*(fw_stat(client, id_name) for id_name in res))
    
async def fw_all_egg_groups(client: AiopokeClient):
    res = fetch_resources(ALL_EGG_GROUPS_URL)
    info("[*] fetch and write all EGG GROUPS")
    await asyncio.gather(*(fw_egg_group(client, id_name) for id_name in res))

async def fw_all_species(client: AiopokeClient):
    res = fetch_resources(ALL_SPECIES_URL)
    info("[*] fetch and write all SPECIES")
    await asyncio.gather(*(fw_species(client, id_name) for id_name in res))

async def fw_all_move_damage_classes(client: AiopokeClient):
    res = fetch_resources(ALL_MOVE_DAMAGE_CLASSES_URL)
    info("[*] fetch and write all MOVE_DAMAGE_CLASSES")
    await asyncio.gather(*(fw_move_damage_class(client, id_name) for id_name in res))

async def fw_all_abilities(client: AiopokeClient):
    res = fetch_resources(ALL_ABILITIES_URL)
    info("[*] fetch and write all ABILITIES")
    await asyncio.gather(*(fw_ability(client, id_name) for id_name in res))

async def fw_all_game_groups(client: AiopokeClient):
    res = fetch_resources(ALL_GAME_GROUPS_URL)
    info("[*] fetch and write all GAME_GROUPS")
    await asyncio.gather(*(fw_game_group(client, id_name) for id_name in res))

async def fw_all_games(client: AiopokeClient):
    res = fetch_resources(ALL_GAMES_URL)
    info("[*] fetch and write all GAMES")
    await asyncio.gather(*(fw_game(client, id_name) for id_name in res))

async def fw_all_types(client: AiopokeClient):
    res = fetch_resources(ALL_TYPES_URL)
    info("[*] fetch and write all TYPES")
    # NOTE ignore type > 10000, it will brings us unfortunate
    await asyncio.gather(*(fw_type(client, id_name) for id_name in res if id_name[0] < 10000))
    if not query_data_existence(cn, "type", f"id=18"):
        fw_type_18() # NOTE: we should do this manually due to a bug(maybe) in aiopokeapi 
    fw_type_relations([v for v in res if v[0] < 10000])

async def fw_all_items(client: AiopokeClient):
    res = fetch_resources(ALL_ITEMS_URL)
    info("[*] fetch and write all items")
    await asyncio.gather(*(fw_item(client, id_name) for id_name in res))
    await fw_missing_items()

async def fw_stat(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "stat", f"id={id}"):
        print(f"- stat {id} already exists")
        return
    try:
        stat = await client.get_stat(id)
    except:
        try:
            stat = await client.get_stat(name)
        except:
            errorSet.add(f"stat {id}")
            return
        
    # stat
    insert_into_table(cn, "stat", stat.id, stat.name, stat.is_battle_only)
    # stat_names
    for n in stat.names:
        insert_into_table(cn, "stat_names", stat.id, n.language.name, n.name)
    print(f"+ FW stat {id} done")

async def fw_species(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "species", f"id={id}"):
        print(f"- species {id} already exists")
        return
    try:
        species = await client.get_pokemon_species(id)
    except:
        try:
            species = await client.get_pokemon_species(name)
        except:
            errorSet.add(f"species {id}")
            return

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

async def fw_egg_group(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "egg_group", f"id={id}"):
        print(f"- egg_group {id} already exists")
        return
    try:
        egg_group = await client.get_egg_group(id)
    except:
        try:
            egg_group = await client.get_egg_group(name)
        except:
            errorSet.add(f"egg_group {id}")
            return
    # egg_group
    insert_into_table(cn, "egg_group", egg_group.id, egg_group.name)
    # egg_group_names
    for n in egg_group.names:
        insert_into_table(cn, "egg_group_names", egg_group.id, n.language.name, n.name)
    print(f"+ FW egg_group {id} done")

async def fw_move_damage_class(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "move_damage_class", f"id={id}"):
        print(f"- move_damage_class {id} already exists")
        return
    try:
        mdc = await client.get_move_damage_class(id)
    except:
        try:
            mdc = await client.get_move_damage_class(name)
        except:
            errorSet.add(f"move_damage_class {id}")
            return
    # move_damage_class
    insert_into_table(cn, "move_damage_class", mdc.id, mdc.name)
    # move_damage_class_names
    for n in mdc.names:
        insert_into_table(cn, "move_damage_class_names", mdc.id, n.language.name, n.name)
    # move_damage_class_descriptions
    for d in mdc.descriptions:
        insert_into_table(cn, "move_damage_class_descriptions", mdc.id, d.language.name, d.description)
    print(f"+ FW move_damage_class {id} done")

async def fw_ability(client: AiopokeClient, id_name: tuple):
    """NOTE: after GAME_GROUP"""
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "ability", f"id={id}"):
        print(f"- ability {id} already exists")
        return
    try:
        ab = await client.get_ability(id)
    except:
        try:
            ab = await client.get_ability(name)
        except:
            errorSet.add(f"ability {id}")
            return
    if query_data_existence(cn, "ability", f"id={id}"):
        print(f"- ability {id} already exists")
        return
        
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

async def fw_game_group(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "game_group", f"id={id}"):
        print(f"- game_group {id} already exists")
        return
    try:
        gp = await client.get_version_group(id)
    except:
        try:
            gp = await client.get_version_group(name)
        except:
            errorSet.add(f"game_group {id}")
            return

    # game_group
    insert_into_table(cn, "game_group", gp.id, gp.name, gp.generation.name)
    print(f"+ FW game_group {id} done")

async def fw_game(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "game", f"id={id}"):
        print(f"- game {id} already exists")
        return
    try:
        game = await client.get_version(id)
    except:
        try:
            game = await client.get_version(name)
        except:
            errorSet.add(f"game {id}")
            return
    # game
    insert_into_table(cn, "game", game.id, game.name, game.version_group.id)
    # game_names
    for n in game.names:
        insert_into_table(cn, "game_names", game.id, n.language.name, n.name)
    print(f"+ FW game {id} done")

async def fw_type(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "type", f"id={id}"):
        print(f"- type {id} already exists")
        return
    try:
        type = await client.get_type(id)
    except:
        try:
            type = await client.get_type(name)
        except:
            if id == 18:
                return
            errorSet.add(f"type {id}")
            return
    # type
    insert_into_table(cn, "type", type.id, type.name, type.generation.name)
    # type_names
    for n in type.names:
        insert_into_table(cn, "type_names", type.id, n.language.name, n.name)
    # store type damage relations 
    type_damage_relationship[type.id] = type.damage_relations
    print(f"+ FW type {id} done")

def fw_type_18(): # TODO temporary solution
    resp = requests.get("https://pokeapi.co/api/v2/type/18")
    resp.raise_for_status()
    type = json(resp.content)
    insert_into_table(cn, "type", type["id"], type["name"], type["generation"]["name"])
    for n in type["names"]:
        insert_into_table(cn, "type_names", type["id"], n["language"]["name"], n["name"])
    type_damage_relationship[18] = TypeRelations(**type["damage_relations"])
    print("+ FW type 18 done")

def fw_type_relations(all_types: list):
    """NOTE: use after executing 'fw_type', complete missing normal part the type relationship table"""
    for from_id,_ in all_types:
        for t in type_damage_relationship[from_id].no_damage_to:
            insert_into_table(cn, "type_relation", from_id, t.id, "no")
        for t in type_damage_relationship[from_id].half_damage_to:
            insert_into_table(cn, "type_relation", from_id, t.id, "half")
        for t in type_damage_relationship[from_id].double_damage_to:
            insert_into_table(cn, "type_relation", from_id, t.id, "double")
        for to_id, _ in all_types:
            if not query_data_existence(cn, "type_relation", f"from_id={from_id} AND to_id={to_id}"):
                insert_into_table(cn, "type_relation", from_id, to_id, "normal")

async def fw_item(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_data_existence(cn, "item", f"id={id}"):
        print(f"- item {id} already exists")
        return
    try:
        item = await client.get_item(id)
    except:
        try:
            item = await client.get_item(name)
        except:
            errorSet.add(f"item {id}")
            return
    # item
    if item.sprite and item.sprite.default:
        insert_into_table(cn, "item", item.id, item.name, item.cost, item.category.name, item.sprite.default.url, item.fling_power)
    else:
        insert_into_table(cn, "item", item.id, item.name, item.cost, item.category.name, None, item.fling_power)
    # item_effects
    for e in item.effect_entries:
        insert_into_table(cn, "item_effects", item.id, e.language.name, e.effect, e.short_effect)
    # item_flavor_text
    for f in item.flavor_text_entries:
        insert_into_table(cn, "item_flavor_text", item.id, f.language.name, f.version_group.id, f.text)
    # item_game_indices
    for g in item.game_indices:
        insert_into_table(cn, "item_game_indices", item.id, g.generation.name, g.game_index)
    # item_names
    for n in item.names:
        insert_into_table(cn, "item_names", item.id, n.language.name, n.name)
    print(f"+ FW item {id} done")

async def fw_missing_items():
    info("fw missing items")
    ids = []
    for item in errorSet:
        if item.startswith("item"):
            id = int(item[5:])
            ids.append(id)
    
    await asyncio.gather(*(fw_missing_item(id, urljoin(API_BASE, f"item/{id}/")) for id in ids))

async def fw_missing_item(id: int, url: str):
    resp = requests.get(url)
    if not resp.ok:
        print(f"- FW item {id} failed!!!")
        return
    item = json(resp.content)
    # item
    if "sprite" in item and item["sprite"] and "default" in item["sprite"]:
        insert_into_table(cn, "item", item["id"], item["name"], item["cost"], item["category"]["name"], item["sprite"]["default"]["url"], item["fling_power"])
    else:
        insert_into_table(cn, "item", item["id"], item["name"], item["cost"], item["category"]["name"], None, item["fling_power"])
    # item_effects
    for e in item.effect_entries:
        insert_into_table(cn, "item_effects", item["id"], e["language"]["name"], e["effect"], e["short_effect"])
    # item_flavor_text
    for f in item.flavor_text_entries:
        insert_into_table(cn, "item_flavor_text", item["id"], f["language"]["name"], f["version_group"]["id"], f["text"])
    # item_game_indices
    for g in item.game_indices:
        insert_into_table(cn, "item_game_indices", item["id"], g["generation"]["name"], g["game_index"])
    # item_names
    for n in item.names:
        insert_into_table(cn, "item_names", item["id"], n["language"]["name"], n["name"])
    print(f"+ FW item {id} done")
    errorSet.remove(f"item {id}")


async def main():
    # await fw_all_stats()
    client = aiopoke.AiopokeClient()
    
    # await fw_all_stats(client)
    # await fw_all_species(client) # TODO 
    # await fw_all_egg_groups(client)
    # await fw_all_move_damage_classes(client)
    await fw_all_game_groups(client)
    await fw_all_games(client)
    # await fw_all_abilities(client) # NOTE: after game_group
    # await fw_all_types(client) 
    await fw_all_items(client) 

    res = await asyncio.gather(*())
    await client.close()
    return res

# async def fw_all_XXXXX(client: AiopokeClient):
#     res = fetch_resources(XXXXX)
#     info("[*] fetch and write all XXXXX")
#     await asyncio.gather(*(fw_XXXXX(client, id_name) for id_name in res))

# async def fw_XXXXX(client: AiopokeClient, id_name: tuple):
#     id = id_name[0]
#     name = id_name[1]
#     if query_data_existence(cn, "XXXXX", f"id={id}"):
#         print(f"- XXXXX {id} already exists")
#         return
#     try:
#         XXXXX = await client.get_XXXXX(id)
#     except:
#         try:
#             XXXXX = await client.get_XXXXX(name)
#         except:
#             errorSet.add(f"XXXXX {id}")
#             return
#     # XXXXX
#     insert_into_table(cn, "XXXXX", XXXXX.id, XXXXX.name, XXXXX.is_battle_only)
#     # XXXXX_names
#     for n in XXXXX.names:
#         insert_into_table(cn, "XXXXX_names", XXXXX.id, n.language.name, n.name)
#     print(f"+ FW XXXXX {id} done")

if __name__ == "__main__":
    # drop_db(cn)
    create_db(cn)
    create_tables(cn)

    info("[-------------------- fetch and write datas --------------------]")
    res = asyncio.run(main())
    if len(errorSet):
        print("[-------------------- Error List --------------------]")
        print(errorSet)
