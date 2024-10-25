<script lang="ts">
    import BackgroundComponent from "$components/BackgroundComponent.svelte";
    import HeaderComponent from "$components/HeaderComponent.svelte";
    import { onMount } from "svelte";
    import "../app.css";
    
    interface Props {
        children?: import('svelte').Snippet;
    }

    let { children }: Props = $props();
    
    let loaded = $state(false);
    onMount(() => {
        loaded = true;
    });
</script>

{#if loaded}
    <BackgroundComponent />
    <HeaderComponent />
    {@render children?.()}
{/if}
