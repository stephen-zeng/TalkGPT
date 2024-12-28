<script setup>
    import { defineProps, inject } from 'vue';
    const props = defineProps(['talking']);
    const socket = inject('socket');
    
    function setRole(role) { // 1为GPT，0为用户
        // console.log(text.value);
        if (role) return "https://gh.qwqwq.com.cn/stephen-zeng/img/master/openai.png";
        else return "https://gh.qwqwq.com.cn/stephen-zeng/img/master/user.png";
    }
    function getRole(role) {
        // console.log(message);
        // console.log(props.message);
        // console.log(props.talking.voice);
        if (role) return "ChatGPT";
        else return "User";
    }

    function setStyle(role) {
        // console.log(vid);
        if (role) return 'left';
        else return 'right';
    }

    function playAudio() {
        console.log("play the audio");
    }

    function deleteTalking() {
        // console.log(props.talking.time);
        socket.emit('deleteTalking',
            {
                time: props.talking.time
            }
        )
    }

    function getTime() {
        const isoString = props.talking.time;
        const date = new Date(isoString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        const formattedDate = `${year}-${month}-${day}`;
        const formattedTime = `${hours}:${minutes}:${seconds}`;
        // console.log(`Date: ${formattedDate}`);
        // console.log(`Time: ${formattedTime}`);
        return formattedDate + ' ' + formattedTime;
    }
    
</script>
<template>
    <div class="talking" :style="{ 'text-align': setStyle(talking.role) }">
        <mdui-tooltip :content="getRole(talking.role)" :placement="setStyle(!talking.role)">
            <mdui-avatar :src="setRole(talking.role)"></mdui-avatar>
        </mdui-tooltip>
        <mdui-text-field variant="outlined" :label="getTime()" :value="talking.message" readonly autosize>
            <mdui-button-icon slot="icon" icon="play_circle" 
            v-show="talking.voice" @click="playAudio"></mdui-button-icon>
            <mdui-button-icon slot="end-icon" icon="delete" @click="deleteTalking"></mdui-button-icon>
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