<script lang="ts">
    import { toast } from 'svelte-sonner';
    import { createEventDispatcher, onMount, getContext } from 'svelte';
    const dispatch = createEventDispatcher();

    import { getBackendConfig } from '$lib/apis';
    import {
        getPaperQAConfig,
        updatePaperQAConfig,
    } from '$lib/apis/paperqa';
    import { config } from '$lib/stores';

    import SensitiveInput from '$lib/components/common/SensitiveInput.svelte';

    import type { Writable } from 'svelte/store';
    import type { i18n as i18nType } from 'i18next';

    const i18n = getContext<Writable<i18nType>>('i18n');

    export let saveHandler: () => void;

    // PaperQA settings variables
    let PAPERQA_API_KEY = '';
    let PAPERQA_ENGINE = '';
    let PAPERQA_MODEL = '';
    let PAPERQA_OTHER_SETTING = '';

    const updateConfigHandler = async () => {
        const res = await updatePaperQAConfig(localStorage.token, {
            apiKey: PAPERQA_API_KEY,
            engine: PAPERQA_ENGINE,
            model: PAPERQA_MODEL,
            otherSetting: PAPERQA_OTHER_SETTING
        });

        if (res) {
            saveHandler();
            getBackendConfig()
                .then(config.set)
                .catch(() => {});
        }
    };

    onMount(async () => {
        const res = await getPaperQAConfig(localStorage.token);

        if (res) {
            PAPERQA_API_KEY = res.apiKey;
            PAPERQA_ENGINE = res.engine;
            PAPERQA_MODEL = res.model;
            PAPERQA_OTHER_SETTING = res.otherSetting;
        }
    });
</script>

<form
    class="flex flex-col h-full justify-between space-y-3 text-sm"
    on:submit|preventDefault={async () => {
        await updateConfigHandler();
        dispatch('save');
    }}
>
    <div class="space-y-3 overflow-y-scroll scrollbar-hidden h-full">
        <div class="flex flex-col gap-3">
            <div>
                <div class="mb-1 text-sm font-medium">{$i18n.t('PaperQA Settings')}</div>

                <div class="mt-1 flex gap-2 mb-1">
                    <SensitiveInput
                        placeholder={$i18n.t('API Key')}
                        bind:value={PAPERQA_API_KEY}
                        required
                    />
                </div>

                <div class="py-0.5 flex w-full justify-between">
                    <div class="self-center text-xs font-medium">{$i18n.t('Engine')}</div>
                    <div class="flex items-center relative">
                        <select
                            class="dark:bg-gray-900 cursor-pointer w-fit pr-8 rounded px-2 p-1 text-xs bg-transparent outline-none text-right"
                            bind:value={PAPERQA_ENGINE}
                            placeholder="Select an engine"
                        >
                            <option value="engine1">Engine 1</option>
                            <option value="engine2">Engine 2</option>
                        </select>
                    </div>
                </div>

                <div class="mt-2 mb-1 text-sm font-medium">{$i18n.t('Model')}</div>
                <div class="flex w-full">
                    <div class="flex-1">
                        <input
                            list="model-list"
                            class="w-full rounded-lg py-2 px-4 text-sm bg-gray-50 dark:text-gray-300 dark:bg-gray-850 outline-none"
                            bind:value={PAPERQA_MODEL}
                            placeholder="Select a model"
                        />
                        <datalist id="model-list">
                            <option value="model1" />
                            <option value="model2" />
                        </datalist>
                    </div>
                </div>

                <!-- Add more settings fields as needed -->

            </div>
        </div>
    </div>
    <div class="flex justify-end text-sm font-medium">
        <button
            class="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-gray-100 transition rounded-lg"
            type="submit"
        >
            {$i18n.t('Save')}
        </button>
    </div>
</form>
