<script setup>
	import Header from './framework/Header.vue';
	import Sidebar from './framework/Sidebar.vue';
	import Bottombar from './framework/Bottombar.vue';
	import { ref } from 'vue';

	const sidebarStatus = ref(false);

	function changeSidebarStatus(way) {
		// console.log(sidebarStatus.value)
		if (way) {
			if (sidebarStatus.value) sidebarStatus.value = false;
			else sidebarStatus.value = true;
		} else sidebarStatus.value = false;
    }
	

</script>
<template>
	<mdui-layout full-height>
		<Bottombar></Bottombar>
		<Header @changeSidebarStatus="changeSidebarStatus(true)"></Header>
		<Sidebar :sidebarStatus="sidebarStatus" @closeSidebar="changeSidebarStatus(false)"></Sidebar>
		<mdui-layout-main>
			<h1 style="text-align: center;">Man!</h1>
		</mdui-layout-main>
	</mdui-layout>
</template>
<style scoped>
mdui-layout-main {
	background-color: black
}
</style>