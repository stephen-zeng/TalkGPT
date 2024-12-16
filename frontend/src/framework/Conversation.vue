<script setup>
    import Talking from '@/components/Talking.vue';
    import { ref, defineProps } from 'vue';
    const props = defineProps(['conversation']);

</script>
<template>
    <mdui-layout-main class="content">
        <Talking v-for="talking in props.conversation" 
        :role="talking.role" 
        :message="talking.message"></Talking>
	</mdui-layout-main>
</template>
<style scope>
</style>