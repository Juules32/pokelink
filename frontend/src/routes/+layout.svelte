<script lang="ts">
    import BackgroundComponent from "$components/BackgroundComponent.svelte";
    import HeaderComponent from "$components/HeaderComponent.svelte";
    import { onMount } from "svelte";
    import "../app.css";
    
    let loaded = false;
    onMount(() => {
        loaded = true;
    });
</script>

{#if loaded}
    <BackgroundComponent />
    <HeaderComponent />
    <slot />
{/if}
