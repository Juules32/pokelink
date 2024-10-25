<script lang="ts">
    import { base } from "$app/paths";
import ArrowComponent from "./ArrowComponent.svelte";
import ModalComponent from "./ModalComponent.svelte";
    import NodeComponent from "./NodeComponent.svelte";

    interface Props {
        showTutorial: boolean,
    }
	let { showTutorial = $bindable() } : Props = $props();
</script>

<ModalComponent bind:showModal={showTutorial}>
    <!-- Header -->
	{#snippet header()}
		<h2>Welcome to PokéLink!</h2>
	{/snippet}

    <!-- Children -->
    <div class="leading-5 py-2 space-y-4">
        <p>
            The goal of this daily puzzle game is to go from one pokémon to another
            in the shortest possible distance.
        </p>
        <p>The rules for going from one pokémon to another are as follows:</p>
        <ol class="list-decimal list-inside space-y-4">
            <li>The two pokemon must have one or more types in common. </li>
            <li>
                The two pokemon must be from the same or adjacent regions,
                adjacent meaning the previous or the next pokémon region.    
            </li>
        </ol>
        <p>Here are some examples that illustrate the rules:</p>
        <div class="flex justify-center items-center">
            <NodeComponent pokemonName="bulbasaur" />
            <ArrowComponent />
            <NodeComponent pokemonName="celebi" />
        </div>
        <p>
            Bulbasaur to Celebi is <span class="text-green-600">allowed</span>
            because they have <img src="{base}/types/grass.png" class="inline-block" alt="grass"/>
            in common and Kanto is adjacent to Johto.
        </p>
        <div class="flex justify-center items-center">
            <NodeComponent pokemonName="onix" />
            <p style="min-width: {20}px;" class="text-lg text-center relative text-red-600">x</p>
            <NodeComponent pokemonName="charmander" />
        </div>
        <p>
            Onix to Charmander is <span class="text-red-600">not allowed</span> 
            because although they are from the same region, they don't share a type.
        </p>
        <div class="flex justify-center items-center">
            <NodeComponent pokemonName="dewgong" />
            <p style="min-width: {20}px;" class="text-lg text-center relative text-red-600">x</p>
            <NodeComponent pokemonName="spheal" />
        </div>
        <p>
            Dewgong to Spheal is <span class="text-red-600">not allowed</span> 
            because although they share a type, they're from neither the same or adjacent regions.
        </p>
        <p>Tip: Hovering over a pokemon shows its region</p>
        <p>Good luck!</p>
    </div>
</ModalComponent>
