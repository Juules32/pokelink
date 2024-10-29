<script lang="ts">
    import BackgroundComponent from "$components/BackgroundComponent.svelte";
    import HeaderComponent from "$components/HeaderComponent.svelte";
    import { onMount } from "svelte";
    import "../app.css";
    import { edges, getGraphData, graphData, pokemonNodes } from "$lib/state";
    
    interface Props {
        children?: import('svelte').Snippet;
    }

    let { children }: Props = $props();
    
    let loaded = $state(false);
    onMount(async () => {
        $graphData = await getGraphData()
        $pokemonNodes = Object.values($graphData.nodes)
        $edges = $graphData.edges

        loaded = true;
    });
</script>

{#if loaded}
    <BackgroundComponent />
    <HeaderComponent />
    {@render children?.()}
{/if}
