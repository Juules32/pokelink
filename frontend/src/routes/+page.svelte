<script lang="ts">
    import { onMount } from "svelte";
    import PuzzleComponent from "$components/PuzzleComponent.svelte";
    import BackgroundComponent from "$components/BackgroundComponent.svelte";
    import HeaderComponent from "$components/HeaderComponent.svelte";

    let loaded = false;
    onMount(() => {
        loaded = true;
    });
</script>

{#if loaded}
    <BackgroundComponent />
    <HeaderComponent />
    <PuzzleComponent />
{/if}
