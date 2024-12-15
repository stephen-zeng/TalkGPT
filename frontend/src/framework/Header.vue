<script setup>
    import { defineEmits, defineProps, ref } from 'vue';
    import AddConversation from '@/components/AddConversation.vue';
    const props = defineProps(['title'])
    const emit = defineEmits(['changeSidebarStatus'])

    function changeSidebarStatus() {
        emit('changeSidebarStatus')
    }
</script>
<template>
    <mdui-top-app-bar variant="center-aligned">
        <mdui-button-icon icon="menu" @click="changeSidebarStatus"></mdui-button-icon>
        <mdui-top-app-bar-title>{{ props.title }}</mdui-top-app-bar-title>
        <AddConversation></AddConversation>
    </mdui-top-app-bar>
</template>