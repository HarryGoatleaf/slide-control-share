import { createRouter, createWebHistory } from 'vue-router'
import Hello from './views/Hello.vue'
import Presentation from './views/Presentation.vue'
import Index from './views/Index.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Index,
    },
    {
      path: '/:path(.*)*/hello',
      component: Hello,
    },
    {
      path: '/presentation',
      component: Presentation,
    }
  ]
})
