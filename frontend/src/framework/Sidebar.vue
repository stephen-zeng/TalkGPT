<script setup>
    import { defineEmits, ref } from 'vue';
    defineProps(['sidebarStatus']);
    const emit = defineEmits(['closeSidebar']);
    function closeSidebar() {
        emit('closeSidebar');
    }
</script>
<template> 
    <mdui-navigation-drawer @close="closeSidebar"
    :open="sidebarStatus" close-on-esc close-on-overlay-click
    class="example-navigation-drawer">
			<mdui-list>
                <mdui-list-item rounded>Navigation drawer</mdui-list-item>
                <mdui-list-item rounded>Navigation drawer</mdui-list-item>
                <mdui-list-item rounded>Navigation drawer</mdui-list-item>
                <mdui-list-item rounded>Navigation drawer</mdui-list-item>
                <mdui-list-item rounded>Navigation drawer</mdui-list-item>
                <mdui-list-item rounded>Navigation drawer</mdui-list-item>
                <mdui-list-item rounded>Navigation drawer</mdui-list-item>
                <mdui-list-item rounded>Navigation drawer</mdui-list-item>
			</mdui-list>
	</mdui-navigation-drawer>
</template>
<style scoped>
    
</style>