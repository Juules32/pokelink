import asyncio
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

async def fetch_pokemon_data(client, result, pokemon_data):
    # Ignores specific pokemon
    if not is_name_legal(result["name"]):
        return
    
    # Fetch pokemon details asynchronously
    pokemon_response = await client.get(result["url"])
    pokemon_response = pokemon_response.json()
    pokemon_id = pokemon_response["id"]
    pokemon_name = pokemon_response["name"]

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

    # Store data
    pokemon_data[pokemon_name] = {
        "id": pokemon_id,
        "types": pokemon_types,
        "region": pokemon_region
    }

async def save_data_to_json():
    pokemon_data = {}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")
        response = response.json()["results"]

        # Create a list of tasks to fetch all pokemon data concurrently
        tasks = [
            fetch_pokemon_data(client, result, pokemon_data)
            for result in response
        ]

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

    # Save the data to JSON files
    with open("pokemon_data.json", "w") as pokemon_data_json:
        json.dump(pokemon_data, pokemon_data_json, indent=4)

# Running this script gathers pokemon data asynchronously and stores it in json format
if __name__ == "__main__":
    asyncio.run(save_data_to_json())
