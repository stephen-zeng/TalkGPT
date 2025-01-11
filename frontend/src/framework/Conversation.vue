<script setup>
    import Talking from '@/components/Talking.vue';
    import { defineProps, onMounted, inject } from 'vue';
    const props = defineProps(['memory']);
    const socket = inject('socket');

    onMounted(
        ()=>{
            socket.on('backend',
                (data)=> {
                    if (data=='processing') {
                        const container = document.querySelector('.talkings');
                        container.scrollTop = container.scrollHeight;
                    }
                }
            )
        }
    )
</script>
<template>
    <mdui-layout-main class="talkings">
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