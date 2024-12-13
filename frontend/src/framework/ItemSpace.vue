<script setup>
    import ItemCard from '@/components/ItemCard.vue'
    defineProps(['itemList'])
</script>
<template>
    <!-- <p> {{ itemList }} </p> -->
    <ItemCard v-for="item in itemList" :item="item"></ItemCard>
</template>
<style scoped>

</style>