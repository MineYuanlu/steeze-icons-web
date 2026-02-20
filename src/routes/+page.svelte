<script lang="ts">
	import { getIconInfo, getIconPkgList, type IconPkg } from '$lib/components/icons';
	import UrlSearchBind from './UrlSearchBind.svelte';
	import { m } from '$lib/paraglide/messages';
	import IconList from './IconList.svelte';
	import { building } from '$app/environment';
	import type { IconSource } from '@steeze-ui/svelte-icon';
	import Copy from './Copy.svelte';

	const defaultPkg = getIconPkgList()[0];

	let selectedPkg = $state<IconPkg | 'all'>(defaultPkg);
	const iconInfo = $derived(selectedPkg === 'all' ? undefined : getIconInfo(selectedPkg));

	const defaultTheme = $derived.by(() => {
		const theme = iconInfo?.theme;
		if (!theme) return '';
		return theme[0] ?? '';
	});

	let nowTheme = $derived(defaultTheme);

	let searchTxt = $state('');
	let filteredIcons = $state<[string, IconSource][]>([]);

	const importPromise = $derived.by(async () => {
		const info = iconInfo;
		if (info) return await info.imp();
		const all = await Promise.all(
			getIconPkgList()
				.map(getIconInfo)
				.map((i) => i.imp()),
		);
		return all.reduce((acc, cur) => Object.assign(acc, cur), {});
	});
</script>

<svelte:head>
	<title>{m.pMainTitle({ name: building ? '' : selectedPkg })}</title>
</svelte:head>

<UrlSearchBind key="pkg" fst={defaultPkg} bind:value={selectedPkg} />
<UrlSearchBind key="theme" default={defaultTheme} bind:value={nowTheme} />

<div class="flex h-screen w-full flex-col">
	<!-- 包列表 -->
	<div class="flex w-full flex-wrap items-center justify-center gap-2 py-1">
		{#snippet pkg_switch_btn(pkg: IconPkg | 'all')}
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
		{/snippet}
		{#each getIconPkgList() as pkg (pkg)}
			{@render pkg_switch_btn(pkg)}
		{/each}
		{@render pkg_switch_btn('all')}
	</div>

	<!-- 简介 -->
	<div class="flex w-full flex-wrap items-center justify-center gap-2 py-1">
		{#if iconInfo}
			{@const { pkg, src, web, theme } = iconInfo}
			{#each [[m.pMainPkgLink(), pkg], [m.pMainSrcLink(), src], [m.pMainWebLink(), web]] as const as [label, href], i (i)}
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
		{/if}
		<input
			bind:value={searchTxt}
			class="ml-2 inline-block w-80 rounded border px-2 py-1"
			placeholder={m.pMainSearchPlaceholder()}
		/>
		<span>
			{#await importPromise}
				-- / --
			{:then icons}
				{filteredIcons.length} / {Object.keys(icons).length}
			{/await}
		</span>
		<Copy content={() => filteredIcons.map(([name]) => name).join('\n')} name={m.pMainCopyList()} />
	</div>

	<!-- 图标列表 -->
	{#await importPromise}
		<div class="flex w-full flex-1 items-center justify-center">
			<div class="text-3xl">{m.loading()}</div>
		</div>
	{:then icons}
		<IconList {icons} theme={nowTheme} pkg={selectedPkg} {searchTxt} bind:filteredIcons />
	{/await}
</div>
