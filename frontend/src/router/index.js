
import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '@/views/Home.vue'
import Home from '@/views/Home.vue'
import Ranking from '@/views/Ranking.vue'
import RegisterAvailability from '@/views/RegisterAvailability.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/ranking',
    name: 'ranking',
    component: Ranking
  },
  {
    path: '/register-availabilty',
    name: 'registerAvailability',
    component: RegisterAvailability
  },
]

const router = new VueRouter({
  // mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router