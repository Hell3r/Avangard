<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-2xl p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold">Добавить материал на склад</h3>
          <div class="mt-1 text-sm text-gray-500">Введите название материала и количество</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>

      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Название материала</label>
          <input
            v-model.trim="form.material_name"
            type="text"
            class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            placeholder="Например: цемент"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Количество (в склад)</label>
          <input
            v-model.number="form.added"
            type="number"
            min="1"
            step="1"
            class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
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
            :disabled="loading || !form.material_name"
          >
            {{ loading ? 'Добавляю…' : 'Добавить' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useStorageStore } from '../stores/storage'
import { useAuthStore } from '../stores/auth'

type FormState = {
  material_name: string
  added: number
}

const storageStore = useStorageStore()
const authStore = useAuthStore()

const open = ref(false)
const loading = ref(false)
const error = ref<string | null>(null)

const form = ref<FormState>({
  material_name: '',
  added: 1
})

function openModal() {
  open.value = true
  error.value = null
  loading.value = false

  if (!storageStore.storages.length) {
    storageStore.loadStorages().catch(() => {})
  }
}

function close() {
  open.value = false
  error.value = null
  loading.value = false
  form.value = { material_name: '', added: 1 }
}

async function submit() {
  if (!form.value.material_name || form.value.added <= 0) return

  loading.value = true
  error.value = null

  try {
    const token = authStore.accessToken
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    }
    if (token) headers.Authorization = `Bearer ${token}`

    // Подразумевается, что backend умеет принимать material_name и added.
    // Если endpoint отличается — действие вернёт ошибку и UI покажет её.
    const res = await fetch('http://0.0.0.0:8000/v1/storage/add', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        material_name: form.value.material_name,
        added: form.value.added
      })
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Не удалось добавить материал: ${res.status} ${text}`)
    }

    await storageStore.loadStorages()
    close()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (!storageStore.storages.length) {
    storageStore.loadStorages().catch(() => {})
  }
})

defineExpose({ openModal })
</script>

