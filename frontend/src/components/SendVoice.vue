<script setup>
    import { ref, defineProps,inject } from 'vue';
    import { Recorder } from '@/audio/recorder';
    
    const socket = inject('socket');
    const prop = defineProps(['disable', 'uuid']);
    const dialogStatus = ref(false);
    const recorder = new Recorder();
    let audioData;
    
    async function openDialog() {
        dialogStatus.value = true;
        await recorder.start();
    }
    async function cancelDialog() {
        dialogStatus.value = false;
        audioData = await recorder.stop();
        console.log('Base64 Encoded Audio:', audioData); // 在这里输出 Base64 编码
    }
    function submit() {
        socket.emit('model', 'newMemory',
            {
                role: false,
                uuid: prop.uuid,
                message: "Should from Whisper",
                voice: "Should be a https link",
                type: 'audio', //g711_alaw, base64
                audio: audioData,
            }
        );
        cancelDialog();
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
    :disabled="false"
    icon="mic" 
    @click="openDialog"></mdui-button-icon>
</template>
<stype scoped>
</stype>