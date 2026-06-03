<template>
  <div class="flex min-h-screen bg-[#F4F6F5]">
    <Sidebar />


    <div class="flex-1 flex flex-col">
      <Topbar />

      <main class="p-6">
        <div class="space-y-6">
          <div class="bg-white rounded-2xl p-5 shadow-sm">
      <div class="flex items-start justify-between gap-4 mb-5">
        <div>
          <h2 class="text-2xl font-semibold text-gray-800">Персонал</h2>
          <div class="text-sm text-gray-500 mt-1">
            Сотрудники компании
          </div>
        </div>
        <button @click="openCreateUserModal" class="bg-[#1F5D3A] text-white px-4 py-2 rounded-xl hover:bg-[#17482D]">Добавить пользователя</button>
      </div>

      <div class="grid grid-cols-12 gap-4">
        <div class="col-span-12">
          <div class="flex gap-3 items-center mb-4">
            <input
              v-model="query"
              placeholder="Поиск по ФИО"
              class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            />
          </div>

          <div class="space-y-3 max-h-[60vh] overflow-auto pr-1">
            <div
              v-for="u in filteredUsers"
              :key="u.id"
              class="border rounded-xl p-4 hover:bg-gray-50 cursor-pointer flex items-center justify-between gap-4"
              @click="openUser(u)"
            >
              <div class="min-w-0">
                <div class="flex items-center gap-2">
                  <span
                    class="inline-block w-3 h-3 rounded-full"
                    :class="
                      u.on_site
                        ? 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.8)]'
                        : 'bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.85)]'
                    "
                  />
                  <div class="font-semibold truncate">{{ u.full_name || u.username }}</div>
                </div>

                <div class="text-sm text-gray-500 mt-1">
                  Объект: <span class="font-medium text-gray-700">{{ u.address_name || '—' }}</span>
                </div>

                <div v-if="u.on_site" class="text-xs text-gray-500 mt-1">
                  Присутствует: {{ formatDuration(u.on_site_seconds ?? 0) }}
                </div>

                <div v-else class="text-xs text-gray-400 mt-1">Сейчас отсутствует</div>
              </div>

              <div class="text-right">
                <div
                  class="text-sm font-semibold"
                  :class="u.on_site ? 'text-green-600' : 'text-red-500'"
                >
                  {{ u.on_site ? 'На объекте' : 'Отсутствует' }}
                </div>
              </div>
            </div>

            <div v-if="filteredUsers.length === 0" class="text-sm text-gray-500">
              Сотрудники не найдены
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- График выполненных задач сотрудника -->
    <div
      v-if="selectedUser"
      class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
      @click.self="closeUserModal"
    >
      <div class="bg-white rounded-2xl shadow-lg w-full max-w-3xl p-5">
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <h3 class="text-xl font-bold truncate">{{ selectedUser.full_name || selectedUser.username }}</h3>
            <div class="mt-1 text-sm text-gray-500">
              График: количество выполненных задач по дням
            </div>
          </div>
          <button class="text-gray-500 hover:text-gray-800" @click="closeUserModal">✕</button>
        </div>

        <div class="mt-5 rounded-xl border p-4 bg-[#F4F6F5]">
          <div v-if="chartLoading" class="text-sm text-gray-500">Загрузка графика…</div>
          <div v-else-if="!chartPoints.length" class="text-sm text-gray-500">Нет выполненных задач</div>
          <div v-else>
            <div class="flex gap-3 h-[220px]">
              <div
                v-for="p in lastNDaysPoints"
                :key="p.dayKey"
                class="flex flex-col items-center"
              >
                <div class="mt-1 text-[11px] text-gray-500 text-center w-6">{{ p.value }}</div>
                <div class="text-[11px] text-gray-400 text-center w-6">{{ p.dayLabel }}</div>
                <div class="mt-auto w-6 rounded-lg bg-[#1F5D3A]" :style="{ height: `${p.heightPct}%`, minHeight: '6px' }" :title="`${p.dayLabel}: ${p.value}`"></div>
              </div>
            </div>

            <div class="mt-4 text-sm text-gray-600 flex items-center gap-2">
              <span class="inline-block w-3 h-3 rounded-full bg-[#1F5D3A]" />
              <span>Значение: кол-во выполненных задач за день</span>
            </div>
          </div>
        </div>

        <div class="mt-5 flex items-center justify-between gap-4">
          <div>
            <div class="text-sm text-gray-500">Текущий статус</div>
            <div
              class="font-semibold"
              :class="selectedUser.on_site ? 'text-green-600' : 'text-red-500'"
            >
              {{ selectedUser.on_site ? 'На объекте' : 'Отсутствует' }}
            </div>
          </div>

          <div class="text-right">
            <button
              class="bg-[#1F5D3A] text-white px-4 py-2 rounded-xl hover:bg-[#17482D] disabled:opacity-60"
              :disabled="!selectedUser || !selectedUser.on_site"
              @click="showTransfer = true"
            >
              Перевести на другой объект
            </button>
            <div v-if="showTransfer" class="mt-2">
              <select v-model="selectedAddress" class="border rounded p-1 m-4" ">
                <option v-for="(name, id) in addressesMap" :key="id" :value="id">{{ name }}</option>
              </select>
              <button @click="transferUser" class="bg-[#1F5D3A] text-white px-4 py-2 rounded-xl hover:bg-[#17482D] disabled:opacity-60">Подтвердить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
      <CreateUserModal ref="createUserModal" @user-created="loadStaff" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'

import { useAuthStore } from '../stores/auth'

import type { Task } from '../stores/tasks'
import Sidebar from '../components/Sidebar.vue'
import Topbar from '../components/Topbar.vue'
import CreateUserModal from '../components/CreateUserModal.vue'



type StaffUserRow = {
  id: number
  username: string
  full_name?: string | null
  on_site?: boolean
  address_name?: string | null
  on_site_seconds?: number
}

type ChartPoint = {
  dayKey: string
  dayLabel: string
  value: number
  heightPct: number
}

const authStore = useAuthStore()
const query = ref('')

const users = ref<StaffUserRow[]>([])
const selectedUser = ref<StaffUserRow | null>(null)

const chartLoading = ref(false)
const chartPoints = ref<{ dayKey: string; dayLabel: string; value: number }[]>([])

// UI state for transfer modal
const showTransfer = ref(false)
const selectedAddress = ref<number | null>(null)
const addressesMap = ref<Record<number, string>>({})
const createUserModal = ref(null)

function closeUserModal() {
  selectedUser.value = null
  chartPoints.value = []
}

const filteredUsers = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return users.value
  return users.value.filter((u) => (u.full_name || u.username).toLowerCase().includes(q))
})

function formatDuration(totalSeconds: number) {
  const s = Math.max(0, Math.floor(totalSeconds))
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  return `${h}ч ${m}м`
}

async function fetchWithAuth<T>(url: string): Promise<T> {
  const token = authStore.accessToken
  const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
  const res = await fetch(url, { headers })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Request failed: ${res.status} ${text}`)
  }
  return (await res.json()) as T
}

async function loadAddressesMap(): Promise<Map<number, string>> {
  const rows = await fetchWithAuth<{ id: number; name: string }[]>(`http://0.0.0.0:8000/v1/addresses?skip=0&limit=1000`)
  return new Map(rows.map((r) => [r.id, r.name]))
}

async function loadStaff(): Promise<void> {
  if (!authStore.accessToken) return

  const addressesMap = await loadAddressesMap()

  const isMaster = authStore.user?.role === 'master'
  const onSiteUrl = isMaster
    ? 'http://0.0.0.0:8000/v1/users/on-site?skip=0&limit=100'
    : 'http://0.0.0.0:8000/v1/users/on-site/all?skip=0&limit=100'

  const onSite = await fetchWithAuth<any[]>(onSiteUrl)

  // active users list
  const allUsers = await fetchWithAuth<any[]>(`http://0.0.0.0:8000/v1/users/active?skip=0&limit=1000`)

  const now = Date.now()

  const onSiteById = new Map<number, any>(onSite.map((u: any) => [u.id, u]))

  const mapped = allUsers.map((u: any) => {
    const os = onSiteById.get(u.id)
    const addressName = os?.address_id ? addressesMap.get(os.address_id) : null
    const onSiteSeconds = os?.on_site_since
      ? (now - new Date(os.on_site_since).getTime()) / 1000
      : undefined

    return {
      id: u.id,
      username: u.username,
      full_name: u.full_name,
      on_site: Boolean(os),
      address_name: addressName,
      on_site_seconds: onSiteSeconds
    } satisfies StaffUserRow
  })

  users.value = mapped
}

function dayKeyFromDate(d: Date) {
  // YYYY-MM-DD
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function dayLabelFromKey(dayKey: string) {
  // DD.MM
  const [, m, d] = dayKey.split('-')
  return `${d}.${m}`
}

async function loadUserChart(userId: number) {
  chartLoading.value = true
  chartPoints.value = []
  try {
    const auth = authStore
    const token = auth.accessToken

    const res = await fetch(`http://0.0.0.0:8000/v1/tasks/`, {
      method: 'GET',
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Failed to load tasks: ${res.status} ${text}`)
    }

    const allTasks = (await res.json()) as Task[]

    const completed = allTasks.filter((t) => t.assigned_to_id === userId && t.completed_at)

    const counts = new Map<string, number>()
    for (const t of completed) {
      const d = new Date(t.completed_at as string)
      if (Number.isNaN(d.getTime())) continue
      const key = dayKeyFromDate(d)
      counts.set(key, (counts.get(key) ?? 0) + 1)
    }

    const points = Array.from(counts.entries())
      .sort((a, b) => (a[0] < b[0] ? -1 : 1))
      .map(([dayKey, value]) => ({
        dayKey,
        dayLabel: dayLabelFromKey(dayKey),
        value
      }))

    chartPoints.value = points
  } finally {
    chartLoading.value = false
  }
}

const lastNDaysPoints = computed<ChartPoint[]>(() => {
  const points = chartPoints.value
  if (!points.length) return []

  // берем последние 7 дней, чтобы график был компактным
  const last = points.slice(-7)
  const max = Math.max(...last.map((p) => p.value), 1)

  return last.map((p) => {
    const heightPct = Math.round((p.value / max) * 100)
    return {
      ...p,
      heightPct: Math.max(6, heightPct) // минимальная высота, чтобы столбцы были видны
    }
  })
})

function openUser(u: StaffUserRow) {
  selectedUser.value = u
  void loadUserChart(u.id)
  // Load addresses for transfer dropdown
  void loadAddressesMap().then(map => {
    addressesMap.value = Object.fromEntries(Array.from(map.entries()))
  })
}

async function transferUser() {
  if (!selectedUser.value || selectedAddress.value === null) return
  const token = authStore.accessToken
  const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' }
  const res = await fetch(`http://0.0.0.0:8000/v1/users/${selectedUser.value.id}/transfer?address_id=${selectedAddress.value}`, {
    method: 'PUT',
    headers,
  })
  if (!res.ok) {
    const txt = await res.text().catch(() => '')
    alert(`Ошибка перевода: ${res.status} ${txt}`)
    return
  }
  // Refresh staff list and close transfer UI
  void loadStaff()
  showTransfer.value = false
}

function openCreateUserModal() {
  if (createUserModal.value) {
    // @ts-ignore
    createUserModal.value.openModal()
  }
}

onMounted(() => {
  void loadStaff()
})


watch(
  () => authStore.accessToken,
  () => {
    void loadStaff()
  }
)
</script>

