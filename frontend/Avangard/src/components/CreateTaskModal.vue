<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-2xl p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold text-gray-900">Создать задачу сотруднику</h3>
          <div class="mt-1 text-sm text-gray-500">Назначение, срок и статус</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>

      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Сотрудник</label>
          <select
            v-model="form.assigned_to_id"
            class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            required
          >
            <option disabled value="">Выберите сотрудника</option>
            <option v-for="u in staff" :key="u.id" :value="u.id">
              {{ u.full_name || u.username }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Описание</label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            placeholder="Например: Подготовить материалы / Выполнить работы"
            required
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Срок</label>
            <input
              v-model="dueDateLocal"
              type="datetime-local"
              class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Статус</label>
            <select
              v-model="form.status"
              class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            >
              <option value="В работе">В работе</option>
              <option value="Проверка">Проверка</option>
              <option value="Выполнено">Выполнено</option>
            </select>
          </div>
        </div>

        <div v-if="error" class="text-sm text-red-600">{{ error }}</div>

        <div class="flex justify-end gap-3 pt-2">
          <button
            type="button"
            class="px-4 py-2 rounded-xl border border-gray-200 text-gray-700 hover:bg-gray-50"
            @click="close"
          >
            Отмена
          </button>
          <button
            type="submit"
            class="px-4 py-2 rounded-xl bg-[#1F5D3A] text-white hover:bg-[#17482D] transition"
            :disabled="loading"
          >
            {{ loading ? 'Создаю…' : 'Создать' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useTasksStore } from '../stores/tasks'
import { useAuthStore } from '../stores/auth'

type StaffUser = {
  id: number
  username: string
  full_name?: string | null
}

const tasksStore = useTasksStore()
const authStore = useAuthStore()

const open = ref(false)
const loading = ref(false)
const error = ref<string | null>(null)

const staff = ref<StaffUser[]>([])

const form = ref<{
  description: string | null
  assigned_to_id: number | ''
  due_at: string | null
  status: string
}>({
  description: null,
  assigned_to_id: '',
  due_at: null,
  status: 'В работе'
})

// datetime-local формат для модели
const dueDateLocal = computed({
  get() {
    // если due_at уже ISO строка — переводим в local
    if (!form.value.due_at) return ''
    const d = new Date(form.value.due_at)
    if (Number.isNaN(d.getTime())) return ''

    const pad = (n: number) => String(n).padStart(2, '0')
    const yyyy = d.getFullYear()
    const mm = pad(d.getMonth() + 1)
    const dd = pad(d.getDate())
    const hh = pad(d.getHours())
    const mi = pad(d.getMinutes())
    return `${yyyy}-${mm}-${dd}T${hh}:${mi}`
  },
  set(v: string) {
    if (!v) {
      form.value.due_at = null
      return
    }
    // v: YYYY-MM-DDTHH:mm
    const iso = new Date(v).toISOString()
    form.value.due_at = iso
  }
})

async function fetchStaff() {
  const token = authStore.accessToken
  const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}

  const isMaster = authStore.user?.role === 'master'
  // master: /on-site ; admin: /on-site/all
  const onSiteUrl = isMaster
    ? 'http://0.0.0.0:8000/v1/users/on-site?skip=0&limit=200'
    : 'http://0.0.0.0:8000/v1/users/on-site/all?skip=0&limit=200'

  const res = await fetch(onSiteUrl, { headers })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Не удалось загрузить сотрудников: ${res.status} ${text}`)
  }

  staff.value = (await res.json()) as StaffUser[]
}

async function openModal() {
  open.value = true
  error.value = null
  loading.value = false

  if (!staff.value.length) {
    try {
      await fetchStaff()
    } catch (e) {
      error.value = e instanceof Error ? e.message : String(e)
    }
  }

  // дефолтный срок: +1 день
  if (!form.value.due_at) {
    form.value.due_at = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
  }
}

function close() {
  open.value = false
  error.value = null
  loading.value = false

  form.value = {
    description: null,
    assigned_to_id: '',
    due_at: null,
    status: 'В работе'
  }
}

async function submit() {
  if (!form.value.assigned_to_id || !form.value.description || !form.value.due_at) return

  loading.value = true
  error.value = null

  try {
    await tasksStore.createTask({
      description: form.value.description,
      assigned_to_id: Number(form.value.assigned_to_id),
      due_at: form.value.due_at,
      status: form.value.status
    })



    await tasksStore.loadTasks()
    close()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // ничего, staff подгружаем только при открытии
})

defineExpose({ openModal })
</script>

