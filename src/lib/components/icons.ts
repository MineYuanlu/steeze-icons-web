import type { IconSource } from '@steeze-ui/svelte-icon';

type IconInfo = {
	/** 包名 */
	name: string;
	/** 包地址 */
	pkg: string;
	/** 来源地址 */
	src: string;
	/** 来源网站 */
	web: string;
	/** 主题 */
	theme: string[];
	imp: () => Promise<Record<string, IconSource>>;
};

const icons = [
	{
		name: '@steeze-ui/heroicons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/heroicons-builder',
		src: 'https://github.com/tailwindlabs/heroicons',
		web: 'https://heroicons.com/',
		theme: ['default(outline)', 'solid', 'mini'],
		imp: () => import('@steeze-ui/heroicons'),
	},
	{
		name: '@steeze-ui/simple-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/simple-icons-builder/',
		src: 'https://github.com/simple-icons/simple-icons',
		web: 'https://simpleicons.org/',
		theme: ['default'],
		imp: () => import('@steeze-ui/simple-icons'),
	},
	{
		name: '@steeze-ui/tabler-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/tabler-icons-builder/',
		src: 'https://github.com/tabler/tabler-icons',
		web: 'https://tabler-icons.io/',
		theme: ['default(outline)', 'filled'],
		imp: () => import('@steeze-ui/tabler-icons'),
	},
	{
		name: '@steeze-ui/radix-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/radix-icons-builder',
		src: 'https://github.com/radix-ui/icons',
		web: 'https://icons.modulz.app/',
		theme: ['default'],
		imp: () => import('@steeze-ui/radix-icons'),
	},
	{
		name: '@steeze-ui/material-design-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/material-design-icons-builder/',
		src: 'https://github.com/google/material-design-icons',
		web: 'https://fonts.google.com/icons',
		theme: ['default(filled)', 'outlined', 'rounded', 'sharp', 'twotone'],
		imp: () => import('@steeze-ui/material-design-icons'),
	},
	{
		name: '@steeze-ui/lucide-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/lucide-icons-builder',
		src: 'https://github.com/lucide-icons/lucide',
		web: 'https://lucide.dev/',
		theme: ['default'],
		imp: () => import('@steeze-ui/lucide-icons'),
	},
	{
		name: '@steeze-ui/phosphor-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/phosphor-icons-builder/',
		src: 'https://phosphoricons.com/',
		web: 'https://phosphoricons.com/',
		theme: ['thin', 'light', 'default(regular)', 'bold', 'fill', 'duotone'],
		imp: () => import('@steeze-ui/phosphor-icons'),
	},
	{
		name: '@steeze-ui/carbon-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/carbon-icons-builder/',
		src: 'https://github.com/carbon-design-system/carbon/tree/main/packages/icons',
		web: 'https://carbondesignsystem.com/guidelines/icons/library/',
		theme: ['default'],
		imp: () => import('@steeze-ui/carbon-icons'),
	},
	{
		name: '@steeze-ui/remix-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/remix-icons-builder',
		src: 'https://github.com/Remix-Design/remixicon',
		web: 'https://remixicon.com/',
		theme: ['default(outline)', 'solid'],
		imp: () => import('@steeze-ui/remix-icons'),
	},
	{
		name: '@steeze-ui/iconic-free',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/iconic-free-builder',
		src: 'https://iconic.app/',
		web: 'https://iconic.app/c/availability/free/',
		theme: ['default'],
		imp: () => import('@steeze-ui/iconic-free'),
	},
	{
		name: '@steeze-ui/octicons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/octicons-builder',
		src: 'https://github.com/primer/octicons',
		web: 'https://primer.style/octicons/',
		theme: ['default(16)', '24', '12'],
		imp: () => import('@steeze-ui/octicons'),
	},
	{
		name: '@steeze-ui/css-gg',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/css-gg-builder/',
		src: 'https://css.gg/',
		web: 'https://css.gg/app',
		theme: ['default'],
		imp: () => import('@steeze-ui/css-gg'),
	},
	{
		name: '@steeze-ui/font-awesome',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/font-awesome-builder/',
		src: 'https://github.com/FortAwesome/Font-Awesome',
		web: 'https://fontawesome.com/search',
		theme: ['default', 'solid'],
		imp: () => import('@steeze-ui/font-awesome'),
	},
	{
		name: '@steeze-ui/feather-icons',
		pkg: 'https://github.com/steeze-ui/icons/blob/main/packages/builders/feather-icons-builder) (deprecated',
		src: 'https://github.com/feathericons/feather',
		web: 'https://feathericons.com/',
		theme: ['default'],
		imp: () => import('@steeze-ui/feather-icons'),
	},
] as const satisfies IconInfo[];
export type IconPkg = (typeof icons)[number]['name'];
export function getIconPkgList(): IconPkg[] {
	return icons.map((i) => i.name);
}
export function getIconInfo(name: IconPkg): IconInfo {
	const info = icons.find((i) => i.name === name)!;
	return {
		...info,
		imp: replaceImp(name, info.imp),
	};
}
export function isIconSource(src: unknown): src is IconSource {
	if (typeof src !== 'object' || src === null) return false;
	if (!('default' in src)) return false;
	const AllowedTags = new Set(['path', 'circle', 'rect', 'polygon', 'polyline', 'line']);
	return Object.values(src).every((theme) => {
		if (typeof theme !== 'object' || theme === null) return false;
		if (!('a' in theme)) return false;
		return Object.entries(theme).every(([tag, attrs]) => {
			if (tag === 'a') return typeof attrs === 'string';
			else if (AllowedTags.has(tag))
				return (
					Array.isArray(attrs) &&
					attrs.every(
						(attr) =>
							typeof attr === 'object' &&
							attr !== null &&
							Object.entries(attr).every(
								([k, v]) => typeof k === 'string' && typeof v === 'string',
							),
					)
				);
			else return false;
		});
	});
}
const impCache = new Map<IconPkg, Promise<Record<string, IconSource>>>();
function replaceImp(name: IconPkg, imp: () => Promise<Record<string, IconSource>>) {
	return async () => {
		if (impCache.has(name)) {
			const result = impCache.get(name)!;
			await new Promise((r) => setTimeout(r));
			return result;
		}
		const promise = imp();
		impCache.set(name, promise);
		return promise;
	};
}
