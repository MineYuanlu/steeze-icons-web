<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let {
		key,
		value = $bindable(),
		default: defaultValue = '',
		clearOnUnmount = false,
		pushMode = false,
		fst,
	}: {
		key: string;
		value: string;
		default?: string;
		clearOnUnmount?: boolean;
		pushMode?: boolean;
		fst?: string;
	} = $props();

	if (browser) setValue(fst);
	$effect(() => {
		const searchs = new URLSearchParams(window.location.search);
		const oldValue = searchs.get(key) ?? defaultValue;
		if (oldValue !== value) {
			if (value === defaultValue) searchs.delete(key);
			else searchs.set(key, value);
			setSearch(searchs);
		}
	});
	onMount(() => {
		if (clearOnUnmount) {
			return () => {
				const searchs = new URLSearchParams(window.location.search);
				searchs.delete(key);
				setSearch(searchs);
			};
		}
	});

	function setValue(fst?: string) {
		const searchs = new URLSearchParams(window.location.search);
		const newValue = searchs.get(key) ?? fst ?? defaultValue;
		if (newValue !== value) {
			value = newValue;
		}
	}
	function setSearch(searchs: URLSearchParams) {
		const locStr = window.location.pathname;
		const searchStr = searchs.toString();
		const url = `${locStr === '/' ? '' : locStr}${searchStr ? '?' : ''}${searchStr}`;
		const state = { [key]: value };
		if (pushMode) window.history.pushState(state, '', url);
		else window.history.replaceState(state, '', url);
	}
</script>

<svelte:window onpopstate={() => setValue()} />
