<template>
  <div class="min-h-screen bg-[#F4F6F5]">
    <div class="p-6 max-w-4xl mx-auto">
      <div class="flex items-start justify-between gap-4 mb-6">
        <div>
          <h2 class="text-2xl font-semibold text-gray-800">Окно сотрудника</h2>
          <div class="text-sm text-gray-500 mt-1">Просмотр задач и управление сменой</div>
        </div>

        <div class="bg-white rounded-2xl p-4 shadow-sm w-[260px]">
          <div class="text-xs text-gray-500">Статус смены</div>
          <div
            class="font-semibold text-lg mt-1"
            :class="isOnShift ? 'text-green-700' : 'text-gray-700'"
          >
            {{ isOnShift ? 'На смене' : 'Не на смене' }}
          </div>

          <div class="mt-2 text-sm font-semibold text-gray-800">
            {{ formatDuration(onShiftSeconds) }}
          </div>

          <button
            class="mt-3 w-full bg-[#1F5D3A] hover:bg-[#17482D] text-white px-4 py-2 rounded-xl text-sm font-medium disabled:opacity-60"
            :disabled="shiftLoading"
            @click="toggleShift"
          >
            {{ isOnShift ? 'Выйти со смены' : 'Войти на смену' }}
          </button>

          <div v-if="shiftError" class="text-xs text-red-600 mt-2">
            {{ shiftError }}
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-5 shadow-sm">
        <div class="flex items-center justify-between gap-4 mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Задачи</h3>
          <div class="text-sm text-gray-500">Всего: {{ myTasks.length }}</div>
        </div>

        <div class="space-y-3 max-h-[60vh] overflow-auto pr-1">
          <div
            v-for="t in myTasks"
            :key="t.id"
            class="border rounded-xl p-4 bg-white hover:bg-gray-50"
          >
            <div class="font-semibold break-words">{{ t.description }}</div>
            <div class="text-sm text-gray-500 mt-1">
              Статус: <span class="font-medium">{{ t.status }}</span>
            </div>
            <div class="text-xs text-gray-400 mt-1">
              Срок: {{ formatDate(t.due_at) }}
            </div>
            <div
              v-if="t.completed_at"
              class="text-xs text-gray-400 mt-1"
            >
              Завершено: {{ formatDate(t.completed_at) }}
            </div>
            <button
              v-if="!t.completed_at && t.status !== 'Выполнена'"
              class="mt-3 w-full bg-[#1F5D3A] hover:bg-[#17482D] text-white px-4 py-2 rounded-xl text-sm font-medium disabled:opacity-60"
              @click="completeTaskHandler(t.id)"
            >Выполнить</button>
          </div>

          <div v-if="!myTasks.length" class="text-sm text-gray-500">Нет задач</div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import Sidebar from '../components/Sidebar.vue'
import Topbar from '../components/Topbar.vue'

import { useAuthStore } from '../stores/auth'
import { useTasksStore, type Task } from '../stores/tasks'

type UserMe = {
  on_site_since?: string | null
  is_on_site?: boolean
}

const authStore = useAuthStore()
const tasksStore = useTasksStore()

const shiftLoading = ref(false)
const shiftError = ref<string | null>(null)

const isOnShift = ref(false)
const onShiftSince = ref<Date | null>(null)
const onShiftSeconds = ref(0)
let intervalId: number | null = null

async function completeTaskHandler(taskId: number) {
 try {
   await tasksStore.completeTask(taskId)
   await tasksStore.loadTasks()
 } catch (e) {
   console.error('Failed to complete task', e)
 }
}




function startTimer() {
  if (intervalId != null) window.clearInterval(intervalId)

  intervalId = window.setInterval(() => {
    if (!onShiftSince.value) return
    onShiftSeconds.value = Math.max(0, Math.floor((Date.now() - onShiftSince.value.getTime()) / 1000))
  }, 1000)
}

function stopTimer() {
  if (intervalId != null) window.clearInterval(intervalId)
  intervalId = null
}

function formatDuration(totalSeconds: number) {
  const s = Math.max(0, Math.floor(totalSeconds))
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  return `${h}ч ${m}м ${sec}с`
}


function formatDate(iso: string) {
  try {
  return new Date(iso).toLocaleString('ru-RU')
  } catch {
    return iso
  }
}

async function fetchMe(): Promise<UserMe> {
  const token = authStore.accessToken
  const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}

  const res = await fetch('http://0.0.0.0:8000/v1/users/me', { headers })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Failed to load user: ${res.status} ${text}`)
  }

  return (await res.json()) as UserMe
}

function shiftOn(msSince: number) {
  const shiftSeconds = Math.max(0, Math.floor(msSince / 1000))
  onShiftSeconds.value = shiftSeconds
}

function parseBackendDate(value: string): Date {
  // Backend returns naive ISO like "2026-05-19T13:26:55.534601" (no Z).
  // JS Date interprets it as local time => timezone shift.
  // Treat it as UTC to match backend datetime.utcnow().
  const ms = Date.parse(value.endsWith('Z') ? value : `${value}Z`)
  return new Date(ms)
}


async function toggleShift() {
  shiftLoading.value = true
  shiftError.value = null
  try {
    const token = authStore.accessToken
    const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}

    const res = await fetch('http://0.0.0.0:8000/v1/users/me/on-site', {
      method: 'PUT',
      headers
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Failed to toggle shift: ${res.status} ${text}`)
    }

    const updated = (await res.json()) as UserMe & { on_site_since?: string | null; is_on_site?: boolean }

    isOnShift.value = Boolean(updated.is_on_site)
    onShiftSince.value = updated.on_site_since ? parseBackendDate(updated.on_site_since) : null
    onShiftSeconds.value = 0

    if (isOnShift.value) startTimer()
    else stopTimer()

    // обновим authStore.user, чтобы при следующем заходе таймер мог быть стартован
    // (если backend вернул поля, соответствующие user_info)
    // Обновим authStore.user как минимум полями для таймера.
    // Важно: тип UserInfo в auth store не содержит этих полей, поэтому используем cast.
    if (authStore.user) {
      const userAny = authStore.user as any
      userAny.is_on_site = (updated as any).is_on_site
      userAny.on_site_since = (updated as any).on_site_since
      ;(authStore as any).persist?.()
    }
  } catch (e) {
    shiftError.value = e instanceof Error ? e.message : String(e)
  } finally {
    shiftLoading.value = false
  }
}

const myTasks = computed(() => {
  const meId = authStore.user?.user_id
  if (!meId) return []
  return tasksStore.tasks.filter((t: Task) => t.assigned_to_id === meId)
})

async function loadAll() {
  if (!authStore.accessToken || !authStore.user) return

  // смена
  const me = await fetchMe()
  isOnShift.value = Boolean(me.is_on_site)
  onShiftSince.value = me.on_site_since ? parseBackendDate(me.on_site_since) : null

  if (isOnShift.value && onShiftSince.value) {
    shiftOn(Date.now() - onShiftSince.value.getTime())
    startTimer()
  } else {
    onShiftSeconds.value = 0
    stopTimer()
  }


  // задачи
  await tasksStore.loadTasks()
}

onMounted(async () => {
  await loadAll()
})

watch(
  () => authStore.user?.user_id,
  () => {
    void loadAll()
  }
)

onBeforeUnmount(() => {
  stopTimer()
})
</script>

