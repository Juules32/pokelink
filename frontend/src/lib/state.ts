import type { PokemonNode, Puzzle, GraphData } from "$lib/interfaces";
import { get, writable } from 'svelte/store';
import { fetchGraphData } from "./backend";
import { browser } from '$app/environment'

export const puzzle = writable<Puzzle>();

export const guessedNodes = writable<PokemonNode[]>([]);

export const validGuesses = writable<PokemonNode[]>([]);

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

export function getPokemonNode(name: string): PokemonNode {
    return graphData.nodes[name]
}

export function addNode(guess: string) {
    const newNode = getPokemonNode(guess)
    guessedNodes.update((nodes) => [...nodes, newNode]);
    if (get(puzzle).target == guess) {
        console.log("You win!")
    }
}
