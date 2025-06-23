<script lang="ts">
	import { Icon, type IconSource } from '@steeze-ui/svelte-icon';
	import Info from './Info.svelte';

	const {
		icons,
		theme,
		pkg,
	}: {
		icons: Record<string, IconSource>;
		theme: string;
		pkg: string;
	} = $props();

	let infoSelName = $state<string>();
	let infoSelSelected = $state<boolean>(false);
	let infoSelHovered = $state<boolean>(false);
	let infoSelPos = $state<ReturnType<typeof getClickPos>>('br');

	function getClickPos({ clientX, clientY }: MouseEvent, inv = true): `${'t' | 'b'}${'l' | 'r'}` {
		const { innerWidth, innerHeight } = window;
		const t = 0.5;
		let isLeft = clientX / innerWidth < t;
		let isTop = clientY / innerHeight < t;
		if (inv) {
			isLeft = !isLeft;
			isTop = !isTop;
		}
		return `${isTop ? 't' : 'b'}${isLeft ? 'l' : 'r'}`;
	}
</script>

<div
	class="flex w-full flex-1 flex-wrap items-center justify-around gap-2 p-5"
	onmouseleave={() => {
		if (!infoSelSelected) infoSelName = undefined;
	}}
	role="group"
>
	{#each Object.entries(icons).sort( ([nameA], [nameB]) => nameA.localeCompare(nameB), ) as [iconName, icon] (iconName)}
		<button
			class={[
				'h-24.5 w-20 cursor-pointer overflow-hidden rounded border border-gray-800 transition-colors duration-200 ease-in-out ',
				infoSelSelected && infoSelName === iconName ? 'bg-blue-200' : 'hover:bg-gray-100',
			]}
			onclick={(e) => {
				// copyToClipboard(iconName);
				if (infoSelSelected) {
					if (infoSelName === iconName) {
						infoSelName = undefined;
						infoSelSelected = false;
					} else {
						infoSelName = iconName;
					}
				} else {
					infoSelName = iconName;
					infoSelSelected = true;
				}
				infoSelPos = getClickPos(e, true);
			}}
			onmouseenter={(e) => {
				if (!infoSelSelected) {
					infoSelName = iconName;
					infoSelPos = getClickPos(e, true);
				}
				infoSelHovered = true;
			}}
			onmouseleave={() => {
				infoSelHovered = false;
			}}
		>
			<Icon class="mx-1.5 mt-1.5 size-17" src={icon} {theme} />
			<span class="w-full text-sm wrap-anywhere">{iconName}</span>
		</button>
	{/each}
</div>

{#if infoSelName}
	<Info
		pos={infoSelPos}
		fade={!infoSelHovered && !infoSelSelected}
		{pkg}
		name={infoSelName}
		icon={icons[infoSelName]}
		{theme}
		onclose={() => {
			infoSelName = undefined;
			infoSelSelected = false;
		}}
	/>
{/if}
