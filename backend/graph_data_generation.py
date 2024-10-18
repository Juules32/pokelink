from typing import Mapping, Union
import networkx as nx
import json
from networkx import Graph
import pickle

def types_in_common(itypes: set[str], jtypes: set[str]) -> bool:
    return not itypes.isdisjoint(jtypes)

def generate_graph() -> Graph:
    # Init an empty graph
    G = nx.Graph()

    # Get data files
    with open("pokemon_data.json", "r") as pokemon_data_json:
        pokemon_data: dict = json.load(pokemon_data_json)

        # Filter out pokemon from Hisui 💀
        pokemon_data = {k: v for k, v in pokemon_data.items() if v["region"] != 'hisui'}

    # Add nodes
    for k, v in pokemon_data.items():
        G.add_node(k, types=v["types"], region=v["region"])
    
    # 'Bridges' between generations
    connected_regions: set[frozenset[str]] = {
        frozenset({"kanto", "johto"}),
        frozenset({"johto", "hoenn"}),
        frozenset({"hoenn", "sinnoh"}),
        frozenset({"sinnoh", "unova"}),
        frozenset({"unova", "kalos"}),
        frozenset({"kalos", "alola"}),
        frozenset({"alola", "galar"}),
        frozenset({"galar", "paldea"})
    }

    # Add edges
    pokemon_items = list(pokemon_data.items())
    for i in range(len(pokemon_items)):
        ik, iv = pokemon_items[i]
        itypes = set(iv["types"])
        iregion = iv["region"]
        
        for j in range(i + 1, len(pokemon_items)):
            jk, jv = pokemon_items[j]
            jtypes = set(jv["types"])
            jregion = jv["region"]

            if iregion == jregion:
                # If the two pokemon have types in common
                if types_in_common(itypes, jtypes):
                    G.add_edge(ik, jk, connection="Share a type")

            elif {iregion, jregion} in connected_regions:
                # If the two pokemon share exactly the same types
                if itypes == jtypes:
                    G.add_edge(ik, jk, connection="Same type(s) across generations")
    
    return G

# Generate positional data for each node based on Fruchterman-Reingold force-directed algorithm
def generate_pos(G: Graph, iterations: int = 50, k: Union[int, None] = None) -> Mapping:
    return nx.spring_layout(G, iterations=iterations, k=k)

def dump_graph(G: Graph):
    with open("graph_data.pkl", "wb") as graph_file:
        pickle.dump(G, graph_file)

def load_graph() -> Graph:
    with open("graph_data.pkl", "rb") as graph_file:
        return pickle.load(graph_file)

def store_graph_json(G: Graph):

    # Format graph data
    graph_data = {
        "nodes": [{
            "name": k, 
            "types": v.get("types"), 
            "region": v.get("region"), 
        } for k, v in G.nodes.items()],
        "edges": [{
            "source": source, 
            "target": target,
            "connection": v.get("connection")
        } for (source, target), v in G.edges.items()]
    }

    with open("graph_data.json", "w") as graph_data_json:
        json.dump(graph_data, graph_data_json, indent=4)

if __name__ == "__main__":
    dump_graph(generate_graph())

    # The graph data is unpickled
    G = load_graph()

    # The graph data is saved to the database and/or a file
    store_graph_json(G)
