<script setup>
	import Header from './framework/Header.vue';
	import Sidebar from './framework/Sidebar.vue';
	import Bottombar from './framework/Bottombar.vue';
	import Conversation from './framework/Conversation.vue';
	import { ref, onMounted, onBeforeMount } from 'vue';

	let monitorID;
	const sidebarStatus = ref(false);
	const currentConversation = ref(0);
	const conversations = [ // true->GPT; false->User;
		{
			title: 'Title 1',
			id: '0',
			conversation: [
				{
					role: true,
					message: 'asdjfhalskjdhlkj'
				},
				{
					role: false,
					message: 'oooooooooooooooo7y2348975y23487'
				},
			]
		},
		{
			title: 'Title 2',
			id: '1',
			conversation: [
				{
					role: true,
					message: 'asdjfhalskjdhlkj'
				},
				{
					role: false,
					message: 'ffffffffffffffff2348975y23487'
				},
			]
		},
		{
			title: 'Title 3',
			id: '2',
			conversation: [
				{
					role: true,
					message: 'asdjfhalskjdhlkj'
				},
				{
					role: false,
					message: 'bbbbbbbbbbbbbf267g345gy34f346yf34y6f346f348975y23487'
				},
			]
		},
		{
			title: 'Title 4',
			id: '3',
			conversation: [
				{
					role: true,
					message: 'asdjfhalskjdhlkj'
				},
				{
					role: false,
					message: 'aaaaaaaaaaaaaaa37y2348975y23487'
				},
			]
		},
	]
	const role = ref(false); // 1为GPT，0为用户

	function changeSidebarStatus(way) {
		// console.log(sidebarStatus.value)
		// console.log(document.body.offsetWidth);
		if (way) {
			if (sidebarStatus.value) sidebarStatus.value = false;
			else sidebarStatus.value = true;
			clearInterval(monitorID);
		} else { // 这是我找到的比较舒服的自动启停的逻辑了
			if (sidebarStatus.value) monitorID = setInterval(monitor, 100);
			sidebarStatus.value = false;
		}
    }
	function monitor() {
		if (document.body.offsetWidth >= 850) sidebarStatus.value = true;
		else sidebarStatus.value = false;
	}
	function updateConversation(index) {
		// console.log(index);
		currentConversation.value = index;
		if (document.body.offsetWidth >= 850) sidebarStatus.value = true;
		else sidebarStatus.value = false;
	}

	onMounted(
		()=> {
			monitorID = setInterval(monitor, 100);
			// clearInterval(monitorID);
		}
	);
	onBeforeMount (
		()=> {
			if (monitorID) clearInterval(monitorID);
		}
	)
	

</script>
<template>
	<mdui-layout full-height>
		<Bottombar></Bottombar>
		<Header @changeSidebarStatus="changeSidebarStatus(true)" 
		:title="conversations[currentConversation].title"></Header>
		<Sidebar :sidebarStatus="sidebarStatus" 
		@closeSidebar="changeSidebarStatus(false)"
		@chooseConversation="updateConversation"
		:conversations="conversations"></Sidebar>
		<Conversation :conversation="conversations[currentConversation].conversation"></Conversation>
	</mdui-layout>
</template>
<style scoped>
</style>