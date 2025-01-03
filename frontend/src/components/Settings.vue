<script setup>
    import { ref, inject, onMounted } from 'vue';
    const dialogStatus = ref(false);
    const key = ref('');
    const socket = inject('socket');
    
    function openDialog() {
        key.value = '';
        dialogStatus.value = true;
    }
    function cancelDialog() {
        key.value = '';
        dialogStatus.value = false;
    }
    function submit() {
        console.log(key.value)
        if (key.value) socket.emit('openai', 'setConfig',
            {
                key: key.value
            }
        )
        cancelDialog();
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
        <mdui-button slot="action" variant="outlined" @click="cancelDialog">Cancel</mdui-button>
        <mdui-button slot="action" @click="submit">Done</mdui-button>
    </mdui-dialog>
    <mdui-button-icon icon="settings" @click="openDialog"></mdui-button-icon>
</template>
<style scope>
</style>