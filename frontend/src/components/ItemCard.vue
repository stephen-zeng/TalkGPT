<script setup>
    import ItemDetail from './ItemDetail.vue';
    import { ref } from 'vue';
    defineProps(['item']);

    const dialogOpenStatus = ref(false);

    function warn(content) {
        window.alert("click");
    }
    function openDialog() {
        dialogOpenStatus.value = true;
    }
    function closeDialog() {
        dialogOpenStatus.value = false;
    }
</script>
<template>
    <mdui-dialog :open="dialogOpenStatus">
        <ItemDetail :item="item"></ItemDetail>
        <mdui-button @click="closeDialog">Close</mdui-button>
    </mdui-dialog>
    <mdui-card clickable variant="filled" @click="openDialog">
        <h1>
            {{ item.title }}
        </h1>
        <p>
            {{ item.preview }}
        </p>
    </mdui-card>
</template>
<style scoped>
    mdui-card {
        margin: 1rem;
        width: 15rem;
        height: 10rem;
        background-color: auto;
    }
    mdui-card h1 {
        margin-left: 10%;
        margin-top: 5%;
        text-align: left;
        color: black;
    }
    mdui-card p {
        margin-left: 10%;
        color: black;
        text-align: left;
    }
</style>