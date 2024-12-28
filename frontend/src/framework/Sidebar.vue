<script setup>
    import { defineEmits, defineProps, ref } from 'vue';
    const props = defineProps(['sidebarStatus', 'conversations']);
    const emit = defineEmits(['closeSidebar', 'chooseConversation']);
</script>
<template> 
    <mdui-navigation-drawer @close="emit('closeSidebar')"
    :open=sidebarStatus close-on-esc close-on-overlay-click
    class="example-navigation-drawer">
			<mdui-list v-for="(conversation, index) in props.conversations">
                <mdui-list-item rounded @click="emit('chooseConversation', index)">{{ conversation.title }}</mdui-list-item>
			</mdui-list>
	</mdui-navigation-drawer>
</template>
<style scoped>
mdui-navigation-drawer {
    box-shadow: 0px 0px 10px #000000;
}
</style>