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
		/** 绑定的键 */
		key: string;
		/** 绑定的值 */
		value: string;
		/**
		 * 默认值
		 * - 如果value为此值, 则删除searchParams中的key;
		 * - 如果searchParams中不存在key, 则使用此值初始化value
		 */
		default?: string;
		/** 组件卸载时是否清除searchParams中的key */
		clearOnUnmount?: boolean;
		/** 是否使用pushState模式更新url, false则使用replaceState模式 */
		pushMode?: boolean;
		/** 首次绑定的值: 如果提供此值, 同时初始化时searchParams中不存在key, 则设置value为此值 */
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
