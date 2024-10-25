<script lang="ts">
    import ModalComponent from "./ModalComponent.svelte";

    interface Props {
        showTutorial: boolean,
    }
	let { showTutorial = $bindable() } : Props = $props();
</script>

<ModalComponent bind:showModal={showTutorial}>
    <!-- Header -->
	{#snippet header()}
		<h2>
			modal
			<small><em>adjective</em> mod·al ˈmō-dəl\</small>
		</h2>
	{/snippet}

    <!-- Children -->
    <p>Hey!</p>
</ModalComponent>
