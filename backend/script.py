import httpx
from business import Business

bn = Business()

for k, v in bn.graph_data.nodes.items():
    res = httpx.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{v.id}.png")
    print(res)