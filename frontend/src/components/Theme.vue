<script setup>
    import { ref, onMounted } from 'vue';
    const status = ref(0);

    function getThemeIcon() {
        if (status.value  == 0) return "hdr_auto";
        if (status.value == 1) return "light_mode";
        if (status.value == -1) return "dark_mode";
    }
    function changeTheme() {
        if (status.value == 1) status.value = -1;
        else status.value++;
        setTheme();
    }
    function setTheme() {
        if (status.value == -1) {
            document.documentElement.classList.remove('mdui-theme-light');
            document.documentElement.classList.add('mdui-theme-dark');
        } else if (status.value == 0) {
            document.documentElement.classList.remove('mdui-theme-dark');
            document.documentElement.classList.add('mdui-theme-auto');
        } else if (status.value == 1) {
            document.documentElement.classList.remove('mdui-theme-auto');
            document.documentElement.classList.add('mdui-theme-light');
        }
    }

    onMounted(
        ()=> {
            document.documentElement.classList.add('mdui-theme-auto');
        }
    )    
</script>
<template>
    <mdui-button-icon :icon="getThemeIcon()" @click="changeTheme()"></mdui-button-icon>
</template>
