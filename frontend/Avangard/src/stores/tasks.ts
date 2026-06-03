import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export interface User {
  id: number
  full_name: string
}

export interface Task {
  id: number
  description: string
  assigned_to_id: number | null
  assigned_by_id: number | null
  due_at: string
  status: string
  created_at: string
  completed_at: string | null
  assigned_to?: User | null
}



type ApiResponse<T> = T

type TaskCompletePayload = {
  completed_at?: string
}

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    tasks: [] as Task[],
    loading: false,
    error: null as string | null
  }),
  actions: {
    async loadTasks() {
      this.loading = true
      this.error = null

      try {
        const auth = useAuthStore()
        const token = auth.accessToken

        const res = await fetch('http://0.0.0.0:8000/v1/tasks/', {
          method: 'GET',
          headers: (token ? { Authorization: `Bearer ${token}` } : {})
        })

        if (!res.ok) {
          const text = await res.text().catch(() => '')
          throw new Error(`Failed to load tasks: ${res.status} ${text}`)
        }

        const data = (await res.json()) as ApiResponse<Task[]>
        this.tasks = data
      } catch (e) {
        this.error = e instanceof Error ? e.message : String(e)
      } finally {
        this.loading = false
      }
    },

    async createTask(payload: {
      description: string | null
      assigned_to_id: number
      due_at: string | null
      status: string
    }) {
      const auth = useAuthStore()
      const token = auth.accessToken

      const res = await fetch('http://0.0.0.0:8000/v1/tasks/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
          description: payload.description,
          assigned_to_id: payload.assigned_to_id,
          due_at: payload.due_at,
          status: payload.status
        })
      })

      if (!res.ok) {
        const text = await res.text().catch(() => '')
        throw new Error(`Failed to create task: ${res.status} ${text}`)
      }

      return (await res.json()) as Task
    },

    async completeTask(taskId: number) {

      const auth = useAuthStore()
      const token = auth.accessToken

      const res = await fetch(`http://0.0.0.0:8000/v1/tasks/${taskId}/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ completed_at: new Date().toISOString() } satisfies TaskCompletePayload)
      })

      if (!res.ok) {
        const text = await res.text().catch(() => '')
        throw new Error(`Failed to complete task: ${res.status} ${text}`)
      }

      return (await res.json()) as Task
    }
  }
})

