export class Player {
    constructor() {
        this.channels = 1;
        this.sampleRate = 24000; 

        this.AudioContext = window.AudioContext || window.webkitAudioContext;
        try {
            this.audioContext = new this.AudioContext({
                sampleRate: this.sampleRate
            });
        } catch (e) {
            console.error('初始化 AudioContext 失败:', e);
            this.audioContext = new this.AudioContext();
            this.sampleRate = this.audioContext.sampleRate; // 更新为实际采样率
        }
        this.nextPlayTime = this.audioContext.currentTime;
        this.isPlaying = false;
        this.audioBufferQueue = [];
    }

    pcm16ToFloat32(pcm16Data) {
        const float32Data = new Float32Array(pcm16Data.length);
        for (let i = 0; i < pcm16Data.length; i++) {
            float32Data[i] = pcm16Data[i] / 32768; 
        }
        return float32Data;
    }

    async realtime(base64Data) {
        try {
            const binaryString = atob(base64Data);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            const pcmData = bytes.buffer;
            const int16Data = new Int16Array(pcmData);
            const float32Data = this.pcm16ToFloat32(int16Data);
            let adjustedPlaybackRate = 1.0;
            if (this.audioContext.sampleRate !== this.sampleRate) {
                adjustedPlaybackRate = this.sampleRate / this.audioContext.sampleRate;
                console.warn(`采样率不匹配：预期 ${this.sampleRate} Hz, 实际 ${this.audioContext.sampleRate} Hz，调整播放速率为 ${adjustedPlaybackRate}`);
            }
            const audioBuffer = this.audioContext.createBuffer(
                this.channels,
                float32Data.length / this.channels,
                this.audioContext.sampleRate 
            );
            for (let channel = 0; channel < this.channels; channel++) {
                const channelData = audioBuffer.getChannelData(channel);
                for (let i = channel; i < float32Data.length; i += this.channels) {
                    channelData[i / this.channels] = float32Data[i];
                }
            }
            this.audioBufferQueue.push({ audioBuffer, playbackRate: adjustedPlaybackRate });
            if (!this.isPlaying) {
                this.isPlaying = true;
                this.play();
            }
        } catch (error) {
            console.error('Audio processing error: ', error);
        }
    }

    async play() {
        while (this.audioBufferQueue.length > 0) {
            const { audioBuffer, playbackRate } = this.audioBufferQueue.shift();
            const source = this.audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(this.audioContext.destination);
            if (playbackRate !== 1.0) {
                source.playbackRate.value = playbackRate;
            }
            const currentTime = this.audioContext.currentTime;
            if (this.nextPlayTime < currentTime) {
                this.nextPlayTime = currentTime;
            }
            source.start(this.nextPlayTime);
            this.nextPlayTime += audioBuffer.duration / (playbackRate || 1.0);
        }
        this.isPlaying = false;
    }

    clear() {
        if (this.audioContext && this.audioContext.state !== 'closed') {
            this.audioContext.close();
        }
        this.audioContext = new this.AudioContext({
            sampleRate: this.sampleRate
        });
        this.nextPlayTime = this.audioContext.currentTime;
        this.isPlaying = false;
        this.audioBufferQueue = [];
    }
}
