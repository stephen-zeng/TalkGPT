<script setup>
    defineProps(['item'])
    
</script>
<template>
    <h1>{{ item.title }}</h1>
    
</template>
<style scoped>
    h1 {
        color: black;
        text-align: left;
    }
</style>