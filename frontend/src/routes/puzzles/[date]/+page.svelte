<script lang="ts">
    import PuzzleComponent from "$components/PuzzleComponent.svelte";

    interface Props {
        data: any;
    }

    let { data }: Props = $props();
</script>

<PuzzleComponent puzzle={data.puzzle} date={data.date}/>
