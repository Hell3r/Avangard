import type { LoginCredentials, LoginResponse, User } from '@/types/auth'
import { apiFetch } from '@/utils/api'

export async function login(credentials: LoginCredentials): Promise<LoginResponse> {
  const data = await apiFetch('/users/login', {
    method: 'POST',
    body: JSON.stringify(credentials)
  })
  localStorage.setItem('token', data.token)
  return data
}

export async function logout() {
  localStorage.removeItem('token')
}

export async function getCurrentUser(): Promise<User | null> {
  try {
    const user = await apiFetch('/users/me')
    return user
  } catch {
    return null
  }
}

