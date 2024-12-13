<script setup>
    // import 'mdui/components/icon.js';
    import { defineEmits, reactive, ref } from 'vue'
    const emit = defineEmits(['addItem'])

    const dialogOpenStatus = ref(false)
    const newTitle = ref('')
    const newContent = ref('')
    const newItem = reactive({
        title: '',
        content: ''
    })

    function clearOldItem() {
        newTitle.value = '';
        newContent.value = '';
    }
    function changeDialogOpenStatusToTrue() {
        clearOldItem()
        dialogOpenStatus.value = true;
    }
    function cancelDialog() {
        clearOldItem()
        dialogOpenStatus.value = false;
    }
    function submit() {
        newItem.title = newTitle.value;
        newItem.content = newContent.value;
        cancelDialog();
        // console.log(newItem);
        emit('addItem', newItem);
    }
</script>
<template>
    <mdui-dialog :open=dialogOpenStatus>
        <h1>New Item</h1>
        <mdui-text-field label="Title" variant="outlined" :value="newTitle" @input="newTitle=$event.target.value"></mdui-text-field>
        <mdui-text-field autosize label="Content" variant="filled" :value="newContent" @input="newContent=$event.target.value"></mdui-text-field>
        <mdui-button variant="outlined" @click="cancelDialog">Cancel</mdui-button>
        <mdui-button @click="submit">Done</mdui-button>
    </mdui-dialog>
    <mdui-fab extended icon="add" @click="changeDialogOpenStatusToTrue">Add</mdui-fab>
</template>
<style scoped>
	mdui-fab {
		position: fixed;
		bottom: 10%;
		right: 10%;
	}
    mdui-dialog h1 {
        color: black;
        margin-bottom: 1rem;
    }
</style>