<script setup>
    import { ref, defineProps, defineEmits, inject, onMounted } from 'vue';
    import ConversationSettings from '@/components/ConversationSettings.vue'
    import SendText from '@/components/SendText.vue';
    import SendVoice from '@/components/SendVoice.vue';

    const vadEnabled = ref(false);
    const prop = defineProps(['uuid', 'index']);
    const emit = defineEmits(['del', 'vad'])
    const socket = inject('socket');
    const connecting = ref(false);
    const disconnected = ref(true);

    function connect(operation) {
        // console.log(prop.uuid)
        if (operation == 'icon') {
            if (disconnected.value) return "play_arrow";
            else return "stop";
        } else if (operation == 'btn') {
            connecting.value = true;
            if (disconnected.value) {
                socket.emit('openai', 'connect', 0);
            } else {
                socket.emit('openai', 'disconnect', 0);
            }
        }
    }

    onMounted(
        ()=>{
            socket.on('openai_response', 
                (data)=>{
                    if (data=='connected') {
                        connecting.value = false;
                        disconnected.value = false;
                    } else if (data=='disconnected') {
                        connecting.value = false;
                        disconnected.value = true;
                    } else if (data=='unConfigured') {
                        connecting.value = false;
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
        scroll-target=".conversation">
            <mdui-tooltip content="Connect to OpenAI">
                <mdui-button-icon 
                :disabled=connecting
                :icon="connect('icon')" 
                @click="connect('btn')"></mdui-button-icon>
            </mdui-tooltip>
            <mdui-tooltip content="Type a message">
                <SendText 
                :disable="vadEnabled | disconnected"
                :uuid="prop.uuid"></SendText>
            </mdui-tooltip>
            <mdui-tooltip content="Say a message">
                <SendVoice 
                :disable="vadEnabled | disconnected"
                :uuid="prop.uuid"></SendVoice>
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