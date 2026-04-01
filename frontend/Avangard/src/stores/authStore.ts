import { defineStore } from 'pinia'
import type { User } from '@/types/auth'
import { login, logout, getCurrentUser } from '@/services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null
  }),

  actions: {
    async signIn(credentials: { email: string; password: string }) {
      const response = await login(credentials)
      this.user = response.user
    },

    async signOut() {
      await logout()
      this.user = null
    },

    async initialize() {
      this.user = await getCurrentUser()
    }
  }
})

