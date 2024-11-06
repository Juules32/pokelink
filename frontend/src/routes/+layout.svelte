<script lang="ts">
    import BackgroundComponent from "$components/BackgroundComponent.svelte";
    import HeaderComponent from "$components/HeaderComponent.svelte";
    import { onMount } from "svelte";
    import "../app.css";
    import { graphData, pokemonNodes } from "$lib/globals";
    import { fetchGraphData } from "$lib/backend";
    import type { GraphData } from "$lib/interfaces";
    
    interface Props {
        children?: import('svelte').Snippet;
    }
    let { children }: Props = $props();
    
    async function getGraphData(): Promise<GraphData> {
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

    let loaded = $state(false);
    onMount(async () => {
        $graphData = await getGraphData()
        $pokemonNodes = Object.values($graphData.nodes)

        loaded = true;
    });
</script>

{#if loaded}
    <BackgroundComponent />
    <HeaderComponent />
    {@render children?.()}
{/if}
