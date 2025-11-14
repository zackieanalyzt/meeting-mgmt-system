import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import CurrentMeeting from '../views/CurrentMeeting.vue'
import ReportsHistory from '../views/ReportsHistory.vue'
import SearchReports from '../views/SearchReports.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/meetings',
    name: 'MeetingList',
    component: () => import('../views/MeetingList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/meetings/create',
    name: 'CreateMeeting',
    component: () => import('../views/MeetingCreate.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/meetings/:id',
    name: 'MeetingDetail',
    component: () => import('../views/MeetingDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/current-meeting',
    name: 'CurrentMeeting',
    component: CurrentMeeting,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports-history',
    name: 'ReportsHistory',
    component: ReportsHistory,
    meta: { requiresAuth: true }
  },
  {
    path: '/search-reports',
    name: 'SearchReports',
    component: SearchReports,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.name === 'Login' && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router