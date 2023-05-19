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

def query_mul_table_id_existence(query: str, *tableNames) -> bool:
    for table in tableNames:
        if not query_data_existence(cn, table, query):
            return False
    return True

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
    
async def fw_all_species(client: AiopokeClient):
    res = fetch_resources(ALL_SPECIES_URL)
    info("[*] fetch and write all SPECIES")
    await asyncio.gather(*(fw_species(client, id_name) for id_name in res))

async def fw_all_egg_groups(client: AiopokeClient):
    res = fetch_resources(ALL_EGG_GROUPS_URL)
    info("[*] fetch and write all EGG GROUPS")
    await asyncio.gather(*(fw_egg_group(client, id_name) for id_name in res))

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
    await asyncio.gather(*(fw_type(client, id_name) for id_name in res))
    await fw_missing_types()
    fw_type_relations(res)

async def fw_all_items(client: AiopokeClient):
    res = fetch_resources(ALL_ITEMS_URL)
    info("[*] fetch and write all items")
    await asyncio.gather(*(fw_item(client, id_name) for id_name in res))
    await fw_missing_items()

async def fw_all_regions(client: AiopokeClient):
    res = fetch_resources(ALL_REGIONS_URL)
    info("[*] fetch and write all regions")
    await asyncio.gather(*(fw_region(client, id_name) for id_name in res))
    await fw_missing_regions()

async def fw_all_locations(client: AiopokeClient):
    res = fetch_resources(ALL_LOCATIONS_URL)
    info("[*] fetch and write all locations")
    await asyncio.gather(*(fw_location(client, id_name) for id_name in res))
    await fw_missing_locations()

async def fw_all_areas(client: AiopokeClient):
    res = fetch_resources(ALL_AREAS_URL)
    info("[*] fetch and write all areas")
    await asyncio.gather(*(fw_area(client, id_name) for id_name in res))

async def fw_all_moves(client: AiopokeClient):
    res = fetch_resources(ALL_MOVES_URL)
    info("[*] fetch and write all moves")
    await asyncio.gather(*(fw_move(client, id_name) for id_name in res))
    await fw_missing_moves()

async def fw_all_pokemons(client: AiopokeClient):
    res = fetch_resources(ALL_POKEMONS_URL)
    info("[*] fetch and write all pokemons")
    await asyncio.gather(*(fw_pokemon(client, id_name) for id_name in res))

async def fw_stat(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_mul_table_id_existence(f"id={id}", "stat") and query_mul_table_id_existence(f"stat_id={id}", "stat_names"):
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
    if query_mul_table_id_existence(f"id={id}", "species") and query_mul_table_id_existence(f"species_id={id}", "species_form_descriptions"):
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
    # species_egg_group
    for e in species.egg_groups:
        insert_into_table(cn, "species_egg_group", species.id, e.id)
    # species_names
    for n in species.names:
        insert_into_table(cn, "species_names", species.id, n.language.name, n.name)
    # species_flavor_text
    for f in species.flavor_text_entries:
        insert_into_table(cn, "species_flavor_text", species.id, f.language.name, f.flavor_text, f.version.id)
    # species_form_descriptions
    for f in species.form_descriptions:
        insert_into_table(cn, "species_form_descriptions", species.id, f.language.name, f.description)
    print(f"+ FW species {id} done")

async def fw_egg_group(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_mul_table_id_existence(f"id={id}", "egg_group") and query_mul_table_id_existence(f"egg_group_id={id}", "egg_group_names"):
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
    if query_mul_table_id_existence(f"id={id}", "move_damage_class") and query_mul_table_id_existence(f"class_id={id}", "move_damage_class_descriptions"):
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
    if query_mul_table_id_existence(f"id={id}", "ability") and query_mul_table_id_existence(f"ability_id={id}", "ability_flavor_text"):
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
    if query_mul_table_id_existence(f"id={id}", "game_group"):
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
    if query_mul_table_id_existence(f"id={id}", "game") and query_mul_table_id_existence(f"game_id={id}", "game_names"):
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
    if query_mul_table_id_existence(f"id={id}", "type") and query_mul_table_id_existence(f"from_id={id}", "type_relation") and query_mul_table_id_existence(f"type_id={id}", "type_names"):
        print(f"- type {id} already exists")
        return
    try:
        type = await client.get_type(id)
    except:
        try:
            type = await client.get_type(name)
        except:
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

async def fw_missing_types():
    info("fw missing types")
    ids = []
    for item in errorSet:
        if item.startswith("type"):
            id = int(item[5:])
            ids.append(id)
    
    await asyncio.gather(*(fw_missing_type(id, urljoin(API_BASE, f"type/{id}/")) for id in ids))

async def fw_missing_type(id, url): # TODO temporary solution
    resp = requests.get(url)
    if not resp.ok:
        print(f"- FW type {id} failed!!!")
        return
    type = json(resp.content)
    insert_into_table(cn, "type", type["id"], type["name"], type["generation"]["name"])
    for n in type["names"]:
        insert_into_table(cn, "type_names", type["id"], n["language"]["name"], n["name"])
    type_damage_relationship[id] = TypeRelations(**type["damage_relations"])
    print(f"+ FW type {id} done")
    errorSet.remove(f"type {id}")

def fw_type_relations(all_types: list):
    """NOTE: use after executing 'fw_type', complete missing normal part the type relationship table"""
    for from_id,_ in all_types:
        if from_id not in type_damage_relationship:
            continue
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
    if query_mul_table_id_existence(f"id={id}", "item") and query_mul_table_id_existence(f"item_id={id}", "item_names"):
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
    for e in item["effect_entries"]:
        insert_into_table(cn, "item_effects", item["id"], e["language"]["name"], e["effect"], e["short_effect"])
    # item_flavor_text
    for f in item["flavor_text_entries"]:
        insert_into_table(cn, "item_flavor_text", item["id"], f["language"]["name"], get_id(f["version_group"]["url"]), f["text"])
    # item_game_indices
    for g in item["game_indices"]:
        insert_into_table(cn, "item_game_indices", item["id"], g["generation"]["name"], g["game_index"])
    # item_names
    for n in item["names"]:
        insert_into_table(cn, "item_names", item["id"], n["language"]["name"], n["name"])
    print(f"+ FW item {id} done")
    errorSet.remove(f"item {id}")


async def fw_region(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_mul_table_id_existence(f"id={id}", "region") and query_mul_table_id_existence(f"region_id={id}", "region_names"):
        print(f"- region {id} already exists")
        return
    try:
        region = await client.get_region(id)
    except:
        try:
            region = await client.get_region(name)
        except:
            errorSet.add(f"region {id}")
            return
    # table region
    insert_into_table(cn, "region", region.id, region.name)
    # region_names
    for n in region.names:
        insert_into_table(cn, "region_names", region.id, n.language.name, n.name)
    print(f"+ FW region {id} done")

async def fw_location(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_mul_table_id_existence(f"id={id}", "location") and query_mul_table_id_existence(f"location_id={id}", "location_names"):
        print(f"- location {id} already exists")
        return
    try:
        location = await client.get_location(id)
    except:
        try:
            location = await client.get_location(name)
        except:
            errorSet.add(f"location {id}")
            return
    # location
    insert_into_table(cn, "location", location.id, location.name, location.region.id)
    # location_names
    for n in location.names:
        insert_into_table(cn, "location_names", location.id, n.language.name, n.name)
    print(f"+ FW location {id} done")

async def fw_area(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_mul_table_id_existence(f"id={id}", "area") and query_mul_table_id_existence(f"area_id={id}", "area_names"):
        print(f"- area {id} already exists")
        return
    try:
        area = await client.get_location_area(id)
    except:
        try:
            area = await client.get_location_area(name)
        except:
            errorSet.add(f"area {id}")
            return
    # area
    insert_into_table(cn, "area", area.id, area.name, area.location.id)
    # area_names
    for n in area.names:
        insert_into_table(cn, "area_names", area.id, n.language.name, n.name)
    print(f"+ FW area {id} done")


async def fw_missing_regions():
    info("fw missing regions")
    ids = []
    for item in errorSet:
        if item.startswith("region"):
            id = int(item[7:])
            ids.append(id)
    
    await asyncio.gather(*(fw_missing_region(id, urljoin(API_BASE, f"region/{id}/")) for id in ids))

async def fw_missing_region(id: int, url: str):
    resp = requests.get(url)
    if not resp.ok:
        print(f"- FW region {id} failed!!!")
        return
    region = json(resp.content)
    # table region
    insert_into_table(cn, "region", region["id"], region["name"])
    # region_names
    for n in region["names"]:
        insert_into_table(cn, "region_names", region["id"], n["language"]["name"], n["name"])
    print(f"+ FW region {id} done")
    errorSet.remove(f"region {id}")


async def fw_missing_locations():
    info("fw missing regions")
    ids = []
    for item in errorSet:
        if item.startswith("location"):
            id = int(item[9:])
            ids.append(id)
    
    await asyncio.gather(*(fw_missing_location(id, urljoin(API_BASE, f"location/{id}/")) for id in ids))

async def fw_missing_location(id: int, url: str):
    resp = requests.get(url)
    if not resp.ok:
        print(f"- FW location {id} failed!!!")
        return
    location = json(resp.content)
    # table location
    if "region" in location and location["region"]:
        insert_into_table(cn, "location", location["id"], location["name"], get_id(location["region"]["url"]))
    else:
        insert_into_table(cn, "location", location["id"], location["name"], None)
    # location_names
    for n in location["names"]:
        insert_into_table(cn, "location_names", location["id"], n["language"]["name"], n["name"])
    print(f"+ FW location {id} done")
    errorSet.remove(f"location {id}")
    
async def fw_move(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    # NOTE since there are a lot of entries of move that cannot get from aiopokeapi and need to use my function (slow), we
    # only do limited cheek here
    if query_mul_table_id_existence(f"id={id}", "move"):
        print(f"- move {id} already exists")
        return
    try:
        move = await client.get_move(id)
    except:
        try:
            move = await client.get_move(name)
        except:
            errorSet.add(f"move {id}")
            return
    # move
    insert_into_table(cn, "move", move.id, move.name, move.power, move.accuracy, move.pp, move.priority, move.generation.name, move.type.id, move.damage_class.id)
    # move_effects
    for e in move.effect_entries:
        insert_into_table(cn, "move_effects", move.id, e.language.name, e.effect, e.short_effect)
    # move_names
    for n in move.names:
        insert_into_table(cn, "move_names", move.id, n.language.name, n.name)
    # move_flavor_text
    for f in move.flavor_text_entries:
        insert_into_table(cn, "move_flavor_text", move.id, f.language.name, f.flavor_text, f.version_group.id)
    print(f"+ FW move {id} done")

async def fw_missing_moves():
    info("fw missing moves")
    ids = []
    for item in errorSet:
        if item.startswith("move"):
            id = int(item[5:])
            ids.append(id)
    
    await asyncio.gather(*(fw_missing_move(id, urljoin(API_BASE, f"move/{id}/")) for id in ids))

async def fw_missing_move(id: int, url: str):
    resp = requests.get(url)
    if not resp.ok:
        print(f"- FW move {id} failed!!!")
        return
    move = json(resp.content)
    # move
    insert_into_table(cn, "move", move["id"], move["name"], move["power"], move["accuracy"], move["pp"], move["priority"], move["generation"]["name"], get_id(move["type"]["url"]), get_id(move["damage_class"]["url"]))
    # move_effects
    for e in move["effect_entries"]:
        insert_into_table(cn, "move_effects", move["id"], e["language"]["name"], e["effect"], e["short_effect"])
    # move_names
    for n in move["names"]:
        insert_into_table(cn, "move_names", move["id"], n["language"]["name"], n["name"])
    # move_flavor_text
    for f in move["flavor_text_entries"]:
        insert_into_table(cn, "move_flavor_text", move["id"], f["language"]["name"], f["flavor_text"], get_id(f["version_group"]["url"]))
    print(f"+ FW move {id} done")
    errorSet.remove(f"move {id}")

async def fw_pokemon(client: AiopokeClient, id_name: tuple):
    id = id_name[0]
    name = id_name[1]
    if query_mul_table_id_existence(f"id={id}", "pokemon") and query_mul_table_id_existence(f"pokemon_id={id}", "pokemon_stats"):
        print(f"- pokemon {id} already exists")
        return
    try:
        pokemon = await client.get_pokemon(id)
    except:
        try:
            pokemon = await client.get_pokemon(name)
        except:
            errorSet.add(f"pokemon {id}")
            return
    # pokemon

    sp = lambda s: s.url if s is not None else None
    sprites = pokemon.sprites
    insert_into_table(cn, "pokemon", pokemon.id, pokemon.name, pokemon.order, pokemon.height, pokemon.weight, pokemon.base_experience, sp(sprites.front_default), sp(sprites.front_female), sp(sprites.front_shiny), sp(sprites.front_shiny_female), sp(sprites.back_default), sp(sprites.back_female), sp(sprites.back_shiny), sp(sprites.back_shiny_female), pokemon.species.id)
    # pokemon_types
    for t in pokemon.types:
        insert_into_table(cn, "pokemon_types", pokemon.id, t.type.id)
    # pokemon_abilities
    for a in pokemon.abilities:
        insert_into_table(cn, "pokemon_abilities", pokemon.id, a.ability.id, a.is_hidden)
    # pokemon_forms
    for f in pokemon.forms:
        insert_into_table(cn, "pokemon_forms", pokemon.id, f.name)
    # pokemon_game_indices
    for g in pokemon.game_indices:
        insert_into_table(cn, "pokemon_game_indices", pokemon.id, g.version.id, g.game_index)
    # pokemon_hold_items
    for t in pokemon.held_items:
        insert_into_table(cn, "pokemon_held_items", pokemon.id, t.item.id)
    # pokemon_moves
    for m in pokemon.moves:
        for game_group in m.version_group_details:
            insert_into_table(cn, "pokemon_moves", pokemon.id, m.move.id, game_group.version_group.id, game_group.level_learned_at, game_group.move_learn_method.name)
    # pokemon_stats
    for s in pokemon.stats:
        insert_into_table(cn, "pokemon_stats", pokemon.id, s.stat.id, s.base_stat, s.effort)
    print(f"+ FW pokemon {id} done")

async def main():
    # await fw_all_stats()
    client = aiopoke.AiopokeClient()
    
    # await fw_all_stats(client)
    # await fw_all_game_groups(client)
    # await fw_all_games(client)
    # await fw_all_egg_groups(client)
    # await fw_all_species(client) # NOTE after egg_group and game
    # await fw_all_move_damage_classes(client)
    # await fw_all_abilities(client) # NOTE: after game_group
    # await fw_all_types(client) 
    # await fw_all_items(client) 
    # await fw_all_moves(client) # NOTE after type, move_damage_class and game_group
    await fw_all_pokemons(client) # NOTE after species, type, ability, game, item, move, game_group and stat

    # await fw_all_regions(client) 
    # print(errorSet)
    # await fw_all_locations(client) 
    # print(errorSet)
    # await fw_all_areas(client) 
    # print(errorSet)

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
