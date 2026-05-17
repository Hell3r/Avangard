<template>
  <div class="bg-white rounded-2xl p-5 shadow-sm">
    <h2 class="text-2xl font-semibold mb-6">Журнал событий</h2>

    <div class="space-y-5">
      <div v-if="loading" class="text-gray-500">Загрузка…</div>
      <div v-else-if="error" class="text-red-600">{{ error }}</div>
      <template v-else>
        <div v-if="events.length === 0" class="text-gray-500">Событий пока нет</div>

        <div
          v-for="(e, idx) in events"
          :key="e.id"
          class="flex gap-4 border-b pb-4"
        >
          <div
            class="w-3 h-3 rounded-full mt-2"
            ]:class="idx === 0 ? 'bg-green-500' : idx === 1 ? 'bg-blue-500' : 'bg-yellow-500'"
          ></div>

          <div>
            <div class="font-semibold">{{ formatTime(e.event_at) }}</div>
            <div class="text-gray-600">{{ e.event_description }}</div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { useAuthStore } from '../stores/auth'

type EventJournalItem = {
  id: number
  event_description: string
  event_at: string
}

const loading = ref(false)
const error = ref<string | null>(null)
const events = ref<EventJournalItem[]>([])

const auth = useAuthStore()

const limit = 10

function formatTime(value: string) {
  // event_at приходит как ISO строка
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value

  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  return `${hh}:${mm}`
}

async function loadEvents() {
  loading.value = true
  error.value = null

  try {
    const token = auth.accessToken
    const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}

    const res = await fetch(`http://0.0.0.0:8000/v1/events/?skip=0&limit=${limit}`, {
      headers
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Не удалось загрузить журнал: ${res.status} ${text}`)
    }

    events.value = (await res.json()) as EventJournalItem[]
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  void loadEvents()
})
</script>

