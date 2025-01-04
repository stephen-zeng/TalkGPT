export class Recorder {
    constructor() {
        this.mediaRecorder = null;
        this.recordedChunks = [];
        this.audioStream = null;
    }

    async start() {
        this.audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(this.audioStream);
        this.mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                this.recordedChunks.push(event.data);
            }
        };
        this.recordedChunks = [];
        this.mediaRecorder.start();
    }

    async stop() {
        return new Promise((resolve, reject) => {
            this.mediaRecorder.onstop = async () => {
                const blob = new Blob(this.recordedChunks, { type: 'audio/webm' });
                const arrayBuffer = await blob.arrayBuffer();
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
                const pcmData = audioBuffer.getChannelData(0);
                const alawData = this.pcmToAlaw(pcmData);
                const base64String = this.arrayBufferToBase64(alawData.buffer);
                this.audioStream.getTracks().forEach(track => track.stop());
                resolve(base64String);
            };
            this.mediaRecorder.stop();
        });
    }

    pcmToAlaw(pcmSamples) {
        const alawSamples = new Int8Array(pcmSamples.length);
        for (let i = 0; i < pcmSamples.length; i++) {
            // 将浮点数转换为 16 位整数
            const pcmVal = Math.max(-1, Math.min(1, pcmSamples[i])) * 32767;
            alawSamples[i] = this.linearToAlaw(pcmVal);
        }
        return alawSamples;
    }

    linearToAlaw(sample) {
        const ALAW_MAX = 0x7FFF;
        let compandedValue;
        let sign = (sample >> 8) & 0x80;
        if (sign !== 0) {
            sample = -sample;
        }
        if (sample > ALAW_MAX) {
            sample = ALAW_MAX;
        }
        let exponent = 7;
        for (let expMask = 0x4000; (sample & expMask) === 0 && exponent > 0; exponent--, expMask >>= 1) { }
        let mantissa = (sample >> ((exponent === 0) ? 4 : (exponent + 3))) & 0x0F;
        compandedValue = sign | (exponent << 4) | mantissa;
        return compandedValue ^ 0x55;
    }

    arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }
}
