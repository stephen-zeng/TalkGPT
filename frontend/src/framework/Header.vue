<script setup>
    import { defineEmits, defineProps, ref } from 'vue';
    import AddConversation from '@/components/AddConversation.vue';
    import Theme from '@/components/Theme.vue';
    import Settings from '@/components/Settings.vue';
    const props = defineProps(['title'])
    const emit = defineEmits(['changeSidebarStatus'])

    function changeSidebarStatus() {
        emit('changeSidebarStatus')
    }
</script>
<template>
    <mdui-top-app-bar variant="center-aligned">
        <mdui-button-icon icon="menu" @click="changeSidebarStatus"></mdui-button-icon>
        <AddConversation></AddConversation>
        <mdui-top-app-bar-title>{{ props.title }}</mdui-top-app-bar-title>
        <Theme></Theme>
        <Settings></Settings>
    </mdui-top-app-bar>
</template>
<style scope>
mdui-top-app-bar {
    box-shadow: 0px 0px 10px #000000;
}
</style>