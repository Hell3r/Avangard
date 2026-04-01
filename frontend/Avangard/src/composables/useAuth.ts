import { ref } from 'vue'
import type { User } from '@/types/auth'
import { login, logout, getCurrentUser } from '@/services/authService'
import { useRouter } from 'vue-router'

const user = ref<User | null>(null)
const loading = ref(true)

export function useAuth() {
  const router = useRouter()

  const signIn = async (credentials: { email: string; password: string }) => {
    try {
      const response = await login(credentials)
      user.value = response.user
      router.push('/dashboard')
    } catch (error) {
      console.error('Login failed', error)
      throw error
    }
  }

  const signOut = async () => {
    await logout()
    user.value = null
    router.push('/login')
  }

  const initAuth = async () => {
    loading.value = true
    user.value = await getCurrentUser()
    loading.value = false
  }

  return {
    user,
    loading,
    signIn,
    signOut,
    initAuth
  }
}

