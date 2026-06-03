<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-md p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold text-gray-900">Добавить адрес</h3>
          <div class="mt-1 text-sm text-gray-500">Создание нового объекта</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>

      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Название адреса</label>
          <input
            v-model="form.name"
            type="text"
            class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            placeholder="Например: г. Москва, ул. Ленина, д. 1"
            required
          />
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
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const emit = defineEmits<{ (e: 'address-created', address: any): void }>()

const auth = useAuthStore()

const open = ref(false)
const loading = ref(false)
const error = ref<string | null>(null)

const form = ref({
  name: ''
})

async function openModal() {
  open.value = true
  error.value = null
  loading.value = false
  form.value.name = ''
}

async function close() {
  open.value = false
}

async function submit() {
  if (!form.value.name.trim()) {
    error.value = 'Название адреса обязательно'
    return
  }

  loading.value = true
  error.value = null

  try {
    const headers: Record<string, string> = auth.accessToken ? { 
      Authorization: `Bearer ${auth.accessToken}`,
      'Content-Type': 'application/json'
    } : { 'Content-Type': 'application/json' }

    const res = await fetch('http://0.0.0.0:8000/v1/addresses', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        name: form.value.name.trim()
      })
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Не удалось создать адрес: ${res.status} ${text}`)
    }

    const newAddress = await res.json()
    emit('address-created', newAddress)
    close()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Произошла ошибка'
  } finally {
    loading.value = false
  }
}

defineExpose({
  openModal
})
</script>