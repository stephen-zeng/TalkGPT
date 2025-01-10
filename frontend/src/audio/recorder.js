// recorder.js

export class Recorder {
    /**
     * 构造函数
     * @param {Object} socket - Socket.IO 客户端连接
     * @param {number} targetSampleRate - 目标采样率，默认24000 Hz
     */
    constructor(socket, targetSampleRate = 24000) {
      if (!socket) {
        throw new Error('Socket.IO 客户端连接实例是必需的。');
      }
      this.socket = socket;
      this.audioContext = null;
      this.mediaStream = null;
      this.processor = null;
      this.isRecording = false;
      this.targetSampleRate = targetSampleRate;
    }
  
    /**
     * 开始录音
     * 请求麦克风权限，设置音频处理节点，并开始发送音频数据
     */
    async start() {
      if (this.isRecording) {
        return;
      }
  
      try {
        // 请求用户麦克风权限
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  
        // 创建音频上下文，尝试设置目标采样率
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
          sampleRate: this.targetSampleRate
        });
  
        // 检查实际采样率
        const actualSampleRate = this.audioContext.sampleRate;
        const needsResampling = actualSampleRate !== this.targetSampleRate;
  
        // 创建源节点（麦克风的音频流）
        const source = this.audioContext.createMediaStreamSource(this.mediaStream);
  
        // 设置缓冲区大小（可以根据需要调整）
        const bufferSize = 4096;
        const numberOfInputChannels = 1;
        const numberOfOutputChannels = 1;
  
        // 创建 ScriptProcessorNode（注意：该节点已被弃用，但目前仍被广泛支持）
        this.processor = this.audioContext.createScriptProcessor(bufferSize, numberOfInputChannels, numberOfOutputChannels);
  
        // 连接节点
        source.connect(this.processor);
        this.processor.connect(this.audioContext.destination);
  
        // 处理音频数据
        this.processor.onaudioprocess = (event) => {
          let inputData = event.inputBuffer.getChannelData(0);
  
          // 如果需要重新采样，则进行处理
          if (needsResampling) {
            inputData = this._resample(inputData, actualSampleRate, this.targetSampleRate);
          }
  
          const pcmData = this._floatTo16BitPCM(inputData);
          const base64Data = this._arrayBufferToBase64(pcmData);
          // 发送到后端
          this.socket.emit('openai', 'addVoice', {
                'audio': base64Data
          });
        };
  
        this.isRecording = true;
      } catch (err) {
        console.error('Recording device error:', err);
        throw err;
      }
    }
  
    /**
     * 停止录音
     * 停止音频处理，断开节点连接，关闭音频上下文，并停止音频流
     */
    stop() {
      if (!this.isRecording) {
        console.warn('录音尚未开始。');
        return;
      }
  
      // 停止音频处理
      if (this.processor) {
        this.processor.disconnect();
        this.processor.onaudioprocess = null;
        this.processor = null;
      }
  
      if (this.audioContext) {
        this.audioContext.close();
        this.audioContext = null;
      }
  
      if (this.mediaStream) {
        // 停止所有音轨
        this.mediaStream.getTracks().forEach(track => track.stop());
        this.mediaStream = null;
      }
  
      this.isRecording = false;
    }
  
    /**
     * 将浮点数 PCM 数据转换为 16 位 PCM
     * @private
     * @param {Float32Array} floatBuffer - 浮点数 PCM 数据
     * @returns {ArrayBuffer} - 16 位 PCM 数据
     */
    _floatTo16BitPCM(floatBuffer) {
      const buffer = new ArrayBuffer(floatBuffer.length * 2);
      const view = new DataView(buffer);
      for (let i = 0; i < floatBuffer.length; i++) {
        let s = Math.max(-1, Math.min(1, floatBuffer[i]));
        s = s < 0 ? s * 0x8000 : s * 0x7FFF;
        view.setInt16(i * 2, s, true); // littleEndian
      }
      return buffer;
    }
  
    /**
     * 将 ArrayBuffer 转换为 Base64 字符串
     * @private
     * @param {ArrayBuffer} buffer - 要转换的 ArrayBuffer
     * @returns {string} - Base64 编码字符串
     */
    _arrayBufferToBase64(buffer) {
      let binary = '';
      const bytes = new Uint8Array(buffer);
      const len = bytes.byteLength;
      for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      return window.btoa(binary);
    }
  
    /**
     * 重新采样音频数据到目标采样率
     * @private
     * @param {Float32Array} input - 输入音频数据
     * @param {number} inputSampleRate - 输入采样率
     * @param {number} outputSampleRate - 目标采样率
     * @returns {Float32Array} - 重新采样后的音频数据
     */
    _resample(input, inputSampleRate, outputSampleRate) {
      const ratio = outputSampleRate / inputSampleRate;
      const newLength = Math.round(input.length * ratio);
      const resampled = new Float32Array(newLength);
  
      for (let i = 0; i < newLength; i++) {
        const index = i / ratio;
        const lower = Math.floor(index);
        const upper = lower + 1;
        const weight = index - lower;
  
        if (upper < input.length) {
          resampled[i] = input[lower] * (1 - weight) + input[upper] * weight;
        } else {
          resampled[i] = input[lower];
        }
      }
  
      return resampled;
    }
  }
  
  // 导出 Recorder 类（如果使用模块系统）
  // 如果不使用模块系统，可以忽略以下行
  // export default Recorder;
  