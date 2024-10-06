from typing import Mapping
import networkx as nx
# import matplotlib.pyplot as plt
import json
from networkx import Graph
from db import db
import pickle

def pokemon_data_to_graph() -> tuple[Graph, Mapping]:
    G = nx.Graph()

    # Get data files
    with open("pokemon_data.json", "r") as pokemon_data_json:
        pokemon_data: dict = json.load(pokemon_data_json)
    
    # Add nodes
    for k, v in pokemon_data.items():
        G.add_node(k, types=v["types"], region=v["region"])
    
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
                if not itypes.isdisjoint(jtypes):
                    G.add_edge(ik, jk, connection="Share a type")

            elif {iregion, jregion} in connected_regions:
                # If the two pokemon share exactly the same types
                if itypes == jtypes:
                    G.add_edge(ik, jk, connection="Same type(s) across generations")
    
    # Generate layout (node positions)
    pos = nx.spring_layout(G, iterations=200, k=0.1)

    return (G, pos)

def store_graph():
    graph_data = pokemon_data_to_graph()
    with open("graph_data.pkl", "wb") as graph_file:
        pickle.dump(graph_data, graph_file)

def get_graph() -> tuple[Graph, Mapping]:
    with open("graph_data.pkl", "rb") as graph_file:
        return pickle.load(graph_file)

def store_graph_json(G: Graph, pos: Mapping, store_to_db: bool = False, store_to_file: bool = False):

    # Format graph data
    graph_data = {
        "nodes": [{
            "name": k, 
            "types": v.get("types"), 
            "region": v.get("region"), 
            "pos": list(pos[k])
        } for k, v in G.nodes.items()],
        "edges": [{
            "source": source, 
            "target": target,
            "connection": v.get("connection")
        } for (source, target), v in G.edges.items()]
    }

    # Show graph
    # nx.draw(G, with_labels=True, pos=pos)
    # plt.show()

    if store_to_db:
        db.set_graph(data=graph_data)

    if store_to_file:
        with open("graph_data.json", "w") as graph_data_json:
            json.dump(graph_data, graph_data_json, indent=4)

if __name__ == "__main__":
    # store_graph()
    G, pos = get_graph()
    store_graph_json(G, pos, store_to_db=True, store_to_file=True)
