<script setup>
    import { ref, defineProps, defineEmits, inject } from 'vue';

    const keyboardStatus = ref(false);
    const voiceStatus = ref(false);
    const voiceDisable = ref(false);
    const vadIcon = ref('voice_over_off');
    const vadMessage = ref('');
    const content = ref('');
    const prop = defineProps(['uuid']);
    const emit = defineEmits(['del', 'vad'])
    const socket = inject('socket');
    const recorder = inject('recorder');

    function openKeyboard() {
        content.value = '';
        // console.log(prop.uuid);
        keyboardStatus.value = true;
    }
    function cancelKeyboard() {
        content.value = '';
        keyboardStatus.value = false;
    }
    function submitKeyboard() {
        if (content.value) 
            socket.emit('newText', 
                {
                    uuid: prop.uuid,
                    message: content.value,
                }
            )
        cancelKeyboard();
    }

    function openVoice() {
        voiceStatus.value = true;
        recorder.begin();
        recorder.record((data)=>(socket.emit('audioBuff', data.mono)));
    }
    function cancelVoice() {
        voiceStatus.value = false;
        recorder.end();
    }
    function submitVoice() {
        socket.emit('newVoice',
            {
                uuid: prop.uuid,
                voice: "Should be a https link"
            }
        );
        cancelVoice();
    }
    
    function setVad() {
        if (vadIcon.value == 'filled') { // 停止VAD
            vadIcon.value = 'standard';
            vadMessage.value = 'Stop VAD';
            voiceDisable.value = false;
            emit('vad', false);
        } else { // 开始VAD
            vadIcon.value = 'filled';
            voiceDisable.value = true;
            vadMessage.value = 'Stop VAD';
            emit('vad', true);
        }
    }
    function deleteConversation() {
        socket.emit('deleteConversation',
            {
                uuid: prop.uuid
            }
        );
        emit('del');
    }

</script>
<template>
    <div style="overflow: hidden;">
        <mdui-bottom-app-bar style="justify-content: center;" :hide="uuid ? false : true"
        scroll-behavior="hide"
        scroll-threshold="30"
        scroll-target=".content">
            <mdui-tooltip content="Type a message"><mdui-button-icon :disabled=voiceDisable
            icon="keyboard" @click="openKeyboard"></mdui-button-icon></mdui-tooltip>
            <mdui-tooltip content="Say a message"><mdui-button-icon :disabled=voiceDisable
            icon="mic" @click="openVoice"></mdui-button-icon></mdui-tooltip>
            <mdui-tooltip content="Talk with GPT"><mdui-button-icon :variant=vadIcon 
            icon='record_voice_over' @click="setVad"></mdui-button-icon></mdui-tooltip>
            <mdui-tooltip content="Delete this conversation"><mdui-button-icon
                icon="delete" @click="deleteConversation"></mdui-button-icon></mdui-tooltip>
        </mdui-bottom-app-bar>
    </div>
    <mdui-dialog :open=keyboardStatus id="keyboard" @close="cancelKeyboard"
    icon="keyboard" headline="Type a message" close-on-esc close-on-overlay-click>
        <mdui-text-field label="Content" variant="outlined" autosize clearable
        :value="content" @input="content=$event.target.value"></mdui-text-field>
        <mdui-button slot="action" variant="outlined" @click="cancelKeyboard">Cancel</mdui-button>
        <mdui-button slot="action" @click="submitKeyboard">Send</mdui-button>
    </mdui-dialog>
    <mdui-dialog :open=voiceStatus id="voice" close-on-esc close-on-overlay-click
    icon="mic" headline="Say a message" description="60s Max" @close="cancelVoice">
        <h1 id="timer">Recording</h1>
        <!-- <mdui-linear-progress value="0.5"></mdui-linear-progress> -->
        <mdui-linear-progress></mdui-linear-progress>
        <mdui-button slot="action" variant="outlined" @click="cancelVoice">Cancel</mdui-button>
        <mdui-button slot="action" @click="submitVoice">Send</mdui-button>
    </mdui-dialog>
</template>
<style scope>
mdui-bottom-app-bar mdui-button-icon {
    margin-left: 1rem;
    margin-right: 1rem;
}
#keyboard mdui-text-field {
    width: 30rem;
}
</style>