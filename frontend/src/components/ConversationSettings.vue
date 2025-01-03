<script>
    import { ref, inject, defineProps,defineEmits , onMounted } from 'vue';
    const dialogStatus = ref(false);
    const conversation = ref({});
    const modelBtn = ref('');
    const prop = defineProps(['index']);
    const emit = defineEmits(['del']);
    const socket = inject('socket');

    function openDialog() {
        console.log(prop.index);
        socket.emit('model', 'data', 0);
        modelBtn = 'Model: ' + conversation.value.model;
        dialogStatus.value = true;
    }
    function cancelDialog() {
        dialogStatus.value = false;
        socket.emit('model', 'data', 0);
    }
    function submit() {
        socket.emit('model','editConversation',conversation);
        cancelDialog();
    }
    function deleteConversation() {
        socket.emit('model', 'delConversation',
            {
                uuid: conversation.value.uuid,
            }
        );
        socket.emit('openai', 'disconnect', 0);
        emit('del');
    }
    onMounted(
        ()=>{
            console.log("Hello?");
            socket.on('data_response',
                (data)=>{
                    conversation.value = JSON.parse(data)[prop.index];
                }
            );
        }
    )
</script>
<template>
    <mdui-dialog :open=dialogStatus @overlay-click="cancelDialog()"
    icon="settings" headline="Conversation Settings" close-on-overlay-click>
        <mdui-text-field label="Title" variant="outlined" clearable
        :value="conversation?.title" @input="conversation.title=$event.target.value"></mdui-text-field>
        <mdui-text-field label="Instruction" variant="outlined" clearable
        :value="conversation?.instruction" @input="conversation.instruction=$event.target.value"></mdui-text-field>
        <mdui-slider min="0.6" max="1.2" 
        :value="conversation?.temperature" @input="conversation.temperature=$event.target.value"></mdui-slider>
        <mdui-dropdown trigger="hover" placement="top">
            <mdui-button id="modelBtn" full-width slot="trigger">{{ modelBtn }}</mdui-button>
            <mdui-menu>
                <mdui-menu-item @click="conversation.value.model = 'gpt-4o-realtime-preview-2024-12-17'">gpt-4o-realtime-preview-2024-12-17</mdui-menu-item>
                <mdui-menu-item @click="conversation.value.model = 'gpt-4o-mini-realtime-preview-2024-12-17'">gpt-4o-mini-realtime-preview-2024-12-17</mdui-menu-item>
            </mdui-menu>
        </mdui-dropdown>
        <mdui-button slot="action" variant="outlined" @click="cancelDialog">Cancel</mdui-button>
        <mdui-button slot="action" @click="deleteConversation">Delete</mdui-button>
        <mdui-button slot="action" @click="submit">Done</mdui-button>
    </mdui-dialog>
    <mdui-button-icon icon="settings" @click="openDialog"></mdui-button-icon>
</template>
<style scoped>
#modelBtn {
    margin-top: 1rem;
    margin-bottom: 1rem;
}
</style>