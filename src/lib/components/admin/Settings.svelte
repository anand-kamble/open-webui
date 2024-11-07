<script>
	import { getContext, tick, onMount } from 'svelte';
	import { toast } from 'svelte-sonner';

	import Database from './Settings/Database.svelte';

	import General from './Settings/General.svelte';
	import Users from './Settings/Users.svelte';

	import Pipelines from './Settings/Pipelines.svelte';
	import Audio from './Settings/Audio.svelte';
	import Images from './Settings/Images.svelte';
	import Interface from './Settings/Interface.svelte';
	import Models from './Settings/Models.svelte';
	import Connections from './Settings/Connections.svelte';
	import Documents from './Settings/Documents.svelte';
	import WebSearch from './Settings/WebSearch.svelte';
	import PaperQA from './Settings/PaperQA.svelte';
	import { config } from '$lib/stores';
	import { getBackendConfig } from '$lib/apis';
	import ChartBar from '../icons/ChartBar.svelte';
	import DocumentChartBar from '../icons/DocumentChartBar.svelte';
	import Evaluations from './Settings/Evaluations.svelte';

	const i18n = getContext('i18n');

	let selectedTab = 'general';

	onMount(() => {
		const containerElement = document.getElementById('admin-settings-tabs-container');

		if (containerElement) {
			containerElement.addEventListener('wheel', function (event) {
				if (event.deltaY !== 0) {
					// Adjust horizontal scroll position based on vertical scroll
					containerElement.scrollLeft += event.deltaY;
				}
			});
		}
	});
</script>

<div class="flex flex-col lg:flex-row w-full h-full py-2 lg:space-x-4">
	<div
		id="admin-settings-tabs-container"
		class="tabs flex flex-row overflow-x-auto space-x-1 max-w-full lg:space-x-0 lg:space-y-1 lg:flex-col lg:flex-none lg:w-44 dark:text-gray-200 text-xs text-left scrollbar-none"
	>
		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 lg:flex-none flex text-right transition {selectedTab ===
			'general'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'general';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						fill-rule="evenodd"
						d="M6.955 1.45A.5.5 0 0 1 7.452 1h1.096a.5.5 0 0 1 .497.45l.17 1.699c.484.12.94.312 1.356.562l1.321-1.081a.5.5 0 0 1 .67.033l.774.775a.5.5 0 0 1 .034.67l-1.08 1.32c.25.417.44.873.561 1.357l1.699.17a.5.5 0 0 1 .45.497v1.096a.5.5 0 0 1-.45.497l-1.699.17c-.12.484-.312.94-.562 1.356l1.082 1.322a.5.5 0 0 1-.034.67l-.774.774a.5.5 0 0 1-.67.033l-1.322-1.08c-.416.25-.872.44-1.356.561l-.17 1.699a.5.5 0 0 1-.497.45H7.452a.5.5 0 0 1-.497-.45l-.17-1.699a4.973 4.973 0 0 1-1.356-.562L4.108 13.37a.5.5 0 0 1-.67-.033l-.774-.775a.5.5 0 0 1-.034-.67l1.08-1.32a4.971 4.971 0 0 1-.561-1.357l-1.699-.17A.5.5 0 0 1 1 8.548V7.452a.5.5 0 0 1 .45-.497l1.699-.17c.12-.484.312-.94.562-1.356L2.629 4.107a.5.5 0 0 1 .034-.67l.774-.774a.5.5 0 0 1 .67-.033L5.43 3.71a4.97 4.97 0 0 1 1.356-.561l.17-1.699ZM6 8c0 .538.212 1.026.558 1.385l.057.057a2 2 0 0 0 2.828-2.828l-.058-.056A2 2 0 0 0 6 8Z"
						clip-rule="evenodd"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('General')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'users'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'users';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						d="M8 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM3.156 11.763c.16-.629.44-1.21.813-1.72a2.5 2.5 0 0 0-2.725 1.377c-.136.287.102.58.418.58h1.449c.01-.077.025-.156.045-.237ZM12.847 11.763c.02.08.036.16.046.237h1.446c.316 0 .554-.293.417-.579a2.5 2.5 0 0 0-2.722-1.378c.374.51.653 1.09.813 1.72ZM14 7.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0ZM3.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM5 13c-.552 0-1.013-.455-.876-.99a4.002 4.002 0 0 1 7.753 0c.136.535-.324.99-.877.99H5Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Users')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'connections'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'connections';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						d="M1 9.5A3.5 3.5 0 0 0 4.5 13H12a3 3 0 0 0 .917-5.857 2.503 2.503 0 0 0-3.198-3.019 3.5 3.5 0 0 0-6.628 2.171A3.5 3.5 0 0 0 1 9.5Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Connections')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'models'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'models';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						fill-rule="evenodd"
						d="M10 1c3.866 0 7 1.79 7 4s-3.134 4-7 4-7-1.79-7-4 3.134-4 7-4zm5.694 8.13c.464-.264.91-.583 1.306-.952V10c0 2.21-3.134 4-7 4s-7-1.79-7-4V8.178c.396.37.842.688 1.306.953C5.838 10.006 7.854 10.5 10 10.5s4.162-.494 5.694-1.37zM3 13.179V15c0 2.21 3.134 4 7 4s7-1.79 7-4v-1.822c-.396.37-.842.688-1.306.953-1.532.875-3.548 1.369-5.694 1.369s-4.162-.494-5.694-1.37A7.009 7.009 0 013 13.179z"
						clip-rule="evenodd"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Models')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'evaluations'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'evaluations';
			}}
		>
			<div class=" self-center mr-2">
				<DocumentChartBar />
			</div>
			<div class=" self-center">{$i18n.t('Evaluations')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'documents'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'documents';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path d="M11.625 16.5a1.875 1.875 0 1 0 0-3.75 1.875 1.875 0 0 0 0 3.75Z" />
					<path
						fill-rule="evenodd"
						d="M5.625 1.5H9a3.75 3.75 0 0 1 3.75 3.75v1.875c0 1.036.84 1.875 1.875 1.875H16.5a3.75 3.75 0 0 1 3.75 3.75v7.875c0 1.035-.84 1.875-1.875 1.875H5.625a1.875 1.875 0 0 1-1.875-1.875V3.375c0-1.036.84-1.875 1.875-1.875Zm6 16.5c.66 0 1.277-.19 1.797-.518l1.048 1.048a.75.75 0 0 0 1.06-1.06l-1.047-1.048A3.375 3.375 0 1 0 11.625 18Z"
						clip-rule="evenodd"
					/>
					<path
						d="M14.25 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 16.5 7.5h-1.875a.375.375 0 0 1-.375-.375V5.25Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Documents')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'web'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'web';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						d="M21.721 12.752a9.711 9.711 0 0 0-.945-5.003 12.754 12.754 0 0 1-4.339 2.708 18.991 18.991 0 0 1-.214 4.772 17.165 17.165 0 0 0 5.498-2.477ZM14.634 15.55a17.324 17.324 0 0 0 .332-4.647c-.952.227-1.945.347-2.966.347-1.021 0-2.014-.12-2.966-.347a17.515 17.515 0 0 0 .332 4.647 17.385 17.385 0 0 0 5.268 0ZM9.772 17.119a18.963 18.963 0 0 0 4.456 0A17.182 17.182 0 0 1 12 21.724a17.18 17.18 0 0 1-2.228-4.605ZM7.777 15.23a18.87 18.87 0 0 1-.214-4.774 12.753 12.753 0 0 1-4.34-2.708 9.711 9.711 0 0 0-.944 5.004 17.165 17.165 0 0 0 5.498 2.477ZM21.356 14.752a9.765 9.765 0 0 1-7.478 6.817 18.64 18.64 0 0 0 1.988-4.718 18.627 18.627 0 0 0 5.49-2.098ZM2.644 14.752c1.682.971 3.53 1.688 5.49 2.099a18.64 18.64 0 0 0 1.988 4.718 9.765 9.765 0 0 1-7.478-6.816ZM13.878 2.43a9.755 9.755 0 0 1 6.116 3.986 11.267 11.267 0 0 1-3.746 2.504 18.63 18.63 0 0 0-2.37-6.49ZM12 2.276a17.152 17.152 0 0 1 2.805 7.121c-.897.23-1.837.353-2.805.353-.968 0-1.908-.122-2.805-.353A17.151 17.151 0 0 1 12 2.276ZM10.122 2.43a18.629 18.629 0 0 0-2.37 6.49 11.266 11.266 0 0 1-3.746-2.504 9.754 9.754 0 0 1 6.116-3.985Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Web Search')}</div>
		</button>

		<!-- <button
			class="px-2.5 py-2.5 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'paperqa'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'paperqa';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					viewBox="0 0 24 24"
					fill="currentColor"
					class="w-4 h-4"
					xmlns="http://www.w3.org/2000/svg"
					><g id="SVGRepo_iconCarrier">
						<path
							d="M482.2,470c0,17.6-14.4,31.6-31.6,31.6H38.2c-17.6,0-31.6-14.4-31.6-31.6V57.2 c0-17.6,14.4-31.6,31.6-31.6h412.4c17.6,0,31.6,14.4,31.6,31.6V470L482.2,470z"
						></path>
						<path
							d="M359,210.4c-3.2,3.2-3.2,8.8,0,12.4c1.6,1.6,4,2.4,6,2.4c2.4,0,4.4-0.8,6-2.4L483.8,110 c24-24,24-62.8,0-86.8s-62.8-24-86.8,0l-21.6,21.6L258.6,161.6c-1.6,1.6-2.4,4-2.4,6c0,2.4,0.8,4.4,2.4,6l49.2,49.2 c3.2,3.2,8.8,3.2,12.4,0L445.8,97.2c3.2-3.2,3.2-8.8,0-12.4l-24.4-24.4c-1.6-1.6-4-2.4-6-2.4c-2.4,0-4.4,0.8-6,2.4L309,160.8 c-3.6,3.2-3.6,8.8,0,12.4c3.2,3.2,8.8,3.2,12.4,0l94.4-94.4l12.4,12.4L314.6,204.8L277.8,168L410.2,35.6c17.2-17.2,45.2-17.2,62.4,0 c17.2,17.2,17.2,45.2,0,62.4L359,210.4"
						></path>
						<path
							d="M246.2,139.6h-172c-2.4,0-4-1.6-4-4s1.6-4,4-4h172c2.4,0,4,1.6,4,4S248.6,139.6,246.2,139.6z"
						></path>
						<path
							d="M138.2,179.6h-64c-2.4,0-4-1.6-4-4s1.6-4,4-4h64c2.4,0,4,1.6,4,4S140.6,179.6,138.2,179.6z"
						></path>
						<path
							d="M226.2,179.6h-56c-2.4,0-4-1.6-4-4s1.6-4,4-4h56c2.4,0,4,1.6,4,4S228.6,179.6,226.2,179.6z"
						></path>
						<path
							d="M266.2,219.6h-192c-2.4,0-4-1.6-4-4s1.6-4,4-4h192c2.4,0,4,1.6,4,4S268.6,219.6,266.2,219.6z"
						></path>
						<path
							d="M406.2,259.6h-332c-2.4,0-4-1.6-4-4s1.6-4,4-4h332c2.4,0,4,1.6,4,4S408.6,259.6,406.2,259.6z"
						></path>
						<path
							d="M406.2,379.6h-332c-2.4,0-4-1.6-4-4s1.6-4,4-4h332c2.4,0,4,1.6,4,4S408.6,379.6,406.2,379.6z"
						></path>
						<path
							d="M138.2,299.6h-64c-2.4,0-4-1.6-4-4s1.6-4,4-4h64c2.4,0,4,1.6,4,4S140.6,299.6,138.2,299.6z"
						></path>
						<path
							d="M406.2,299.6h-236c-2.4,0-4-1.6-4-4s1.6-4,4-4h236c2.4,0,4,1.6,4,4S408.6,299.6,406.2,299.6z"
						></path>
						<path
							d="M406.2,339.6h-80c-2.4,0-4-1.6-4-4s1.6-4,4-4h80c2.4,0,4,1.6,4,4S408.6,339.6,406.2,339.6z"
						></path>
						<path
							d="M290.2,339.6h-216c-2.4,0-4-1.6-4-4s1.6-4,4-4h216c2.4,0,4,1.6,4,4S292.6,339.6,290.2,339.6z"
						></path>
						<path
							d="M138.2,419.6h-64c-2.4,0-4-1.6-4-4s1.6-4,4-4h64c2.4,0,4,1.6,4,4S140.6,419.6,138.2,419.6z"
						></path>
						<path
							d="M406.2,419.6h-236c-2.4,0-4-1.6-4-4s1.6-4,4-4h236c2.4,0,4,1.6,4,4S408.6,419.6,406.2,419.6z"
						></path>
						<path
							d="M451.4,507.6H39c-20.4,0-38.8-17.2-38.8-36.4V54.8c0-17.2,15.2-30.4,41.6-35.2c0.4,0,0.4,0,0.8,0h355.6c2.4,0,4,1.6,4,4 s-1.6,4-4,4H43c-10.8,2-34.8,8.8-34.8,27.2v416.4c0,14.4,15.2,28.4,30.8,28.4h412.4c16.4,0,24.8-14.4,24.8-28.4V117.6 c0-2.4,1.6-4,4-4s4,1.6,4,4v353.6C484.2,492,470.2,507.6,451.4,507.6z"
						></path>
						<path
							d="M315.4,228.4c-3.2,0-6.4-1.2-8.8-3.6l-49.2-49.2c-2.4-2.4-3.6-5.6-3.6-8.8c0-3.2,1.2-6.4,3.6-8.8L374.2,41.2 c1.6-1.6,4-1.6,5.6,0s1.6,4,0,5.6L263,163.6c-0.8,0.8-1.2,2-1.2,3.2s0.4,2.4,1.2,3.2l49.2,49.2c1.6,1.6,4.8,1.6,6.8,0L444.6,93.6 c0.8-0.8,1.2-2,1.2-3.2s-0.4-2.4-1.2-3.2l-24.8-24.8c-1.6-1.6-4.8-1.6-6.8,0L312.6,162.8c-0.8,0.8-1.2,2-1.2,3.2s0.4,2.4,1.2,3.2 c0.8,0.8,2,1.2,3.2,1.2l0,0c1.2,0,2.4-0.4,3.2-1.2l94.4-94.4c1.6-1.6,4-1.6,5.6,0l12.4,12.4c0.8,0.8,1.2,1.6,1.2,2.8 c0,1.2-0.4,2-1.2,2.8L317.8,206.4c-1.6,1.6-4,1.6-5.6,0l-36.8-36.8c-0.8-0.8-1.2-1.6-1.2-2.8s0.4-2,1.2-2.8L407.8,31.6 c9.2-9.2,21.2-14,34-14s24.8,4.8,34,14c18.8,18.8,18.8,49.2,0,68L363,212.4c-1.6,1.6-4,1.6-5.6,0s-1.6-4,0-5.6L470.2,93.6 c15.6-15.6,15.6-41.2,0-56.8c-7.6-7.6-17.6-11.6-28.4-11.6c-10.8,0-20.8,4-28.4,11.6L284.2,166l31.2,31.2l108-108l-6.8-6.8L325,174 c-2.4,2.4-5.6,3.6-8.8,3.6l0,0c-3.2,0-6.4-1.2-8.8-3.6c-2.4-2.4-3.6-5.6-3.6-8.8c0-3.2,1.2-6.4,3.6-8.8L407.8,56 c4.8-4.8,13.2-4.8,18,0l24.4,24.4c2.4,2.4,3.6,5.6,3.6,8.8s-1.2,6.4-3.6,8.8L324.6,223.6C321.8,226.8,318.6,228.4,315.4,228.4z"
						></path>
						<path
							d="M366.2,228.4c-3.2,0-6.4-1.2-8.8-3.6c-2.4-2.4-3.6-5.6-3.6-8.8c0-3.2,1.2-6.4,3.6-8.8c1.6-1.6,4-1.6,5.6,0s1.6,4,0,5.6 c-0.8,0.8-1.2,2-1.2,3.2s0.4,2.4,1.2,3.2c1.6,1.6,4.8,1.6,6.8,0l112.8-112.8c10.8-10.8,16.8-25.2,16.8-40.8s-6-29.6-16.8-40.8 c-22.4-22.4-58.8-22.4-81.2,0c-1.6,1.6-4,1.6-5.6,0s-1.6-4,0-5.6c25.6-25.6,67.2-25.6,92.4,0c12.4,12.4,19.2,28.8,19.2,46.4 s-6.8,34-19.2,46.4L375.4,224.8C372.6,226.8,369.4,228.4,366.2,228.4z"
						></path>
					</g></svg
				>
			</div>
			<div class=" self-center">{$i18n.t('Paper QA')}</div>
		</button> -->

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'interface'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'interface';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						fill-rule="evenodd"
						d="M2 4.25A2.25 2.25 0 0 1 4.25 2h7.5A2.25 2.25 0 0 1 14 4.25v5.5A2.25 2.25 0 0 1 11.75 12h-1.312c.1.128.21.248.328.36a.75.75 0 0 1 .234.545v.345a.75.75 0 0 1-.75.75h-4.5a.75.75 0 0 1-.75-.75v-.345a.75.75 0 0 1 .234-.545c.118-.111.228-.232.328-.36H4.25A2.25 2.25 0 0 1 2 9.75v-5.5Zm2.25-.75a.75.75 0 0 0-.75.75v4.5c0 .414.336.75.75.75h7.5a.75.75 0 0 0 .75-.75v-4.5a.75.75 0 0 0-.75-.75h-7.5Z"
						clip-rule="evenodd"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Interface')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'audio'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'audio';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						d="M7.557 2.066A.75.75 0 0 1 8 2.75v10.5a.75.75 0 0 1-1.248.56L3.59 11H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.59l3.162-2.81a.75.75 0 0 1 .805-.124ZM12.95 3.05a.75.75 0 1 0-1.06 1.06 5.5 5.5 0 0 1 0 7.78.75.75 0 1 0 1.06 1.06 7 7 0 0 0 0-9.9Z"
					/>
					<path
						d="M10.828 5.172a.75.75 0 1 0-1.06 1.06 2.5 2.5 0 0 1 0 3.536.75.75 0 1 0 1.06 1.06 4 4 0 0 0 0-5.656Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Audio')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'images'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'images';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						fill-rule="evenodd"
						d="M2 4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4Zm10.5 5.707a.5.5 0 0 0-.146-.353l-1-1a.5.5 0 0 0-.708 0L9.354 9.646a.5.5 0 0 1-.708 0L6.354 7.354a.5.5 0 0 0-.708 0l-2 2a.5.5 0 0 0-.146.353V12a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5V9.707ZM12 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"
						clip-rule="evenodd"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Images')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'pipelines'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'pipelines';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="currentColor"
					class="size-4"
				>
					<path
						d="M11.644 1.59a.75.75 0 0 1 .712 0l9.75 5.25a.75.75 0 0 1 0 1.32l-9.75 5.25a.75.75 0 0 1-.712 0l-9.75-5.25a.75.75 0 0 1 0-1.32l9.75-5.25Z"
					/>
					<path
						d="m3.265 10.602 7.668 4.129a2.25 2.25 0 0 0 2.134 0l7.668-4.13 1.37.739a.75.75 0 0 1 0 1.32l-9.75 5.25a.75.75 0 0 1-.71 0l-9.75-5.25a.75.75 0 0 1 0-1.32l1.37-.738Z"
					/>
					<path
						d="m10.933 19.231-7.668-4.13-1.37.739a.75.75 0 0 0 0 1.32l9.75 5.25c.221.12.489.12.71 0l9.75-5.25a.75.75 0 0 0 0-1.32l-1.37-.738-7.668 4.13a2.25 2.25 0 0 1-2.134-.001Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Pipelines')}</div>
		</button>

		<button
			class="px-2.5 py-2 min-w-fit rounded-lg flex-1 md:flex-none flex text-right transition {selectedTab ===
			'db'
				? 'bg-gray-100 dark:bg-gray-800'
				: ' hover:bg-gray-50 dark:hover:bg-gray-850'}"
			on:click={() => {
				selectedTab = 'db';
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path d="M8 7c3.314 0 6-1.343 6-3s-2.686-3-6-3-6 1.343-6 3 2.686 3 6 3Z" />
					<path
						d="M8 8.5c1.84 0 3.579-.37 4.914-1.037A6.33 6.33 0 0 0 14 6.78V8c0 1.657-2.686 3-6 3S2 9.657 2 8V6.78c.346.273.72.5 1.087.683C4.42 8.131 6.16 8.5 8 8.5Z"
					/>
					<path
						d="M8 12.5c1.84 0 3.579-.37 4.914-1.037.366-.183.74-.41 1.086-.684V12c0 1.657-2.686 3-6 3s-6-1.343-6-3v-1.22c.346.273.72.5 1.087.683C4.42 12.131 6.16 12.5 8 12.5Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Database')}</div>
		</button>
	</div>

	<div class="flex-1 mt-3 lg:mt-0 overflow-y-scroll">
		{#if selectedTab === 'general'}
			<General
				saveHandler={async () => {
					toast.success($i18n.t('Settings saved successfully!'));

					await tick();
					await config.set(await getBackendConfig());
				}}
			/>
		{:else if selectedTab === 'users'}
			<Users
				saveHandler={() => {
					toast.success($i18n.t('Settings saved successfully!'));
				}}
			/>
		{:else if selectedTab === 'connections'}
			<Connections
				on:save={() => {
					toast.success($i18n.t('Settings saved successfully!'));
				}}
			/>
		{:else if selectedTab === 'models'}
			<Models />
		{:else if selectedTab === 'evaluations'}
			<Evaluations />
		{:else if selectedTab === 'documents'}
			<Documents
				on:save={async () => {
					toast.success($i18n.t('Settings saved successfully!'));

					await tick();
					await config.set(await getBackendConfig());
				}}
			/>
		{:else if selectedTab === 'web'}
			<WebSearch
				saveHandler={async () => {
					toast.success($i18n.t('Settings saved successfully!'));

					await tick();
					await config.set(await getBackendConfig());
				}}
			/>
		{:else if selectedTab === 'interface'}
			<Interface
				on:save={() => {
					toast.success($i18n.t('Settings saved successfully!'));
				}}
			/>
		{:else if selectedTab === 'audio'}
			<Audio
				saveHandler={() => {
					toast.success($i18n.t('Settings saved successfully!'));
				}}
			/>
		{:else if selectedTab === 'images'}
			<Images
				on:save={() => {
					toast.success($i18n.t('Settings saved successfully!'));
				}}
			/>
		{:else if selectedTab === 'db'}
			<Database
				saveHandler={() => {
					toast.success($i18n.t('Settings saved successfully!'));
				}}
			/>
		{:else if selectedTab === 'pipelines'}
			<Pipelines
				saveHandler={() => {
					toast.success($i18n.t('Settings saved successfully!'));
				}}
			/>
		{:else if selectedTab === 'paperqa'}
			<PaperQA
				saveHandler={() => {
					toast.success($i18n.t('Settings saved successfully!'));
				}}
			/>
		{/if}
	</div>
</div>
