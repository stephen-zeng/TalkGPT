<script setup>
    import { ref, defineProps, defineEmits, inject, onMounted } from 'vue';
    import ConversationSettings from '../components/ConversationSettings.vue'

    const keyboardStatus = ref(false);
    const voiceStatus = ref(false);
    const vadEnabled = ref(false);
    const vadIcon = ref('voice_over_off');
    const vadMessage = ref('');
    const content = ref('');
    const prop = defineProps(['uuid', 'index']);
    const emit = defineEmits(['del', 'vad'])
    const socket = inject('socket');
    const recorder = inject('recorder');
    const connecting = ref(false);
    const disconnected = ref(true);

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
            socket.emit('model', 'newMemory', 
                {
                    role: false,
                    uuid: prop.uuid,
                    message: content.value,
                    voice: "Should be a https link",
                },
                typ='text',
                audio=0,
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
        socket.emit('model', 'newMemory',
            {
                role: false,
                uuid: prop.uuid,
                message: "Should from Whisper",
                voice: "Should be a https link",
            },
            typ='voice',
            audio=0,
        );
        cancelVoice();
    }
    
    function setVad() {
        if (vadIcon.value == 'filled') { // 停止VAD
            vadIcon.value = 'standard';
            vadMessage.value = 'Stop VAD';
            vadEnabled.value = false;
            emit('vad', false);
        } else { // 开始VAD
            vadIcon.value = 'filled';
            vadEnabled.value = true;
            vadMessage.value = 'Stop VAD';
            emit('vad', true);
        }
    }
    function connect(operation) {
        if (operation == 'icon') {
            if (disconnected.value) return "play_arrow";
            else return "stop";
        } else if (operation == 'btn') {
            connecting.value = true;
            if (disconnected.value) {
                socket.emit('openai', 'connect', 0);
            } else {
                socket.emit('openai', 'disconnect', 0);
            }
        }
    }

    onMounted(
        ()=>{
            socket.on('openai_response', 
                (data)=>{
                    if (data=='connected') {
                        connecting.value = false;
                        disconnected.value = false;
                    } else if (data=='disconnected') {
                        connecting.value = false;
                        disconnected.value = true;
                    } else if (data=='unConfigured') {
                        connecting.value = false;
                    }
                }
            )
        }
    )

</script>
<template>
    <div style="overflow: hidden;">
        <mdui-bottom-app-bar style="justify-content: center;" :hide="uuid ? false : true"
        scroll-behavior="hide"
        scroll-threshold="30"
        scroll-target=".content">
            <mdui-tooltip content="Connect to OpenAI">
                <mdui-button-icon :disabled=connecting
                :icon="connect('icon')" @click="connect('btn')"></mdui-button-icon>
            </mdui-tooltip>
            <mdui-tooltip content="Type a message">
                <mdui-button-icon :disabled="vadEnabled | disconnected"
                icon="keyboard" @click="openKeyboard">
            </mdui-button-icon></mdui-tooltip>
            <mdui-tooltip content="Say a message">
                <mdui-button-icon :disabled="vadEnabled | disconnected"
                icon="mic" @click="openVoice"></mdui-button-icon>
            </mdui-tooltip>
            <!-- <mdui-tooltip content="Talk with GPT"><mdui-button-icon :variant="vadIcon" :disabled="disconnected"
            icon='record_voice_over' @click="setVad"></mdui-button-icon></mdui-tooltip> -->
            <mdui-tooltip content="Configure this conversation">
                <ConversationSettings :index="index" @del="emit('del')"></ConversationSettings>
            </mdui-tooltip>
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