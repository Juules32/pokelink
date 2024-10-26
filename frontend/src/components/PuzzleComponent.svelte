<script lang="ts">
    import { fetchHint } from "$lib/backend";
    import { edges, graphData, pokemonNodes } from "$lib/state";
    import GraphComponent from "./GraphComponent.svelte";
    import SearchComponent from "./SearchComponent.svelte";
    import type { PokemonNode, Puzzle } from "$lib/interfaces";
    import NodeComponent from "./NodeComponent.svelte";
    import ArrowComponent from "./ArrowComponent.svelte";
    import { dev } from "$app/environment";

    interface Props {
        date: string | undefined;
        puzzle: Puzzle;
    }
    let { date, puzzle }: Props = $props();

    let guessedNodes: PokemonNode[] = $state([]);
    let hint: string | undefined = $state();
    const latestGuessNode = $derived(guessedNodes.at(-1));

    async function addHint() {
        if (latestGuessNode) {
            hint = await fetchHint(latestGuessNode.name, puzzle.target);
        }
    }

    function tryGuess(name: string) {
        if (latestGuessNode) {
            if (edges[latestGuessNode.name].includes(name)) {
                hint = undefined;
                addNode(name);
            }
        }
    }

    function addNode(guess: string) {
        const newNode = graphData.nodes[guess];
        guessedNodes = [...guessedNodes, newNode];
        if (puzzle.target == guess) {
            console.log("You win!");
        }
    }

    addNode(puzzle.source);
</script>

{#if dev}
    <button
        class="w-[128px] absolute left-0 text-center"
        onclick={() => addNode(
            pokemonNodes[Math.floor(Math.random() * pokemonNodes.length)].name
        )}
    >
        Add Random Pokemon
    </button>
{/if}

<div class="h-fit flex flex-col pt-12 space-y-5 items-center">
    <h1 class="text-5xl">{date ? "Puzzle: " + date : "Today's Puzzle"}</h1>
    <div class="flex items-center">
        <NodeComponent pokemonName={puzzle.source} />
        <ArrowComponent />
        <NodeComponent pokemonName={puzzle.target} />
    </div>

    <div class="flex w-full justify-center space-x-2">
        <div class="w-[80px]"></div>
        <SearchComponent {tryGuess} />
        <button
            onclick={addHint}
            class="bg-red-400 w-[80px] rounded-lg border-black border-2"
        >
            Hint?
        </button>
    </div>
    <GraphComponent graphNodes={guessedNodes} {hint} />

    {#if latestGuessNode?.name == puzzle.target}
        <h2 class="text-3xl">Shortest path</h2>
        <GraphComponent
            graphNodes={puzzle.shortestPath.map(
                (name) => graphData.nodes[name]
            )}
            hint={undefined}
        />
    {/if}
</div>
