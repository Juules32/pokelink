<script lang="ts">
    interface Props {
        showModal: boolean,
        header?: import('svelte').Snippet
        children?: import('svelte').Snippet;
    }
	let { showModal = $bindable(), header, children } : Props = $props();

	let dialog: HTMLDialogElement | undefined = $state();

	$effect(() => {if (showModal) dialog?.showModal()});

    $effect(() => {
        if (dialog && showModal) {
            dialog.scrollTop = 0;
        }
    });
</script>

<!-- eslint-disable-next-line svelte/no-unused-svelte-ignore -->
<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_noninteractive_element_interactions -->
<!-- eslint-disable-next-line svelte/valid-compile -->
<dialog
    class="border-2 border-black rounded-lg w-[500px] max-h-[80%] overflow-y-scroll overflow-x-hidden"
	bind:this={dialog}
	onclose={() => (showModal = false)}
	onclick={(e) => { if (e.target == dialog) dialog.close(); }}
>
	<div class="p-4">
        <div class="text-3xl text-center">
            {@render header?.()}
        </div>
		<hr />
		{@render children?.()}
		<hr />
		<button 
			class="bg-red-400 mt-2 border-2 border-black px-2 py-1 rounded-lg" 
			onclick={() => dialog?.close()}
		>
			Close
		</button>
	</div>
</dialog>

<style scoped>
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
	}
	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}
	@keyframes zoom {
		from {transform: scale(0.95)}
		to {transform: scale(1)}
	}
	dialog[open]::backdrop {
		animation: fade 0.2s ease-out;
	}
	@keyframes fade {
		from {opacity: 0}
		to {opacity: 1}
	}
</style>
