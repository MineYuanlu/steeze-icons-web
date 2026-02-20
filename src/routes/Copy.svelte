<script lang="ts">
	import { ClipboardDocument, ClipboardDocumentCheck } from '@steeze-ui/heroicons';
	import { Icon } from '@steeze-ui/svelte-icon';

	const { content, name }: { content: string | (() => string); name?: string } = $props();

	let copyHover = $state(false);
	let copyed = $state<number>();

	function copyToClipboard(text: string) {
		const el = document.createElement('textarea');
		el.value = text;
		document.body.appendChild(el);
		el.select();
		document.execCommand('copy');
		document.body.removeChild(el);
		if (copyed !== undefined) clearTimeout(copyed);
		const timer = (copyed = setTimeout(() => {
			if (timer === copyed) copyed = undefined;
		}, 1000));
	}
</script>

<button
	class={[
		'ml-2 flex cursor-pointer items-center justify-center gap-1 rounded',
		typeof name === 'string' && 'border border-gray-900 px-3 py-1',
	]}
	onmouseover={() => (copyHover = true)}
	onmouseout={() => (copyHover = false)}
	onfocus={() => (copyHover = true)}
	onblur={() => (copyHover = false)}
	onclick={() => {
		copyToClipboard(typeof content === 'string' ? content : content());
	}}
>
	{#if typeof name === 'string'}
		<span>{name}</span>
	{/if}
	<Icon
		class="size-6"
		src={copyed !== undefined ? ClipboardDocumentCheck : ClipboardDocument}
		theme={copyHover ? 'solid' : 'default'}
	/>
</button>
