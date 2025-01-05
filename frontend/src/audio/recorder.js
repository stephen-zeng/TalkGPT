// recorder.js

export class Recorder {
    constructor(socket) { // 添加 sendInterval 参数，默认100ms
        this.audioContext = null;
        this.socket = socket;
        this.processorNode = null;
        this.stream = null;
        this.sendInterval = 200; // 发送间隔（毫秒）
        this.buffer = []; // 用于存储PCM数据的缓冲区
        this.sendTimer = null; // 发送定时器
    }

    async start() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const pcmProcessorCode = `
                class PCMProcessor extends AudioWorkletProcessor {
                    constructor() {
                        super();
                    }

                    process(inputs, outputs, parameters) {
                        const input = inputs[0];
                        if (input.length > 0) {
                            const channelData = input[0];
                            // 发送一份副本以避免变异
                            this.port.postMessage(new Float32Array(channelData));
                        }
                        return true; // 保持处理器运行
                    }
                }

                registerProcessor('pcm-processor', PCMProcessor);
            `;

            const blob = new Blob([pcmProcessorCode], { type: 'application/javascript' });
            const blobURL = URL.createObjectURL(blob);
            await this.audioContext.audioWorklet.addModule(blobURL);
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const source = this.audioContext.createMediaStreamSource(this.stream);
            this.processorNode = new AudioWorkletNode(this.audioContext, 'pcm-processor');
            source.connect(this.processorNode);
            this.processorNode.port.onmessage = (event) => {
                const pcmData = event.data; // Float32Array
                const alawData = this.pcmToAlaw(pcmData);
                this.buffer.push(alawData); // 将编码后的数据存入缓冲区
            };

            // 启动定时器定期发送缓冲区中的数据
            this.sendTimer = setInterval(() => {
                if (this.buffer.length > 0 && this.socket && this.socket.connected) {
                    // 合并所有缓冲的数据
                    const combined = this.concatenateBuffers(this.buffer);
                    const base64String = this.arrayBufferToBase64(combined.buffer);
                    this.socket.emit('openai', 'addVoice', {
                        'audio': base64String,
                    });
                    console.log('音频块已发送');
                    // 清空缓冲区
                    this.buffer = [];
                }
            }, this.sendInterval);

            console.log('录音已开始');
        } catch (error) {
            console.error('启动录音失败:', error);
        }
    }

    stop() {
        // 断开并关闭AudioContext
        if (this.processorNode) {
            this.processorNode.port.close();
            this.processorNode.disconnect();
            this.processorNode = null;
        }

        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }

        // 停止所有媒体轨道
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }

        // 清除发送定时器
        if (this.sendTimer) {
            clearInterval(this.sendTimer);
            this.sendTimer = null;
        }

        // 清空缓冲区
        this.buffer = [];

        console.log('录音已停止');
    }

    pcmToAlaw(pcmSamples) {
        const alawSamples = new Int8Array(pcmSamples.length);
        for (let i = 0; i < pcmSamples.length; i++) {
            // 将浮点数 [-1, 1] 转换为16-bit PCM
            const pcmVal = Math.max(-1, Math.min(1, pcmSamples[i])) * 32767;
            alawSamples[i] = this.linearToAlaw(pcmVal);
        }
        return alawSamples;
    }

    linearToAlaw(sample) {
        const ALAW_MAX = 0x7FFF;
        let sign = (sample >> 8) & 0x80;
        let magnitude = sample & 0x7FFF;

        if (magnitude > ALAW_MAX) {
            magnitude = ALAW_MAX;
        }

        let exponent = 7;
        for (let expMask = 0x4000; (magnitude & expMask) === 0 && exponent > 0; exponent--, expMask >>= 1) {}
        
        const mantissa = (magnitude >> ((exponent === 0) ? 4 : (exponent + 3))) & 0x0F;
        let compandedValue = sign | (exponent << 4) | mantissa;
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

    concatenateBuffers(buffers) {
        // 计算所有缓冲区的总长度
        let totalLength = 0;
        buffers.forEach(buf => {
            totalLength += buf.length;
        });

        // 创建一个新的缓冲区
        let result = new Int8Array(totalLength);
        let offset = 0;
        buffers.forEach(buf => {
            result.set(buf, offset);
            offset += buf.length;
        });

        return result;
    }
}
