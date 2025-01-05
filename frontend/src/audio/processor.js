// processor.js
class PCMProcessor extends AudioWorkletProcessor {
    constructor() {
      super();
      this.bufferSize = 1024; // Adjust the buffer size as needed
      this._buffer = [];
    }
  
    process(inputs, outputs, parameters) {
      const input = inputs[0]; // Get the first input
      if (input.length > 0) {
        const channelData = input[0]; // Get data from the first channel
  
        // Accumulate samples in the buffer
        this._buffer.push(...channelData);
  
        // Check if buffer has enough data to send
        if (this._buffer.length >= this.bufferSize) {
          const samples = this._buffer.slice(0, this.bufferSize);
          this._buffer = this._buffer.slice(this.bufferSize);
  
          // Create a Float32Array from the samples
          const float32Samples = new Float32Array(samples);
  
          // Transfer the data to the main thread
          this.port.postMessage({ samples: float32Samples }, [float32Samples.buffer]);
        }
      }
      return true; // Returning true keeps the processor alive
    }
  }
  
  registerProcessor('pcm-processor', PCMProcessor);
  