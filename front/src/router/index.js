import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Sign from '../views/sign.vue'
import Signin from '../views/signin.vue'
import Signon from '../views/logon.vue'
import Games from '../views/games/games.vue'
import Ranking from '../views/games/ranking.vue'
import Bets from '../views/games/bets.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/sign',
    name: 'Sign',
    component: Sign
  },
  {
    path: '/signin',
    name: 'Signin',
    component: Signin
  },
  {
    path: '/signon',
    name: 'Signon',
    component: Signon
  },
  {
    path: '/games',
    name: 'Games',
    component: Games
  },
  {
    path: '/bets',
    name: 'Bets',
    component: Bets
  },
  {
    path: '/ranking',
    name: 'Ranking',
    component: Ranking
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
