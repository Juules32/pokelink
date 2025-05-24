from typing import Mapping, Optional
import networkx as nx
import json, pickle
from networkx import Graph
from util import types_in_common
from model import GraphData, PokemonNode
from fastapi.encoders import jsonable_encoder

def generate_graph() -> Graph:
    # Init an empty graph
    graph = nx.Graph()

    # Get data files
    with open("data/pokemon_data.json", "r") as pokemon_data_json:
        pokemon_data: dict = json.load(pokemon_data_json)

        # Filter out pokemon from Hisui 💀
        pokemon_data = {k: v for k, v in pokemon_data.items() if v["region"] != 'hisui'}

    # Add nodes
    for k, v in pokemon_data.items():
        graph.add_node(k, id=v["id"], types=v["types"], region=v["region"])
    
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

            # If the two pokemon are from the same or connected regions
            if iregion == jregion or {iregion, jregion} in connected_regions:
                # If the two pokemon have types in common
                if types_in_common(itypes, jtypes):
                    graph.add_edge(ik, jk)
    return graph

# Generate positional data for each node based on Fruchterman-Reingold force-directed algorithm
def generate_pos(graph: Graph, iterations: int = 50, k: Optional[int] = None) -> Mapping:
    return nx.spring_layout(graph, iterations=iterations, k=k)

def dump_graph(graph: Graph):
    with open("data/graph.pkl", "wb") as graph_file:
        pickle.dump(graph, graph_file)

def load_graph() -> Graph:
    with open("data/graph.pkl", "rb") as graph_file:
        return pickle.load(graph_file)

def generate_graph_data(graph: Graph) -> GraphData:
    nodes: dict[str, PokemonNode] = {}
    edges: dict[str, list[str]] = {}
    for name, values in graph.nodes.items():
        nodes[name] = PokemonNode(
            name=name,
            id=values.get("id"),
            types=values.get("types"),
            region=values.get("region")
        )
        edges[name] = list(graph.neighbors(name))

    return GraphData(
        nodes=nodes,
        edges=edges
    )

def store_graph_data(graph_data: GraphData) -> None:
    with open("data/graph_data.json", "w") as graph_data_json:
        json.dump(jsonable_encoder(graph_data), graph_data_json, indent=4)

if __name__ == "__main__":
    # Generate and pickle the graph to a file
    dump_graph(generate_graph())

    # The graph is unpickled
    graph = load_graph()

    # The graph data is formatted from the graph
    graph_data = generate_graph_data(graph)

    # The graph data is saved to a json file
    store_graph_data(graph_data)
