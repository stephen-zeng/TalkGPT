import { createApp } from 'vue'
import App from './App.vue'
import { io } from 'socket.io-client'
import { Player } from '@/audio/player.js';
import 'mdui/mdui.css'
import 'mdui'
import './assets/main.css'

const app = createApp(App);
const socket = io('ws://127.0.0.1:11111');
const player = new Player();
app.provide('socket', socket);
app.provide('player', player);
app.mount("#app");
