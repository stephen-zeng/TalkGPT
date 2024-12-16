<script setup>
    import { ref } from 'vue';

    const keyboardStatus = ref(false);
    const voiceStatus = ref(false);
    const voiceDisable = ref(false);
    const vadIcon = ref('voice_over_off');
    const vadMessage = ref('');
    const content = ref('');

    function openKeyboard() {
        content.value = '';
        keyboardStatus.value = true;
    }
    function cancelKeyboard() {
        content.value = '';
        keyboardStatus.value = false;
    }
    function submitKeyboard() {
        cancelKeyboard();
    }

    function openVoice() {
        voiceStatus.value = true;
    }
    function cancelVoice() {
        voiceStatus.value = false;
    }
    function submitVoice() {
        cancelVoice();
    }
    
    function setVad() {
        if (vadIcon.value == 'filled') { // 停止VAD
            vadIcon.value = 'standard';
            vadMessage.value = 'Stop VAD';
            voiceDisable.value = false;
        } else { // 开始VAD
            vadIcon.value = 'filled';
            voiceDisable.value = true;
            vadMessage.value = 'Stop VAD';
        }
    }

</script>
<template>
    <div style="overflow: hidden;">
        <mdui-bottom-app-bar style="justify-content: center;"
        scroll-behavior="hide"
        scroll-threshold="30"
        scroll-target=".content">
            <mdui-tooltip content="Type a message"><mdui-button-icon
            icon="keyboard" @click="openKeyboard"></mdui-button-icon></mdui-tooltip>
            <mdui-tooltip content="Say a message"><mdui-button-icon :disabled=voiceDisable
            icon="mic" @click="openVoice"></mdui-button-icon></mdui-tooltip>
            <mdui-tooltip content="Talk with GPT"><mdui-button-icon :variant=vadIcon 
            icon='record_voice_over' @click="setVad"></mdui-button-icon></mdui-tooltip>
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
        <h1 id="timer">30s</h1>
        <mdui-linear-progress value="0.5"></mdui-linear-progress>
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