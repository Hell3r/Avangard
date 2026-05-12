import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export interface Storage {
  id: number
  material_name: string
  description?: string | null
  remainder: number
}

type ApiResponse<T> = T

export const useStorageStore = defineStore('storage', {
  state: () => ({
    storages: [] as Storage[],
    loading: false,
    error: null as string | null
  }),
  actions: {
    async loadStorages() {
      this.loading = true
      this.error = null

      try {
        const auth = useAuthStore()
        const token = auth.accessToken

        const res = await fetch('http://0.0.0.0:8000/v1/storage/', {
          method: 'GET',
          headers: (token ? { Authorization: `Bearer ${token}` } : {})
        })

        if (!res.ok) {
          const text = await res.text().catch(() => '')
          throw new Error(`Failed to load storages: ${res.status} ${text}`)
        }

        const data = (await res.json()) as ApiResponse<Storage[]>
        this.storages = data
      } catch (e) {
        this.error = e instanceof Error ? e.message : String(e)
      } finally {
        this.loading = false
      }
    }
  }
})

