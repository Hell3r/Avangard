import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type UserInfo = {
  username: string
  full_name?: string | null
  user_id: number
  avatar_path: string | null
  role: string
  is_active: boolean
  last_login: string | null
  address_id: number | null
}


type LoginResponse = {
  access_token: string
  token_type: string
  user_info: UserInfo
}

const ACCESS_TOKEN_KEY = 'access_token'
const USER_KEY = 'user_info'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem(ACCESS_TOKEN_KEY))
  const user = ref<UserInfo | null>(
    (() => {
      const raw = localStorage.getItem(USER_KEY)
      if (!raw) return null
      try {
        return JSON.parse(raw) as UserInfo
      } catch {
        return null
      }
    })()
  )

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

  function persist() {
    if (accessToken.value) localStorage.setItem(ACCESS_TOKEN_KEY, accessToken.value)
    else localStorage.removeItem(ACCESS_TOKEN_KEY)

    if (user.value) localStorage.setItem(USER_KEY, JSON.stringify(user.value))
    else localStorage.removeItem(USER_KEY)
  }

  async function login(username: string, password: string) {
    // Backend expects OAuth2PasswordRequestForm: x-www-form-urlencoded
    const res = await fetch('http://0.0.0.0:8000/v1/users/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        username,
        password
      })
    })

    if (!res.ok) {
      let detail = 'Login failed'
      try {
        const data = await res.json()
        if (data?.detail) detail = data.detail
      } catch {
        // ignore
      }
      throw new Error(detail)
    }

    const data = (await res.json()) as LoginResponse
    accessToken.value = data.access_token
    user.value = data.user_info
    persist()
  }

  function logout() {
    accessToken.value = null
    user.value = null
    persist()
  }

  return {
    accessToken,
    user,
    isAuthenticated,
    login,
    logout
  }
})

