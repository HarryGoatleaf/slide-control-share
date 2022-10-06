import { createRouter, createWebHistory } from 'vue-router'
import Hello from './views/Hello.vue'
import Presentation from './views/Presentation.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Hello,
    },
    {
      path: '/presentation',
      component: Presentation,
    }
  ]
})
