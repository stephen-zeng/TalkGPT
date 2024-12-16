<script setup>
    import { ref } from 'vue';
    const dialogStatus = ref(false);
    const key = ref('');
    const newKey = ref('');
    
    function openDialog() {
        newKey.value = '';
        dialogStatus.value = true;
    }
    function cancelDialog() {
        newKey.value = '';
        dialogStatus.value = false;
    }
    function submit() {
        key.value = newKey.value;
        cancelDialog();
    }
</script>
<template>
    <mdui-dialog :open=dialogStatus @overlay-click="cancelDialog()"
    icon="settings" headline="Settings" close-on-overlay-click>
        <mdui-text-field label="OpenAI API Key" variant="outlined" clearable
        :value="newKey" @input="newKey=$event.target.value"></mdui-text-field>
        <mdui-button slot="action" variant="outlined" @click="cancelDialog">Cancel</mdui-button>
        <mdui-button slot="action" @click="submit">Done</mdui-button>
    </mdui-dialog>
    <mdui-button-icon icon="settings" @click="openDialog"></mdui-button-icon>
</template>
<style scope>
</style>