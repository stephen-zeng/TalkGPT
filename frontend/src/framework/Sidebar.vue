<script setup>
    import { defineEmits, defineProps, ref } from 'vue';
    const props = defineProps(['sidebarStatus', 'conversations']);
    const emit = defineEmits(['closeSidebar', 'chooseConversation']);
    function closeSidebar() { // 0->直接关闭；1->选择了一个东西
        emit('closeSidebar');
    }
    function chooseConversation(index) {
        // console.log(index);
        emit('chooseConversation', index);
        // emit('closeSidebar');
    }
</script>
<template> 
    <mdui-navigation-drawer @close="closeSidebar()"
    :open=sidebarStatus close-on-esc close-on-overlay-click
    class="example-navigation-drawer">
			<mdui-list v-for="(conversation, index) in props.conversations">
                <mdui-list-item rounded @click="chooseConversation(index)">{{ conversation.title }}</mdui-list-item>
			</mdui-list>
	</mdui-navigation-drawer>
</template>
<style scoped>
    
</style>