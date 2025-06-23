<script lang="ts">
	import { getIconInfo, getIconPkgList, type IconPkg } from '$lib/components/icons';
	import { Icon } from '@steeze-ui/svelte-icon';
	import UrlSearchBind from './UrlSearchBind.svelte';
	import { untrack } from 'svelte';

	const defaultPkg = getIconPkgList()[0];

	let selectedPkg = $state<IconPkg>(defaultPkg);
	const { pkg, src, web, theme, imp } = $derived(getIconInfo(selectedPkg));

	let nowTheme = $derived.by(() => {
		if (!selectedPkg) return '';
		return untrack(() => theme[0]);
	});

	function copyToClipboard(text: string) {
		const el = document.createElement('textarea');
		el.value = text;
		document.body.appendChild(el);
		el.select();
		document.execCommand('copy');
		document.body.removeChild(el);
	}
</script>

<svelte:head>
	<title>Steeze UI 图标可视化 - {selectedPkg}</title>
</svelte:head>

<UrlSearchBind key="pkg" fst={defaultPkg} bind:value={selectedPkg} />
<UrlSearchBind key="theme" default={theme[0]} bind:value={nowTheme} />

<div class="flex h-screen w-screen flex-col">
	<!-- 包列表 -->
	<div class="flex w-full flex-wrap items-center justify-center gap-2 py-1">
		{#each getIconPkgList() as pkg (pkg)}
			<button
				class={[
					'inline-block rounded border border-gray-800 px-2 py-1 transition-colors duration-200 ease-in-out ',
					selectedPkg === pkg ? 'bg-blue-600 text-gray-100' : 'cursor-pointer hover:bg-gray-100',
				]}
				onclick={() => {
					selectedPkg = pkg;
				}}
			>
				{pkg}
			</button>
		{/each}
	</div>

	<!-- 简介 -->
	<div class="flex w-full flex-wrap items-center justify-center gap-2 py-1">
		{#each [['包源码', pkg], ['图标源码', src], ['图标网站', web]] as const as [label, href]}
			<a
				class="inline-block border-b py-1 transition-colors duration-200 ease-in-out hover:border-blue-600 hover:text-blue-600"
				{href}
				target="_blank"
			>
				{label}
			</a>
		{/each}
		<div class="ml-2 overflow-hidden rounded border">
			{#each theme as t, i (t)}
				<button
					class={[
						'inline-block px-3 py-1 transition-colors duration-200 ease-in-out ',
						i && 'border-l',
						t === nowTheme ? 'bg-amber-500 text-gray-50' : 'cursor-pointer hover:bg-gray-100',
					]}
					onclick={() => (nowTheme = t)}
				>
					{t}
				</button>
			{/each}
		</div>
	</div>

	<!-- 图标列表 -->
	<div class="flex w-full flex-1 flex-wrap items-center justify-center gap-2 p-5">
		{#await imp()}
			<div class="text-3xl">LOADING...</div>
		{:then icons}
			{#each Object.entries(icons).sort( ([nameA], [nameB]) => nameA.localeCompare(nameB), ) as [iconName, icon] (iconName)}
				<button
					class="h-24.5 w-20 cursor-pointer overflow-hidden rounded border transition-colors duration-200 ease-in-out hover:bg-gray-100"
					onclick={() => {
						copyToClipboard(iconName);
					}}
				>
					<Icon class="mx-1.5 mt-1.5 size-17" src={icon} theme={nowTheme} />
					<span class="w-full text-sm wrap-anywhere">{iconName}</span>
				</button>
			{/each}
		{/await}
	</div>
</div>
