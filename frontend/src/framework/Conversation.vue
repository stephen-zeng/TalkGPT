<script setup>
    import Talking from '@/components/Talking.vue';
    import { ref, defineProps } from 'vue';
    const props = defineProps(['conversation']);

</script>
<template>
    <mdui-layout-main class="content">
        <Talking v-for="talking in props.conversation" 
        :talking="talking"></Talking>
        <div class="filling"></div>
	</mdui-layout-main>
</template>
<style scope>
.filling {
    height: 4rem;
}
</style>