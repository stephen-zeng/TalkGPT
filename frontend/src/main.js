import { createApp } from 'vue'
import App from './App.vue'
import { io } from 'socket.io-client'
import 'mdui/mdui.css'
import 'mdui'
import './assets/main.css'

const app = createApp(App);
const socket = io('http://127.0.0.1:11111');
app.provide('socket', socket);
app.mount("#app");
