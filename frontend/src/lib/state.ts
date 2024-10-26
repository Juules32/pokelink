import type { PokemonNode, GraphData } from "$lib/interfaces";
import { fetchGraphData } from "./backend";
import { browser } from '$app/environment'

async function getGraphData(): Promise<GraphData> {
    if (browser) {
        const localGraphDataJson = localStorage.getItem("graphData")
        if (localGraphDataJson) {
            console.log("Loaded graph data from local storage")
            const localGraphData: GraphData = JSON.parse(localGraphDataJson)
            return localGraphData
        }
        else {
            console.log("Loaded graph data from backend")
            const generatedGraphData = await fetchGraphData()
            localStorage.setItem("graphData", JSON.stringify(generatedGraphData))
            return generatedGraphData
        }
    }
    else {
        // Should never happen 🤡
        return await fetchGraphData()
    }
}

export const graphData: GraphData = await getGraphData()
export const pokemonNodes: PokemonNode[] = Object.values(graphData.nodes)
export const edges = graphData.edges
