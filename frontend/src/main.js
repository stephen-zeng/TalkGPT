import { createApp } from 'vue'
import App from './App.vue'
import { io } from 'socket.io-client'
import { Player } from '@/audio/player.js';
import router from './router';
import 'mdui/mdui.css'
import 'mdui'
import './assets/main.css'

const app = createApp(App);
const socket = io('wss://talk-backend.goforit.top');
const player = new Player();
app.provide('socket', socket);
app.provide('player', player);
app.use(router).mount("#app");
