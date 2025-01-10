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
	function changeConversation(index) {
		currentConversation.value = index;
		socket.emit('openai', 'change', conversations.value[currentConversation.value]);
		if (document.body.offsetWidth >= 850) sidebarStatus.value = true;
		else sidebarStatus.value = false;
	}
	function deleteConversation() {
		if (currentConversation.value != 0) currentConversation.value--;
		if (conversations.value.length)
			socket.emit('openai', 'change', conversations.value[currentConversation.value])
	}
	function changeVad(newMode) {
		vad.value = newMode;
	}
	function getSocket() {
		socket.on('connect',
			()=> {
				console.log("WS Connected");
				socket.emit('model', 'data', 0);
				socket.emit('openai', 'setConfig',
					{
						key: "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",
					}
				)
			}
		);
		socket.on('disconnect',
			()=> {
				console.log("WS Disconnected");
			}
		);
		socket.on('data_response',
			(data)=> {
				conversations.value = JSON.parse(data);
			}
		)
		socket.on('audio',
			(data)=> {
				if (data['type']=='newAudio') {
					player.clear();
				} else if (data['type']=='addAudio') {
					player.realtime(data['audio']);
				}
			}
		)
	}

	onMounted(
		()=> {
			monitorID = setInterval(monitor, 100);
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
		<Header @changeSidebarStatus="changeSidebarStatus(true)"
		@addConversation="currentConversation = conversations.length" 
		:title="conversations[currentConversation]?.title"></Header>
		<Bottombar :uuid="conversations[currentConversation]?.uuid"
		:index="currentConversation"
		@del="deleteConversation()" @vad="changeVad"></Bottombar>
		<Sidebar :sidebarStatus="sidebarStatus" 
		@closeSidebar="changeSidebarStatus(false)"
		@chooseConversation="changeConversation"
		:conversations="conversations"></Sidebar>
		<Conversation :memory="conversations[currentConversation]?.memory"></Conversation>
	</mdui-layout>
</template>
<style scoped>
</style>