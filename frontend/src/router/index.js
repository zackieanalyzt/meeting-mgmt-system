import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Meetings from '../views/Meetings.vue'
import Reports from '../views/Reports.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/meetings',
    name: 'Meetings',
    component: Meetings
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router