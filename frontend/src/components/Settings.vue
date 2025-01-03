<script setup>
    import { ref, inject, onMounted } from 'vue';
    const dialogStatus = ref(false);
    const key = ref('');
    const model = ref('gpt-4o-mini-realtime-preview-2024-12-17');
    const modelBtn = ref('Model: gpt-4o-mini-realtime-preview-2024-12-17');
    const socket = inject('socket');
    
    function openDialog() {
        modelBtn.value = 'Model: ' + model.value;
        key.value = '';
        dialogStatus.value = true;
    }
    function cancelDialog() {
        key.value = '';
        dialogStatus.value = false;
    }
    function submit() {
        console.log(key.value)
        console.log(model.value)
        socket.emit('openai', 'setConfig',
            {
                key: key.value,
                model: model.value
            }
        )
        cancelDialog();
    }

    function setModel(newModel) {
        model.value = newModel;
        modelBtn.value = 'Model: ' + model.value;
    }

    onMounted(
        ()=>{
            socket.on('openai_response',
                (data)=>{
                    if (data=='unConfigured')
                    dialogStatus.value = true;
                }
            )
        }
    )
</script>
<template>
    <mdui-dialog :open=dialogStatus @overlay-click="cancelDialog()"
    icon="settings" headline="Settings" close-on-overlay-click>
        <mdui-text-field label="OpenAI API Key" variant="outlined" clearable
        :value="key" @input="key=$event.target.value"></mdui-text-field>
        <mdui-dropdown trigger="hover" placement="top">
            <mdui-button id="voiceBtn" full-width slot="trigger">{{ modelBtn }}</mdui-button>
            <mdui-menu>
                <mdui-menu-item @click="setModel('gpt-4o-realtime-preview-2024-12-17')">gpt-4o-realtime-preview-2024-12-17</mdui-menu-item>
                <mdui-menu-item @click="setModel('gpt-4o-mini-realtime-preview-2024-12-17')">gpt-4o-mini-realtime-preview-2024-12-17</mdui-menu-item>
            </mdui-menu>
        </mdui-dropdown>
        <mdui-button slot="action" variant="outlined" @click="cancelDialog">Cancel</mdui-button>
        <mdui-button slot="action" @click="submit">Done</mdui-button>
    </mdui-dialog>
    <mdui-button-icon icon="settings" @click="openDialog"></mdui-button-icon>
</template>
<style scope>
</style>