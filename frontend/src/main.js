import { createApp } from 'vue'
import { WavStreamPlayer, WavRecorder } from './wavtools/index.js'
import App from './App.vue'
import { io } from 'socket.io-client'
import 'mdui/mdui.css'
import 'mdui'
import './assets/main.css'

const app = createApp(App);
const socket = io('http://127.0.0.1:11111');
const recorder = new WavRecorder({ sampleRate: 24000 });
const player = new WavStreamPlayer({ sampleRate: 24000 });
app.provide('socket', socket);
app.provide('recorder', recorder);
app.provide('player', player);
app.mount("#app");
