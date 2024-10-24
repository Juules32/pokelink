<script lang="ts">
    import PuzzleComponent from "$components/PuzzleComponent.svelte";

    export let data;
</script>

<PuzzleComponent puzzle={data.puzzle} date={data.date}/>
