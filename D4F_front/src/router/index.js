import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import InputView from '../views/InputView.vue'
import CommandsView from '@/views/CommandsView.vue'
import ShopView from '@/views/ShopView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/shop',
      name: 'shop',
      component: ShopView
    },
    {
      path: '/commands',
      name: 'commands',
      component: CommandsView
    }
  ]
})

export default router
