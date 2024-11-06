<script lang="ts">
    import { fetchHint, postSolution } from "$lib/backend";
    import { edges, pokemonNodes } from "$lib/state";
    import GraphComponent from "./GraphComponent.svelte";
    import SearchComponent from "./SearchComponent.svelte";
    import type { PuzzleSolution } from "$lib/interfaces";
    import NodeComponent from "./NodeComponent.svelte";
    import ArrowComponent from "./ArrowComponent.svelte";
    import { dev } from "$app/environment";
    import { confetti } from "@neoconfetti/svelte";
    import { onMount } from "svelte";
    import { page } from "$app/stores";

    interface Props {
        puzzleSolution: PuzzleSolution;
    }
    let { puzzleSolution }: Props = $props();

    const puzzle = puzzleSolution.puzzle

    let guessedNames: string[] = $state(puzzleSolution.solution || getLocalGuesses());
    let hint: string | undefined = $state();
    const latestGuessName = $derived(guessedNames.at(-1));

    async function addHint() {
        if (latestGuessName) {
            hint = await fetchHint(latestGuessName, puzzle.target);
        }
    }

    function getLocalGuesses(): string[] {
        const localGuessesJson = localStorage.getItem(`puzzle-${puzzle.date}`)
        if (localGuessesJson) {
            console.log("Loaded guesses from local storage")
            const parsedLocalGuesses = JSON.parse(localGuessesJson)
            if (!parsedLocalGuesses.length || parsedLocalGuesses[0] != puzzle.source) {
                localStorage.removeItem(`puzzle-${puzzle.date}`)
                console.log("Invalid local guessed found, deleted local guesses")
                return []
            }
            
            return parsedLocalGuesses
        }
        else {
            return []
        }
    }

    function setLocalGuesses() {
        localStorage.setItem(`puzzle-${puzzle.date}`, JSON.stringify(guessedNames))
    }

    function tryGuess(name: string) {
        if (latestGuessName && $edges[latestGuessName].includes(name)) {
            addNode(name);
        }
    }

    function addNode(guess: string) {
        if (won) {
            console.log("Can't guess when you have already completed this puzzle")
            return
        }

        hint = undefined;
        guessedNames = [...guessedNames, guess];
        setLocalGuesses()
        if (puzzle.target == guess) {
            console.log("You win!");
            postSolution(puzzle.date, guessedNames).catch((err) => {
                localStorage.removeItem(`puzzle-${puzzle.date}`);
                guessedNames = [puzzle.source]
                alert(err)
            });
        }
    }

    onMount(() => {
        if (!guessedNames.length) {
            console.log("Adding puzzle source to guesses")
            addNode(puzzle.source);
        }
    })

    let won = $derived(puzzleSolution.solution || latestGuessName == puzzle.target);
    let numGuesses = $derived(guessedNames.length - 1)
</script>

{#if dev}
    <button
        class="w-[128px] absolute left-0 text-center"
        onclick={() => addNode(
            $pokemonNodes[Math.floor(Math.random() * $pokemonNodes.length)].name
        )}
    >
        Add Random Pokemon
    </button>
    <button
        class="w-[128px] absolute left-32 text-center"
        onclick={() => addNode(puzzle.target)}
    >
        Complete Puzzle
    </button>
{/if}

{#if won && !puzzleSolution.solution}
    <div
        style="position: absolute; left: 50%; top: 0%"
        use:confetti={{
            force: 0.7,
            stageWidth: window.innerWidth - 40, // 40 prevents overflow
            stageHeight: window.innerHeight - 16, // 16 prevents overflow
            colors: ["#ff3e00", "#40b3ff", "#676778"]
        }}
    ></div>
{/if}

<div class="h-fit flex flex-col pt-12 space-y-5 items-center">
    <h1 class="sm:text-5xl text-3xl">{$page.params.date ? "Puzzle: " + $page.params.date : "Today's Puzzle"}</h1>
    <div class="flex items-center">
        <NodeComponent pokemonName={puzzle.source} />
        <ArrowComponent />
        <NodeComponent pokemonName={puzzle.target} />
    </div>

    {#if won}
        <h2 class="sm:text-3xl text-xl">Your Solution: {numGuesses} {numGuesses > 1 ? "Guesses" : "Guess"}</h2>
    {:else}
        <div class="flex w-3/4 max-w-[500px] justify-center space-x-2">
            <SearchComponent {tryGuess} />
            <button
                onclick={addHint}
                class="bg-red-400 w-[80px] rounded-lg border-black border-2"
            >
                Hint?
            </button>
        </div>
    {/if}

    <GraphComponent 
        graphNames={guessedNames}
        {hint}
    />

    {#if won}
        <h2 class="sm:text-3xl text-xl">Shortest path: {puzzle.shortestPathLength} {puzzle.shortestPathLength > 1 ? "Guesses" : "Guess"}</h2>
        <GraphComponent
            graphNames={puzzle.shortestPath}
        />
    {/if}
</div>
