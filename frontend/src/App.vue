<script setup>
	import Header from './framework/Header.vue';
	import Sidebar from './framework/Sidebar.vue';
	import Bottombar from './framework/Bottombar.vue';
	import Conversation from './framework/Conversation.vue';
	import { io } from 'socket.io-client'
	import { ref, onMounted, onBeforeUnmount, onBeforeMount } from 'vue';

	let monitorID;
	const sidebarStatus = ref(false);
	const currentConversation = ref(0);
	const conversations = ref([]);
	const socket = io('http://127.0.0.1:11111');
	const role = ref(false); // 1为GPT，0为用户

	function changeSidebarStatus(way) {
		// console.log(sidebarStatus.value)
		// console.log(document.body.offsetWidth);
		let i = currentConversation.value
		let c = conversations.value
		console.log(c);
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
	function getSocket() {
		console.log("Init WS");
		socket.on('connect',
			()=> {
				console.log("WS Connected");
				socket.emit('get_data');
			}
		);
		socket.on('disconnect',
			()=> {
				console.log("WS Disconnected");
			}
		);
		socket.on('data_response',
			(data)=> {
				console.log("Receiving Data");
				conversations.value.push(data);
				// console.log(conversations.value);
			}
		)
	}

	onMounted(
		()=> {
			monitorID = setInterval(monitor, 100);
			// clearInterval(monitorID);
		}
	);
	onBeforeUnmount (
		()=> {
			if (monitorID) clearInterval(monitorID);
		}
	);
	onBeforeMount(
		()=> {
			getSocket();
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