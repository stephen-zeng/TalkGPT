import { createRouter, createWebHistory } from 'vue-router';
import App from '../App.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: App
  }
  // 其他路由
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
