<script lang="ts">
	import { Clipboard, XCircle, XMark } from '@steeze-ui/heroicons';
	import { Icon, type IconSource } from '@steeze-ui/svelte-icon';
	import Code from './Code.svelte';

	const {
		pos,
		fade = false,
		pkg,
		name,
		icon,
		theme,
		onclose,
	}: {
		pos: `${'t' | 'b'}${'l' | 'r'}`;
		/** 是否淡化显示 */
		fade?: boolean;
		pkg: string;
		name: string;
		icon: IconSource;
		theme: string;

		onclose: () => void;
	} = $props();
</script>

<div
	role="tooltip"
	class={[
		'fixed z-50 flex h-140 w-100 flex-col rounded border bg-white transition-opacity duration-500 ease-in-out',
		pos[0] === 't' ? 'top-0' : 'bottom-0',
		pos[1] === 'l' ? 'left-0' : 'right-0',
		fade ? 'opacity-0' : '',
	]}
>
	<div class="flex h-10 flex-row-reverse">
		<Icon
			src={XMark}
			class="size-10 cursor-pointer"
			onclick={() => {
				onclose();
			}}
		/>
	</div>
	<Icon class="size-100 border-t border-b" src={icon} {theme} />
	<div class="flex flex-1 flex-col justify-around">
		<Code content="npm i -D {pkg}" />
		<Code content={name} />
	</div>
</div>
