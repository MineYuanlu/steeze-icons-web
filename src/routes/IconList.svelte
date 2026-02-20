<script lang="ts">
	import { Icon, type IconSource } from '@steeze-ui/svelte-icon';
	import Info from './Info.svelte';

	const ITEM_H = 98;
	const ITEM_W = 80;
	const GAP = 8;
	const OVERSCAN = 2;

	let {
		icons,
		filteredIcons = $bindable(),
		theme,
		pkg,
		searchTxt = '',
	}: {
		icons: Record<string, IconSource>;
		filteredIcons: [string, IconSource][];
		theme: string;
		pkg: string;
		searchTxt?: string;
	} = $props();

	const iconArray = $derived(
		Object.entries(icons).sort(([nameA], [nameB]) => nameA.localeCompare(nameB)),
	);

	/* info state */

	let infoSelName = $state<string>();
	let infoSelSelected = $state(false);
	let infoSelHovered = $state(false);
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

	function search(name: string): boolean {
		if (!searchTxt) return true;
		name = name.toLowerCase();
		let idx = 0;
		for (const c of searchTxt.toLowerCase()) {
			idx = name.indexOf(c, idx);
			if (idx === -1) return false;
		}
		return true;
	}

	$effect(() => {
		filteredIcons = iconArray.filter(([name]) => search(name));
	});

	/* layout */

	let container: HTMLDivElement;

	let width = $state(0);
	let height = $state(0);
	let scrollTop = $state(0);

	const cols = $derived(Math.max(1, Math.floor((width + GAP) / (ITEM_W + GAP))));
	const rowHeight = ITEM_H + GAP;
	const rows = $derived(Math.ceil(filteredIcons.length / cols));
	const visibleRows = $derived(Math.ceil(height / rowHeight));
	const startRow = $derived(Math.max(0, Math.floor(scrollTop / rowHeight) - OVERSCAN));
	const endRow = $derived(Math.min(rows, startRow + visibleRows + OVERSCAN * 2));

	const visibleIcons = $derived.by(() => {
		const start = startRow * cols;
		const end = endRow * cols;
		return filteredIcons.slice(start, end);
	});

	function resizeObserver(node: HTMLElement) {
		const ro = new ResizeObserver(([e]) => {
			const cr = e.contentRect;
			width = cr.width;
			height = cr.height;
			// node.dispatchEvent(
			// 	new CustomEvent('resize', {
			// 		detail: { width: cr.width, height: cr.height },
			// 	}),
			// );
		});

		ro.observe(node);

		return {
			destroy() {
				ro.disconnect();
			},
		};
	}

	const offsetY = $derived(startRow * rowHeight);

	type IconMouseEvent = MouseEvent & {
		currentTarget: EventTarget & HTMLButtonElement;
	};

	function onIconClick(e: IconMouseEvent) {
		const iconName = e.currentTarget.dataset.name;
		if (!iconName) return;
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
	}

	function onIconEnter(e: IconMouseEvent) {
		const iconName = e.currentTarget.dataset.name;
		if (!iconName) return;
		if (!infoSelSelected) {
			infoSelName = iconName;
			infoSelPos = getClickPos(e, true);
		}
		infoSelHovered = true;
	}

	function onIconLeave() {
		infoSelHovered = false;
	}
</script>

<div
	bind:this={container}
	class={[
		'mt-1 w-full flex-1 overflow-auto border-t p-5 transition-colors duration-200 ease-in-out',
		scrollTop > 0 ? 'border-t-gray-900' : 'border-t-transparent',
	]}
	onscroll={(e) => (scrollTop = (e.target as HTMLElement).scrollTop)}
	onmouseleave={() => {
		if (!infoSelSelected) infoSelName = undefined;
	}}
	role="group"
	use:resizeObserver
>
	<div style={`height:${rows * rowHeight}px; position:relative;`}>
		<div style={`transform:translateY(${offsetY}px);`} class="flex flex-wrap items-start gap-2">
			{#each visibleIcons as [iconName, icon] (iconName)}
				<button
					class={[
						'h-24.5 w-20 cursor-pointer overflow-hidden rounded border border-gray-800 transition-colors duration-200 ease-in-out',
						infoSelSelected && infoSelName === iconName ? 'bg-blue-200' : 'hover:bg-gray-100',
					]}
					data-name={iconName}
					onclick={onIconClick}
					onmouseenter={onIconEnter}
					onmouseleave={onIconLeave}
				>
					<Icon class="mx-1.5 mt-1.5 size-17" src={icon} {theme} />
					<span class="w-full text-sm wrap-anywhere">{iconName}</span>
				</button>
			{/each}
		</div>
	</div>
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
