<script setup>
    import { defineEmits, defineProps, inject } from 'vue';
    const props = defineProps(['sidebarStatus', 'conversations']);
    const emit = defineEmits(['closeSidebar', 'chooseConversation']);
    const socket = inject('socket');
    function chooseConversation(index) {
        emit('chooseConversation', index);
    }
</script>
<template> 
    <mdui-navigation-drawer @close="emit('closeSidebar')"
    :open=sidebarStatus close-on-esc close-on-overlay-click
    class="conversations">
			<mdui-list v-for="(conversation, index) in props.conversations">
                <mdui-list-item rounded @click="chooseConversation(index)">{{ conversation.title }}</mdui-list-item>
			</mdui-list>
	</mdui-navigation-drawer>
</template>
<style scoped>
mdui-navigation-drawer {
    box-shadow: 0px 0px 10px #000000;
    margin-bottom: 5rem;
}
</style>