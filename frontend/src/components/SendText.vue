<script setup>
    import { ref, defineProps,inject } from 'vue';
    
    const socket = inject('socket');
    const prop = defineProps(['disable', 'uuid']);
    const dialogStatus = ref(false);
    const content = ref('')
    
    function openDialog() {
        content.value = '';
        dialogStatus.value = true;
    }
    function cancelDialog() {
        dialogStatus.value = false;
        content.value = '';
    }
    function submit() {
        if (content.value == '') return
        socket.emit('model', 'newMemory',
            {
                role: false,
                uuid: prop.uuid,
                message: content.value,
                voice: 'None',
                serverid: 'None'
            }
        )
        cancelDialog();
    }
</script>
<template>
    <mdui-dialog 
    :open=dialogStatus 
    id="keyboard" 
    @close="cancelDialog"
    icon="keyboard" 
    headline="Send a Text Message" 
    close-on-esc close-on-overlay-click>
        <mdui-text-field 
        label="Content" 
        variant="outlined" 
        autosize clearable
        :value="content" 
        @input="content=$event.target.value"></mdui-text-field>
        <mdui-button 
        slot="action" 
        variant="outlined" 
        @click="cancelDialog">Cancel</mdui-button>
        <mdui-button 
        slot="action" 
        @click="submit">Send</mdui-button>
    </mdui-dialog>
    <mdui-button-icon 
    :disabled="false"
    icon="keyboard" 
    @click="openDialog"></mdui-button-icon>
</template>
<style scope>
#keyboard mdui-text-field {
width: 30rem;
}
</style>