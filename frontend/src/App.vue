<script setup>
    import ItemSpace from './framework/ItemSpace.vue';
	import Header from './framework/Header.vue';
	import AddItem from './framework/AddItem.vue';
	import { ref } from 'vue';

	const itemList = ref([])

	function warn(content) {
		window.alert(content);
	}
	function addItem(item) {
		// console.log(item);
		itemList.value.push({
			title: item.title,
			content: item.content,
			preview: item.content.substring(0,15)+'...',
		});
	}
</script>
<template>
	<div class="header">
		<Header></Header>
	</div>
	<div class="item-space">
		<ItemSpace :itemList="itemList"></ItemSpace>
	</div>
	<div class="add-item">
		<AddItem @addItem="addItem"></AddItem>
	</div>
</template>
<style scoped>
	.item-space {
		margin: 0 auto;
		padding: 1rem;
		font-weight: normal;
		text-align: center;
	}
</style>