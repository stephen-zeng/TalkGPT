<script setup>
	import Header from './framework/Header.vue';
	import Sidebar from './framework/Sidebar.vue';
	import Bottombar from './framework/Bottombar.vue';
	import Conversation from './framework/Conversation.vue';
	import { ref, onMounted, onBeforeUnmount, onBeforeMount, inject } from 'vue';

	let monitorID;
	const sidebarStatus = ref(false);
	const currentConversation = ref(0);
	const conversations = ref([]);
	const vad = ref(false);
	const socket = inject('socket');
	const player = inject('player');
	// const role = ref(false); // 1为GPT，0为用户

	function changeSidebarStatus(way) {
		// console.log(sidebarStatus.value)
		// console.log(document.body.offsetWidth);
		// let i = currentConversation.value
		// let c = conversations.value
		// console.log(c);
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
		socket.emit('openai', 'disconnect', 0);
		currentConversation.value = index;
		if (document.body.offsetWidth >= 850) sidebarStatus.value = true;
		else sidebarStatus.value = false;
	}
	function changeVad(newMode) {
		vad.value = newMode;
	}
	function deleteConversation() {
		if (currentConversation.value != 0) currentConversation.value--;
	}
	function getSocket() {
		// console.log("Init WS");
		socket.on('connect',
			()=> {
				// console.log("WS Connected");
				socket.emit('model', 'data', 0);
				// socket.emit('openai', 'setConfig',
				// 	{
				// 		key: "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",
				// 		model: "gpt-4o-mini-realtime-preview-2024-12-17"
				// 	}
				// )
			}
		);
		socket.on('disconnect',
			()=> {
				console.log("WS Disconnected");
			}
		);
		socket.on('data_response',
			(data)=> {
				// console.log("Receiving Data");
				conversations.value = JSON.parse(data);
			}
		)
	}

	onMounted(
		()=> {
			monitorID = setInterval(monitor, 100);
			player.connect();
		}
	);
	onBeforeUnmount (
		()=> {
			socket.emit('openai', 'disconnect', 0);
			if (monitorID) clearInterval(monitorID);
			player.interrupt();
			socket.close();
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
		<Bottombar :uuid="conversations[currentConversation]?.uuid"
		@del="deleteConversation()" @vad="changeVad"></Bottombar>
		<Header @changeSidebarStatus="changeSidebarStatus(true)"
		@addConversation="currentConversation = conversations.length" 
		:title="conversations[currentConversation]?.title"></Header>
		<Sidebar :sidebarStatus="sidebarStatus" 
		@closeSidebar="changeSidebarStatus(false)"
		@chooseConversation="updateConversation"
		:conversations="conversations"></Sidebar>
		<Conversation :conversation="vad ? conversations[currentConversation]?.vad : conversations[currentConversation]?.manual" v-show="conversations[currentConversation]"></Conversation>
	</mdui-layout>
</template>
<style scoped>
</style>