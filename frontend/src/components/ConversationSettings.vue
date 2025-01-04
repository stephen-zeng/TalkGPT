<script setup>
    import { ref, inject, defineProps,defineEmits , onMounted } from 'vue';
    const dialogStatus = ref(false);
    const conversation = ref({});
    const modelBtn = ref('');
    const prop = defineProps(['index']);
    const emit = defineEmits(['del']);
    const socket = inject('socket');

    function openDialog() {
        // console.log(conversation.value.model);
        socket.emit('model', 'data', 0);
        modelBtn.value = 'Model: ' + conversation.value.model;
        dialogStatus.value = true;
    }
    function cancelDialog() {
        dialogStatus.value = false;
        socket.emit('model', 'data', 0);
    }
    function submit() {
        socket.emit('model','editConversation',conversation.value);
        cancelDialog();
    }
    function deleteConversation() {
        dialogStatus.value = false;
        socket.emit('model', 'delConversation',
            {
                uuid: conversation.value.uuid,
            }
        );
        socket.emit('openai', 'disconnect', 0);
        emit('del');
    }
    function changeModel(newModel) {
        conversation.value.model = newModel;
        modelBtn.value = 'Model: ' + conversation.value.model;
    }
    onMounted(
        ()=>{
            // console.log("Hello?");
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
        <mdui-dropdown trigger="click hover" placement="top">
            <mdui-button id="modelBtn" full-width slot="trigger" variant="outlined">{{ modelBtn }}</mdui-button>
            <mdui-menu>
                <mdui-menu-item @click="changeModel('gpt-4o-realtime-preview-2024-12-17')">gpt-4o-realtime-preview-2024-12-17</mdui-menu-item>
                <mdui-menu-item @click="changeModel('gpt-4o-mini-realtime-preview-2024-12-17')">gpt-4o-mini-realtime-preview-2024-12-17</mdui-menu-item>
            </mdui-menu>
        </mdui-dropdown>
        <mdui-button id="modelBtn" full-width variant="outlined" @click="deleteConversation">Delete</mdui-button>
        <mdui-button slot="action" variant="outlined" @click="cancelDialog">Cancel</mdui-button>
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