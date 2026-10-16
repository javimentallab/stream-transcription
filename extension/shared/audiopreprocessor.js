// AudioWorklet: passes the audio through unchanged (so it keeps playing), and posts
// 0.5 s chunks of mono 16 kHz float32 audio, which is what WhisperLive expects.
class AudioPreProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.inRate = sampleRate || 48000;
    this.outRate = 16000;
    this.chunk = Math.round(this.inRate * 0.5);
    this.buffer = new Float32Array(this.chunk);
    this.offset = 0;
  }

  process(inputs, outputs) {
    const input = inputs[0];
    const output = outputs[0];
    if (!input || input.length === 0 || !input[0]) return true;

    for (let ch = 0; ch < Math.min(input.length, output.length); ch++) {
      if (input[ch] && output[ch]) output[ch].set(input[ch]);
    }

    let mono = input[0];
    if (input.length > 1) {
      mono = new Float32Array(input[0].length);
      for (let ch = 0; ch < input.length; ch++) {
        const data = input[ch];
        for (let i = 0; i < mono.length; i++) mono[i] += data[i];
      }
      for (let i = 0; i < mono.length; i++) mono[i] /= input.length;
    }

    let pos = 0;
    while (pos < mono.length) {
      const n = Math.min(this.chunk - this.offset, mono.length - pos);
      this.buffer.set(mono.subarray(pos, pos + n), this.offset);
      this.offset += n;
      pos += n;
      if (this.offset === this.chunk) {
        this.port.postMessage(this.downsample(this.buffer));
        this.offset = 0;
      }
    }
    return true;
  }

  // Averages each window of input samples (a cheap low-pass) instead of just picking
  // one sample out of every three, which folds high frequencies back as noise.
  downsample(buf) {
    const ratio = this.inRate / this.outRate;
    const len = Math.floor(buf.length / ratio);
    const out = new Float32Array(len);
    for (let i = 0; i < len; i++) {
      const start = Math.floor(i * ratio);
      const end = Math.min(buf.length, Math.floor((i + 1) * ratio));
      let sum = 0;
      for (let j = start; j < end; j++) sum += buf[j];
      out[i] = end > start ? sum / (end - start) : buf[start];
    }
    return out;
  }
}

registerProcessor("audiopreprocessor", AudioPreProcessor);
