<template>
  <div v-if="open" class="fixed inset-0 bg-black/30 flex items-center justify-center p-4" @click.self="close">
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-md p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold text-gray-900">Добавить пользователя</h3>
          <div class="mt-1 text-sm text-gray-500">Создание нового сотрудника</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>
    
      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Имя пользователя</label>
          <input v-model="form.username" type="text" class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Полное имя</label>
          <input v-model="form.full_name" type="text" class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Пароль</label>
          <input v-model="form.password" type="password" class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Адрес</label>
          <select v-model.number="form.address_id" class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30" required>
            <option v-for="addr in addresses" :key="addr.id" :value="addr.id">{{ addr.name }}</option>
          </select>
        </div>
        <div v-if="error" class="text-sm text-red-600">{{ error }}</div>
        <div class="flex justify-end gap-3 pt-2">
          <button type="button" class="px-4 py-2 rounded-xl border border-gray-200 text-gray-700 hover:bg-gray-50" @click="close">Отмена</button>
          <button type="submit" class="px-4 py-2 rounded-xl bg-[#1F5D3A] text-white hover:bg-[#17482D] transition" :disabled="loading">
            {{ loading ? 'Создаю…' : 'Создать' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const emit = defineEmits<{ (e: 'user-created'): void }>()
const auth = useAuthStore()

const open = ref(false)
const loading = ref(false)
const error = ref<string | null>(null)

const form = ref({
  username: '',
  full_name: '',
  password: '',
  address_id: null as number | null
})

// list of addresses for dropdown
const addresses = ref<Array<{id: number; name: string}>>([])

async function fetchAddresses() {
  const token = auth.accessToken
  const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
  const res = await fetch('http://0.0.0.0:8000/v1/addresses?skip=0&limit=1000', { headers })
  if (!res.ok) {
    const txt = await res.text().catch(() => '')
    console.error('Failed to load addresses', res.status, txt)
    return
  }
  const data = await res.json()
  addresses.value = data
}

onMounted(() => {
  fetchAddresses()
})

function openModal() {
  open.value = true
  error.value = null
  loading.value = false
  form.value = { username: '', full_name: '', password: '', address_id: null }
}

function close() {
  open.value = false
}

async function submit() {
  if (!form.value.username.trim()) {
    error.value = 'Имя пользователя обязательно'
    return
  }
  loading.value = true
  error.value = null
  try {
    const headers: Record<string, string> = auth.accessToken ? { Authorization: `Bearer ${auth.accessToken}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' }
    const res = await fetch('http://0.0.0.0:8000/v1/users/user', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        username: form.value.username.trim(),
        full_name: form.value.full_name.trim() || undefined,
        password: form.value.password,
        role: 'employee',
        address_id: form.value.address_id
      })
    })
    if (!res.ok) {
      const txt = await res.text().catch(() => '')
      throw new Error(`Не удалось создать пользователя: ${res.status} ${txt}`)
    }
    // ignore response content, just emit event
    emit('user-created')
    close()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Произошла ошибка'
  } finally {
    loading.value = false
  }
}

defineExpose({ openModal })
</script>
