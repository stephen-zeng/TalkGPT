<script setup>
    import { ref, onMounted } from 'vue';
    const props = defineProps(['role', 'message']);
    const text = ref("")
    
    function setRole(role) { // 1为GPT，0为用户
        console.log(text.value);
        if (role) return "https://gh.qwqwq.com.cn/stephen-zeng/img/master/openai.png";
        else return "https://gh.qwqwq.com.cn/stephen-zeng/img/master/user.png";
    }
    function getRole(role) {
        // console.log(message);
        if (role) return "ChatGPT";
        else return "User";
    }

    function setStyle(role) {
        // console.log(vid);
        if (role) return 'left';
        else return 'right';
    }
    
    
</script>
<template>
    <div class="talking" :style="{ 'text-align': setStyle(role) }">
        <mdui-tooltip :content="getRole(role)" :placement="setStyle(!role)">
            <mdui-avatar :src="setRole(role)"></mdui-avatar>
        </mdui-tooltip>
        <mdui-text-field variant="outlined" label="Date" :value="message" readonly>
            <mdui-button-icon slot="end-icon" icon="play_circle"></mdui-button-icon>
        </mdui-text-field>
    </div>
</template>
<style scope>
.talking {
    margin: 1rem;
    /* display: flex; */
    /* align-items: flex-end; */
}
mdui-card {
    margin-left: 1rem;
    margin-right: 1rem;
}
mdui-text-field{
    margin-top: 1rem;
    margin-bottom: 1rem;
}


</style>