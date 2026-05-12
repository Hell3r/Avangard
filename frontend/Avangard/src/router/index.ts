import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: { name: 'login-page' }
    },

    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAdmin: true }
    },
    // чтобы / всегда начинался с логина
    {
      path: '/login',
      name: 'login-page',
      component: Login
    }
  ]

})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta?.requiresAdmin && (!auth.isAuthenticated || auth.user?.role !== 'admin')) {
    return {
      name: 'login',
      query: { error: 'forbidden' }
    }
  }

  return true
 })


export default router

