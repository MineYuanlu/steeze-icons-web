<script lang="ts">
	import { ClipboardDocument, ClipboardDocumentCheck } from '@steeze-ui/heroicons';
	import { Icon } from '@steeze-ui/svelte-icon';

	const { content }: { content: string } = $props();

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

<div class="mx-1 flex items-start rounded-xl border border-gray-700 bg-gray-50 p-2">
	<div class="flex-1 wrap-anywhere">
		{content}
	</div>
	<button
		class="ml-2 size-6 cursor-pointer rounded"
		onmouseover={() => (copyHover = true)}
		onmouseout={() => (copyHover = false)}
		onfocus={() => (copyHover = true)}
		onblur={() => (copyHover = false)}
		onclick={() => {
			copyToClipboard(content);
		}}
	>
		<Icon
			src={copyed !== undefined ? ClipboardDocumentCheck : ClipboardDocument}
			theme={copyHover ? 'solid' : 'default'}
		/>
	</button>
</div>
