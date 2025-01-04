<script setup>
    import Talking from '@/components/Talking.vue';
    import { defineProps } from 'vue';
    const props = defineProps(['memory']);

</script>
<template>
    <mdui-layout-main class="conversation">
        <Talking v-for="talking in props.memory" 
        :talking="talking"></Talking>
        <div class="filling"></div>
	</mdui-layout-main>
</template>
<style scope>
.filling {
    height: 4rem;
}
</style>