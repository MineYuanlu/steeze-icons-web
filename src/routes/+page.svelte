<script lang="ts">
	import { getIconInfo, getIconPkgList, type IconPkg } from '$lib/components/icons';
	import { Icon } from '@steeze-ui/svelte-icon';
	import UrlSearchBind from './UrlSearchBind.svelte';
	import { untrack } from 'svelte';
	import { m } from '$lib/paraglide/messages';
	import Info from './Info.svelte';
	import IconList from './IconList.svelte';

	const defaultPkg = getIconPkgList()[0];

	let selectedPkg = $state<IconPkg>(defaultPkg);
	const { pkg, src, web, theme, imp } = $derived(getIconInfo(selectedPkg));

	let nowTheme = $derived.by(() => {
		if (!selectedPkg) return '';
		return untrack(() => theme[0]);
	});
</script>

<svelte:head>
	<title>{m.title({ name: selectedPkg })}</title>
</svelte:head>

<UrlSearchBind key="pkg" fst={defaultPkg} bind:value={selectedPkg} />
<UrlSearchBind key="theme" default={theme[0]} bind:value={nowTheme} />

<div class="flex h-screen w-full flex-col">
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
		{#each [[m.pMainPkgLink(), pkg], [m.pMainSrcLink(), src], [m.pMainWebLink(), web]] as const as [label, href]}
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
	{#await imp()}
		<div class="flex w-full flex-1 items-center justify-center">
			<div class="text-3xl">{m.loading()}</div>
		</div>
	{:then icons}
		<IconList {icons} theme={nowTheme} pkg={selectedPkg} />
	{/await}
</div>
