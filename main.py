# NOTE: Pokemon id >= 10001 is the one variant (from) of the origin Pokemon
import asyncio
from json import loads as json
from urllib.parse import urljoin
import requests
import threading

API_BASE = "https://pokeapi.co/api/v2/"
ALL_POKEMONS_LIST_URL = urljoin(API_BASE, "pokemon?limit={limit}&offset=0")

pokemons = []

def fetch_pokemon_list(limit: int) -> dict:
    resp = requests.get(ALL_POKEMONS_LIST_URL.format(limit=limit))
    resp.raise_for_status()
    return json(resp.content)

def fetch_pokemon_information(url: str) -> bool:
    resp = requests.get(url)
    if not resp.ok:
        return False
    return True

async def main():
    pokemon_list_res = fetch_pokemon_list(1010)["results"]
    res = await asyncio.gather(*())
    return res

if __name__ == "__main__":
    asyncio.run(main())
