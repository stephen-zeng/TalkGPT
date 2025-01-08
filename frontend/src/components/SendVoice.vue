<script setup>
    import { ref, defineProps, inject, defineEmits } from 'vue';
    import { Recorder } from '@/audio/recorder';
    
    const socket = inject('socket');
    const prop = defineProps(['disable', 'uuid']);
    const emit = defineEmits(['sent']);
    const dialogStatus = ref(false);
    const recorder = new Recorder(socket);
    
    async function openDialog() {
        dialogStatus.value = true;
        socket.emit('openai', 'newVoice', 0)
        await recorder.start();
    }
    async function cancelDialog() {
        dialogStatus.value = false;
        await recorder.stop();
        socket.emit('openai', 'cancelVoice', 0)
    }
    async function submit() {
        dialogStatus.value = false;
        emit('sent');
        await recorder.stop();
        socket.emit('openai', 'sendVoice', 0);
        socket.emit('openai', 'reply', 0);
    }
</script>
<template>
    <mdui-dialog 
    :open=dialogStatus 
    id="voice" 
    icon="mic" 
    headline="Send a voice message" >
        <h1>Recording</h1>
        <!-- <mdui-linear-progress value="0.5"></mdui-linear-progress> -->
        <mdui-linear-progress></mdui-linear-progress>
        <mdui-button slot="action" variant="outlined" @click="cancelDialog">Cancel</mdui-button>
        <mdui-button slot="action" @click="submit">Send</mdui-button>
    </mdui-dialog>
    <mdui-button-icon 
    :disabled="disable"
    icon="mic" 
    @click="openDialog"></mdui-button-icon>
</template>
<stype scoped>
</stype>