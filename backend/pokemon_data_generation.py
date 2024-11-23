import asyncio
from collections import defaultdict
import pickle
import httpx
import json

def is_name_legal(name):
    return not (
        "rockruff-" in name or
        "cramorant-" in name or
        "greninja-" in name or
        "-totem" in name or
        "zarude-dada" in name or                            # No sprite
        "morpeko-hangry" in name or                         # No sprite
        ("miraidon-" in name and name != "miraidon") or     # No sprite
        ("koraidon-" in name and name != "koraidon") or     # No sprite
        ("zygarde-" in name and name != "zygarde-50") or
        ("pikachu-" in name and name != "pikachu-gmax") or
        ("eevee-" in name and name != "eevee-gmax")
    )

regions = [
    "kanto",
    "johto",
    "hoenn",
    "sinnoh",
    "unova",
    "kalos",
    "alola",
    "galar",
    "paldea",
    "hisui"
]

region_number: dict[str, int] = {
    "kanto": 1,
    "johto": 2,
    "hoenn": 3,
    "sinnoh": 4,
    "unova": 5,
    "kalos": 6,
    "alola": 7,
    "galar": 8,
    "paldea": 9,
    "hisui": -1     # Hisui is excluded (for now)
}

generation_to_region = {
    "generation-i": "kanto",
    "generation-ii": "johto",
    "generation-iii": "hoenn",
    "generation-iv": "sinnoh",
    "generation-v": "unova",
    "generation-vi": "kalos",
    "generation-vii": "alola",
    "generation-viii": "galar",
    "generation-ix": "paldea"
}

def find_region(name, species_generation):
    # Handle exceptions
    if name == "wyrdeer": return "hisui"
    if name == "kleavor": return "hisui"
    if name == "overqwil": return "hisui"
    if name == "ursaluna": return "hisui"
    if name == "sneasler": return "hisui"
    if name == "enamorus": return "hisui"
    if name == "basculin-white-striped": return "hisui"
    if name == "ursaluna-bloodmoon": return "paldea"
    if "-alola" in name: return "alola"
    if "-galar" in name: return "galar"
    if "-hisui" in name: return "hisui"
    if "-paldea" in name: return "paldea"
    if "basculegion" in name: return "hisui"

    # Default to generation's region
    return generation_to_region[species_generation]

def get_real_pokemon_name(pokemon_name: str) -> str:
    # Pokemon that either have '-' in their name
    # Or that have different names than what pokeAPI says
    exceptions: dict = {
        "porygon-z": "porygon-z",
        "wo-chien": "wo-chien",
        "chi-yu": "chi-yu",
        "chien-pao": "chien-pao",
        "ting-lu": "ting-lu",
        "ho-oh": "ho-oh",
        "jangmo-o": "jangmo-o",
        "hakamo-o": "hakamo-o",
        "kommo-o": "kommo-o",
        "nidoran-m": "nidoran♂",
        "nidoran-f": "nidoran♀",
        "basculin-blue-striped": "basculin blue-striped",
        "basculin-red-striped": "basculin red-striped",
        "basculin-white-striped": "basculin white-striped",
        "dudunsparce-two-segment": "dudunsparce two-segment",
        "dudunsparce-three-segment": "dudunsparce three-segment",
        "mr-mime": "mr. mime",
        "mr-mime-galar": "mr. mime galar",
        "mr-rime": "mr. rime",
        "mime-jr": "mime jr.",
        "type-null": "type: null",
        "farfetchd": "farfetch'd"
    }
    
    exception_name = exceptions.get(pokemon_name)
    if exception_name:
        return exception_name
    else:
        return pokemon_name.replace("-", " ")

async def fetch_pokemon_data(client, result, pokemon_data, criteria_data):
    # Ignores specific pokemon
    if not is_name_legal(result["name"]):
        return
    
    # Fetch pokemon details asynchronously
    pokemon_response = await client.get(result["url"])
    pokemon_response = pokemon_response.json()
    pokemon_id: int = pokemon_response["id"]
    pokemon_name: str = pokemon_response["name"]

    print(f"Generating data for: {pokemon_name} (id {pokemon_id})")
    
    # Types
    pokemon_types = []
    for type_entry in pokemon_response["types"]:
        pokemon_type = type_entry["type"]["name"]
        pokemon_types.append(pokemon_type)
    
    # Pokemon-species
    species_url = pokemon_response["species"]["url"]
    species_data = await client.get(species_url)
    species_data = species_data.json()

    # Region
    species_generation = species_data["generation"]["name"]
    pokemon_region = find_region(pokemon_name, species_generation)

    # Pokédex number
    pokedex_number = species_data["pokedex_numbers"][0]["entry_number"]

    pokemon_name = get_real_pokemon_name(pokemon_name)

    # Store data
    pokemon_data[pokemon_name] = {
        "id": pokemon_id,
        "types": pokemon_types,
        "region": pokemon_region,
        "pokedex": pokedex_number
    }

    def add(criterion, name):
        criteria_data[criterion].append(name)

    # Popular moves
    popular_moves = ["stomp", "fly", "bite"]
    move_names = [pokemon_response["move"]["name"] for pokemon_response in pokemon_response["moves"]]
    for popular_move in popular_moves:
        if popular_move in move_names:
            add(f"knows-{popular_move}", pokemon_name)

    # Types
    if len(pokemon_types) == 1:
        add("mono-type", pokemon_name)
    if len(pokemon_types) == 2:
        add("dual-type", pokemon_name)
    for type in pokemon_types:
        add(f"type-{type}", pokemon_name)
    
    # Special types of pokemon
    if "-mega" in pokemon_name:
        add("mega", pokemon_name)
    if "-gmax" in pokemon_name:
        add("gmax", pokemon_name)
    
    # Pokemon-species
    # Special types of pokemon
    if species_data["is_baby"]:
        add("baby", pokemon_name)
    if species_data["is_legendary"]:
        add("legendary", pokemon_name)
    if species_data["is_mythical"]:
        add("mythical", pokemon_name)
    
    # Region
    add(f'region-{pokemon_region}', pokemon_name)

def dump_criteria_data(criteria_data: dict):
    with open("criteria_data.pkl", "wb") as criteria_file:
        pickle.dump(dict(criteria_data.items()), criteria_file)

def load_criteria_data() -> dict:
    with open("criteria_data.pkl", "rb") as criteria_file:
        return pickle.load(criteria_file)

LIMIT = 100000
OFFSET = 0

async def generate_pokemon_and_criteria_data() -> tuple[dict, dict]:
    pokemon_data = {}
    criteria_data = defaultdict(lambda : [])

    criteria_data["fossil"] = [
        "omanyte", "omastar", "kabuto", "kabutops", "aerodactyl", "aerodactyl-mega", "lileep", "cradily", "anorith", "armaldo", "cranidos", "rampardos", "shieldon", "bastiodon", "tirtouga", "carracosta", "archen", "archeops", "genesect", "tyrunt", "tyrantrum", "amaura", "aurorus", "dracozolt", "arctozolt", "dracovish", "arctovish"
    ]
    criteria_data["starter"] = [
        "bulbasaur", "charmander", "squirtle", "chikorita", "cyndaquil", "totodile", "treecko", "torchic", "mudkip", "turtwig", "chimchar", "piplup", "snivy", "tepig", "oshawott", "chespin", "fennekin", "froakie", "rowlet", "litten", "popplio", "grookey", "scorbunny", "sobble", "sprigatito", "fuecoco", "quaxly", "pikachu", "eevee"
    ]
    criteria_data["ultra-beast"] = [
        "nihilego", "buzzwole", "pheromosa", "xurkitree", "celesteela", "kartana", "guzzlord", "necrozma", "poipole", "naganadel", "stakataka", "blacephalon"
    ]
    criteria_data["paradox"] = [
        "great-tusk", "scream-tail", "brute-bonnet", "flutter-mane", "slither-wing", "sandy-shocks", "roaring-moon", "koraidon", "walking-wake", "raging-bolt", "gouging-fire", "iron-treads", "iron-bundle", "iron-hands", "iron-jugulis", "iron-moth", "iron-thorns", "iron-valiant", "miraidon", "iron-leaves", "iron-crown", "iron-boulder"
    ]

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"https://pokeapi.co/api/v2/pokemon?limit={LIMIT}&offset={OFFSET}")
        response = response.json()["results"]

        # Create a list of tasks to fetch all pokemon data concurrently
        tasks = [
            fetch_pokemon_data(client, result, pokemon_data, criteria_data)
            for result in response
        ]

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

    return (pokemon_data, criteria_data)


# Running this script gathers pokemon data asynchronously and stores it in json format
if __name__ == "__main__":
    pokemon_data, criteria_data = asyncio.run(generate_pokemon_and_criteria_data())
    
    # Save the data to JSON files
    with open("pokemon_data.json", "w") as pokemon_data_json:
        json.dump(pokemon_data, pokemon_data_json, indent=4)
    
    with open("criteria_data.json", "w") as criteria_data_json:
        json.dump(criteria_data, criteria_data_json, indent=4)

    dump_criteria_data(criteria_data)
