<script setup>
    import { ref, defineProps, defineEmits, inject, onMounted } from 'vue';
    import ConversationSettings from '@/components/ConversationSettings.vue'
    import SendText from '@/components/SendText.vue';
    import SendVoice from '@/components/SendVoice.vue';

    const vadEnabled = ref(false);
    const prop = defineProps(['uuid', 'index']);
    const emit = defineEmits(['del', 'vad'])
    const socket = inject('socket');
    const disconnected = ref(true);
    const processing = ref(false);

    function connect(operation) {
        if (operation == 'icon') {
            if (disconnected.value) return "play_arrow";
            else return "stop";
        } else if (operation == 'btn') {
            processing.value = true;
            if (disconnected.value) {
                socket.emit('openai', 'connect', 0);
            } else {
                socket.emit('openai', 'disconnect', 0);
            }
        }
    }

    onMounted(
        ()=>{
            socket.on('backend', 
                (data)=> {
                    if (data=='processing') {
                        processing.value = true;
                    } else if (data=='processed') {
                        processing.value = false;
                    } 
                }
            )
            socket.on('openai_response', 
                (data)=>{
                    if (data=='connected') {
                        processing.value = false;
                        disconnected.value = false;
                    } else if (data=='disconnected') {
                        processing.value = false;
                        disconnected.value = true;
                    } else if (data=='unConfigured') {
                        processing.value = false;
                    }
                }
            )
        }
    )

</script>
<template>
    <div style="overflow: hidden;">
        <mdui-bottom-app-bar 
        style="justify-content: center;"
        scroll-behavior="hide"
        scroll-threshold="30"
        scroll-target=".talkings .conversations">
            <mdui-tooltip content="Connect to OpenAI">
                <mdui-button-icon 
                :disabled="processing"
                :icon="connect('icon')" 
                @click="connect('btn')"></mdui-button-icon>
            </mdui-tooltip>
            <mdui-tooltip content="Type a message">
                <SendText 
                :disable="vadEnabled | disconnected | processing"
                :uuid="prop.uuid"
                @sent="processing = true"></SendText>
            </mdui-tooltip>
            <mdui-tooltip content="Say a message">
                <SendVoice 
                :disable="vadEnabled | disconnected | processing"
                :uuid="prop.uuid"
                @sent="processing = true"></SendVoice>
            </mdui-tooltip>
            <mdui-tooltip content="Configure this conversation">
                <ConversationSettings 
                :index="index" 
                @del="emit('del')"></ConversationSettings>
            </mdui-tooltip>
        </mdui-bottom-app-bar>
    </div>
</template>
<style scope>
mdui-bottom-app-bar mdui-button-icon {
    margin-left: 1rem;
    margin-right: 1rem;
}
</style>