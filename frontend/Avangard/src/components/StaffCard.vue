<template>
  <div class="space-y-6">
    <div class="bg-white rounded-2xl p-5 shadow-sm">
      <h2 class="text-xl font-semibold mb-5">Персонал</h2>

      <div class="space-y-4">
        <div
          v-for="u in onSiteUsers.slice(0, 3)"
          :key="u.id"
          class="flex items-start justify-between gap-3"
        >
          <div class="min-w-0">
            <div class="font-medium flex items-center gap-2">
              <span class="inline-block w-3 h-3 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.8)]" />
              <span class="truncate">{{ u.full_name || u.username }}</span>
            </div>
            <div class="text-sm text-gray-500">На объекте</div>
          </div>
        </div>

        <div v-if="onSiteUsers.length === 0" class="text-sm text-gray-500">
          На объекте никого нет
        </div>

        <div v-if="onSiteUsers.length > 3" class="text-sm text-gray-400">
          +{{ onSiteUsers.length - 3 }}
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-5 shadow-sm">
      <h2 class="text-xl font-semibold mb-5 text-red-500">Отсутствуют</h2>

      <div class="space-y-4">
        <div v-for="u in offSiteUsers.slice(0, 3)" :key="u.id" class="flex items-center gap-2">
          <span class="inline-block w-3 h-3 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.85)]" />
          <span class="font-medium truncate">{{ u.full_name || u.username }}</span>
        </div>

        <div v-if="offSiteUsers.length > 3" class="text-sm text-gray-400">
          +{{ offSiteUsers.length - 3 }}
        </div>

        <div v-if="offSiteUsers.length === 0" class="text-sm text-gray-500">
          Никто не отсутствует
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { useAuthStore } from '../stores/auth'

type UserRow = {
  id: number
  username: string
  full_name?: string | null
}

const authStore = useAuthStore()

const onSiteUsers = ref<UserRow[]>([])
const offSiteUsers = ref<UserRow[]>([])

async function fetchWithAuth(url: string) {
  const token = authStore.accessToken
  const headers: Record<string, string> = token
    ? { Authorization: `Bearer ${token}` }
    : {}
  const res = await fetch(url, { headers })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Request failed: ${res.status} ${text}`)
  }
  return (await res.json()) as UserRow[]
}

async function loadStaff() {
  try {
    if (!authStore.accessToken) {
      console.warn('[StaffCard] No access token');
      return
    }

    // Повторяем логику из Dashboard:
    // мастер -> /v1/users/on-site
    // иначе -> /v1/users/on-site/all
    const isMaster = authStore.user?.role === 'master'

    // Use unified endpoint that returns all on‑site users regardless of role
    const onSiteUrl = 'http://0.0.0.0:8000/v1/users/on-site/all?skip=0&limit=100'

    const onSite = await fetchWithAuth(onSiteUrl)
    onSiteUsers.value = onSite

    const allUsers = await fetchWithAuth(
      'http://0.0.0.0:8000/v1/users/active?skip=0&limit=1000'
    )

    const onSiteIds = new Set(onSite.map((u) => u.id))
    offSiteUsers.value = allUsers.filter((u) => !onSiteIds.has(u.id))
  } catch (e) {
    console.error('[StaffCard] loadStaff failed', e)
    // не обнуляем onSite, чтобы хотя бы «На объекте» отображался
  }
}

onMounted(() => {
  loadStaff()
})
</script>
