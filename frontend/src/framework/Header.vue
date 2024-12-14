<script setup>
    import { defineEmits, ref } from 'vue';
    import AddConversation from '@/components/AddConversation.vue';
    

    const emit = defineEmits(['changeSidebarStatus'])

    function changeSidebarStatus() {
        emit('changeSidebarStatus')
    }
</script>
<template>
    <mdui-top-app-bar variant="center-aligned" scroll-behavior="elevate">
        <mdui-button-icon icon="menu" @click="changeSidebarStatus"></mdui-button-icon>
        <mdui-top-app-bar-title>Title</mdui-top-app-bar-title>
        <AddConversation></AddConversation>
    </mdui-top-app-bar>
</template>