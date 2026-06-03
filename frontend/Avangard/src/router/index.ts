import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import { useAuthStore } from '../stores/auth'
import MaterialsBoard from '../components/MaterialsBoard.vue'
import Objects from '../views/Objects.vue'
import Staff from '../views/Staff.vue'
import Master from '../views/Master.vue'
import Employee from '../views/Employee.vue'



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
    
    {
      path: '/objects',
      name: 'objects',
      component: Objects,
      meta: { requiresAdmin: true }
    },

    {
      path: '/staff',
      name: 'staff',
      component: Staff,
      meta: { requiresAdmin: true }
    },


    {
      path: '/warehouse',
      name: 'warehouse',
      component: MaterialsBoard,
      meta: { requiresAdmin: true }
    },

    {
      path: '/login',
      name: 'login-page',
      component: Login
    },

    {
      path: '/master',
      name: 'master',
      component: Master,
      meta: { requiresMaster: true }
    },

    {
      path: '/employee',
      name: 'employee',
      component: Employee,
      meta: { requiresEmployee: true }
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

  if (to.meta?.requiresMaster && (!auth.isAuthenticated || auth.user?.role !== 'master')) {
    return {
      name: 'login',
      query: { error: 'forbidden' }
    }
  }

  if (to.meta?.requiresEmployee && (!auth.isAuthenticated || auth.user?.role !== 'employee')) {
    return {
      name: 'login',
      query: { error: 'forbidden' }
    }
  }

  return true
 })



export default router

