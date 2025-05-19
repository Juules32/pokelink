import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		alias: {
			'$components': 'src/components'
		},
		adapter: adapter({
			fallback: '404.html'
		})
	}
};

export default config;
