from typing import Mapping, Union
import networkx as nx
import json, pickle
from networkx import Graph
from model import GraphData, PokemonNode
from fastapi.encoders import jsonable_encoder

def types_in_common(itypes: set[str], jtypes: set[str]) -> bool:
    return not itypes.isdisjoint(jtypes)

def generate_graph(pokemon_nodes: list[PokemonNode]) -> Graph:
    # Init an empty graph
    graph = nx.Graph()

    for pn in pokemon_nodes:
        graph.add_node(pn.name, id=pn.id, pokedex=pn.pokedex, types=pn.types, region=pn.region)
    
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

    for i in range(len(pokemon_nodes)):
        inode = pokemon_nodes[i]
        itypes = set(inode.types)
        iregion = inode.region
        
        for j in range(i + 1, len(pokemon_nodes)):
            jnode = pokemon_nodes[j]
            jtypes = set(jnode.types)
            jregion = jnode.region

            # If the two pokemon are from the same or connected regions
            if iregion == jregion or {iregion, jregion} in connected_regions:
                # If the two pokemon have types in common
                if types_in_common(itypes, jtypes):
                    graph.add_edge(inode.name, jnode.name)
    return graph

# Generate positional data for each node based on Fruchterman-Reingold force-directed algorithm
def generate_pos(graph: Graph, iterations: int = 50, k: Union[int, None] = None) -> Mapping:
    return nx.spring_layout(graph, iterations=iterations, k=k)

def dump_graph(graph: Graph):
    with open("graph_data.pkl", "wb") as graph_file:
        pickle.dump(graph, graph_file)

def load_graph() -> Graph:
    with open("graph_data.pkl", "rb") as graph_file:
        return pickle.load(graph_file)

def get_graph_data(graph: Graph):
    nodes: dict[str, PokemonNode] = {}
    edges: dict[str, list[str]] = {}
    for name, values in graph.nodes.items():
        nodes[name] = PokemonNode(
            name=name,
            id=values.get("id"),
            pokedex=values.get("pokedex"),
            types=values.get("types"),
            region=values.get("region")
        )
        edges[name] = list(graph.neighbors(name))

    return GraphData(
        nodes=nodes,
        edges=edges
    )

def store_graph_data(graph_data: GraphData):
    with open("graph_data.json", "w") as graph_data_json:
        json.dump(jsonable_encoder(graph_data), graph_data_json, indent=4)

if __name__ == "__main__":
    with open("pokemon_data.json", "r") as pokemon_data_json:
        pokemon_data = json.load(pokemon_data_json)
    pokemon_nodes: list[PokemonNode] = [
        PokemonNode(name=k, id=v["id"], types=v["types"], region=v["region"], pokedex=v["pokedex"])
        for k, v in pokemon_data.items()
    ]

    # Generate and pickle the graph to a file
    dump_graph(generate_graph(pokemon_nodes))

    # The graph is unpickled
    graph = load_graph()

    # The graph data is formatted from the graph
    graph_data = get_graph_data(graph)

    # The graph data is saved to a json file
    store_graph_data(graph_data)
