<template>
  <div class="flex min-h-screen bg-[#F4F6F5]">
    <div class="flex-1 flex flex-col">
      <Topbar />

      <main class="p-6">
        <div class="space-y-6">
          <div class="bg-white rounded-2xl p-5 shadow-sm">
            <div class="flex items-start justify-between gap-4 mb-5">
              <div>
                <h2 class="text-xl font-semibold">Мастер: {{ authStore.user?.full_name }}</h2>
                <div class="text-sm text-gray-500 mt-1">
                  Объект закреплён за вашим аккаунтом
                </div>
              </div>

              <div v-if="address" class="text-sm font-semibold text-[#1F5D3A] whitespace-nowrap">
                ID: {{ address.id }}
              </div>
            </div>

            <div v-if="loadingAddress" class="text-sm text-gray-500">Загрузка объекта…</div>

            <div v-else-if="address" class="text-sm text-gray-700">
              <div class="font-semibold text-gray-800">{{ address.name }}</div>
            </div>

            <div v-else class="text-sm text-gray-500">Объект не найден</div>
          </div>

          <div class="grid grid-cols-12 gap-6">
            <div class="col-span-6">
              <div class="bg-white rounded-2xl p-5 shadow-sm h-full">
                <h3 class="text-lg font-semibold mb-3">Присутствуют</h3>

                <div v-if="loadingPeople" class="text-sm text-gray-500">Загрузка сотрудников…</div>

                <div v-else class="space-y-3">
                  <div
                    v-for="u in onSiteUsers"
                    :key="u.id"
                    class="border rounded-xl p-4 flex items-center justify-between gap-4"
                  >
                    <div class="min-w-0">
                      <div class="font-semibold truncate flex items-center gap-2">
                        <span class="inline-block w-3 h-3 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.8)]" />
                        {{ u.full_name || u.username }}
                      </div>
                      <div class="text-sm text-gray-500 mt-1">На объекте</div>
                    </div>
                  </div>

                  <div v-if="!onSiteUsers.length" class="text-sm text-gray-500">Никого нет</div>
                </div>
              </div>
            </div>

            <div class="col-span-6">
              <div class="bg-white rounded-2xl p-5 shadow-sm h-full">
                <h3 class="text-lg font-semibold mb-3 text-red-500">Отсутствуют</h3>

                <div v-if="loadingPeople" class="text-sm text-gray-500">Загрузка сотрудников…</div>

                <div v-else class="space-y-3">
                  <div
                    v-for="u in offSiteUsers"
                    :key="u.id"
                    class="border rounded-xl p-4 flex items-center justify-between gap-4"
                  >
                    <div class="min-w-0">
                      <div class="font-semibold truncate flex items-center gap-2">
                        <span class="inline-block w-3 h-3 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.85)]" />
                        {{ u.full_name || u.username }}
                      </div>
                      <div class="text-sm text-gray-500 mt-1">Вне объекта</div>
                    </div>
                  </div>

                  <div v-if="!offSiteUsers.length" class="text-sm text-gray-500">Никого нет</div>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-12 gap-6">
            <div class="col-span-7">
              <div class="bg-white rounded-2xl p-5 shadow-sm h-full">
                <div class="flex items-start justify-between gap-4 mb-5">
                  <div>
                    <h3 class="text-lg font-semibold">Материалы</h3>
                    <div class="text-sm text-gray-500 mt-1">Взять материалы со склада</div>
                  </div>

                  <button
                    class="bg-[#1F5D3A] hover:bg-[#17482D] text-white px-4 py-2 rounded-xl text-sm font-medium"
                    @click="openTakeModal"
                  >
                    Взять материал
                  </button>
                </div>

                <div class="space-y-3 max-h-[35vh] overflow-auto pr-1">
                  <div
                    v-for="m in materials"
                    :key="m.id"
                    class="border rounded-xl p-4 hover:bg-gray-50 cursor-pointer flex items-start justify-between gap-4"
                    @click="openTakeModalFor(m)"
                  >
                    <div class="min-w-0">
                      <div class="font-semibold truncate">{{ m.material_name }}</div>
                      <div class="text-sm text-gray-500 break-words">{{ m.description || '—' }}</div>
                    </div>

                    <div
                      class="font-bold whitespace-nowrap"
                      :class="{
                        'text-red-600': m.remainder <= 0,
                        'text-yellow-600': m.remainder > 0 && m.remainder <= 5,
                        'text-green-700': m.remainder > 5,
                      }"
                    >
                      {{ m.remainder }}
                    </div>
                  </div>

                  <div v-if="!materials.length" class="text-sm text-gray-500">Нет материалов</div>
                </div>
              </div>
            </div>

            <div class="col-span-5">
              <div class="bg-white rounded-2xl p-5 shadow-sm h-full flex flex-col">
                <div class="flex items-start justify-between gap-4 mb-5">
                  <div>
                    <h3 class="text-lg font-semibold">Задачи сотрудникам</h3>
                    <div class="text-sm text-gray-500 mt-1">Только на вашем объекте</div>
                  </div>

                  <button
                    class="bg-[#1F5D3A] hover:bg-[#17482D] text-white px-4 py-2 rounded-xl text-sm font-medium"
                    @click="openCreateTaskModal"
                  >
                    +
                  </button>
                </div>

                <div class="flex-1 overflow-auto space-y-3">
                  <div v-for="t in tasksForObject" :key="t.id" class="border rounded-xl p-4">
                    <div class="font-semibold">{{ t.description }}</div>
                    <div class="text-sm text-gray-500 mt-1">
                      Назначен: {{ t.assigned_to?.full_name ?? '—' }}
                    </div>
                    <div class="text-xs text-gray-400 mt-1">Срок: {{ formatDate(t.due_at) }}</div>
                  </div>

                  <div v-if="!tasksForObject.length" class="text-sm text-gray-500">Задач пока нет</div>
                </div>
              </div>
            </div>
          </div>

          <TakeMaterialModal ref="takeModalRef" @withdraw-done="reloadAll" />
          <CreateTaskForObjectModal ref="createTaskModalRef" @task-created="reloadAll" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import Topbar from '../components/Topbar.vue'

import TakeMaterialModal from '../components/TakeMaterialModal.vue'
import CreateTaskForObjectModal from '../components/CreateTaskForObjectModal.vue'

import { useAuthStore } from '../stores/auth'
import { useStorageStore } from '../stores/storage'
import { useTasksStore, type Task } from '../stores/tasks'

type AddressRow = { id: number; name: string }

type UserRow = {
  id: number
  username: string
  full_name?: string | null
  address_id?: number
}

type StorageRow = {
  id: number
  material_name: string
  description?: string | null
  remainder: number
}

const authStore = useAuthStore()
const storageStore = useStorageStore()
const tasksStore = useTasksStore()

const address = ref<AddressRow | null>(null)
const loadingAddress = ref(false)

const onSiteUsers = ref<UserRow[]>([])
const offSiteUsers = ref<UserRow[]>([])
const loadingPeople = ref(false)

const takeModalRef = ref<InstanceType<typeof TakeMaterialModal> | null>(null)
const createTaskModalRef = ref<InstanceType<typeof CreateTaskForObjectModal> | null>(null)

const tasksForObject = computed(() => {
  // MVP: бэкенд пока возвращает задачи без фильтра по address_id.
  // На фронте фильтруем по assigned_to.address_id через уже загруженные on-site/off-site.
  const allowedIds = new Set<number>([...onSiteUsers.value, ...offSiteUsers.value].map((u) => u.id))
  return tasksStore.tasks.filter((t) => t.assigned_to_id == null ? false : allowedIds.has(t.assigned_to_id))
})

const materials = computed(() => storageStore.storages as StorageRow[])

function formatDate(iso: string) {
  try {
    return new Date(iso).toLocaleString('ru-RU')
  } catch {
    return iso
  }
}

async function fetchJSON<T>(url: string): Promise<T> {
  const token = authStore.accessToken
  const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
  const res = await fetch(url, { headers })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Request failed: ${res.status} ${text}`)
  }
  return (await res.json()) as T
}

async function loadAddress() {
  const addressId = authStore.user?.address_id
  if (!addressId) return

  loadingAddress.value = true
  try {
    address.value = await fetchJSON<AddressRow>(`http://0.0.0.0:8000/v1/addresses/${addressId}`)
  } finally {
    loadingAddress.value = false
  }
}

async function loadPeople() {
  const addressId = authStore.user?.address_id
  if (!addressId) return

  loadingPeople.value = true
  try {
    onSiteUsers.value = await fetchJSON<UserRow[]>(`http://0.0.0.0:8000/v1/users/on-site?skip=0&limit=200`)
    offSiteUsers.value = await fetchJSON<UserRow[]>(`http://0.0.0.0:8000/v1/users/off-site?skip=0&limit=200`)
  } finally {
    loadingPeople.value = false
  }
}

async function reloadAll() {
  await Promise.all([
    storageStore.loadStorages(),
    tasksStore.loadTasks(),
    loadPeople(),
    loadAddress()
  ])
}

function openTakeModal() {
  takeModalRef.value?.openModal()
}

function openTakeModalFor(m: StorageRow) {
  takeModalRef.value?.openModalWithStorage(m)
}

function openCreateTaskModal() {
  createTaskModalRef.value?.openModal({
    allowedUserIds: new Set<number>([...onSiteUsers.value, ...offSiteUsers.value].map((u) => u.id)),
  })
}

onMounted(async () => {
  await reloadAll()
})
</script>

