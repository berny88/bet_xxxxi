import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Signin from '../views/signin.vue'
import User from '../views/user.vue'
import Users from '../views/users.vue'
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
    path: '/user/:uid',
    name: 'User',
    component: User
  },
  {
    path: '/users',
    name: 'Users',
    component: Users
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
  
  base: process.env.BASE_URL,
  routes
})

export default router
