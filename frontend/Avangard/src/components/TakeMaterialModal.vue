<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-2xl p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold">Взять материал со склада</h3>
          <div class="mt-1 text-sm text-gray-500">Уменьшаем остаток</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>

      <div class="mt-4 border rounded-xl p-4 bg-[#F4F6F5]" v-if="selectedStorage">
        <div class="text-sm text-gray-500">Материал</div>
        <div class="font-semibold">{{ selectedStorage.material_name }}</div>
        <div class="text-sm text-gray-500 mt-1">
          Остаток: <span class="font-semibold text-[#1F5D3A]">{{ selectedStorage.remainder }}</span>
        </div>
      </div>

      <form class="mt-5 space-y-4" @submit.prevent="submit">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Материал</label>
          <select
            v-model.number="form.storage_id"
            class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            required
          >
            <option v-for="m in storageStore.storages" :key="m.id" :value="m.id">
              {{ m.material_name }} ({{ m.remainder }})
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Количество</label>
          <input
            v-model.number="form.quantity"
            type="number"
            min="1"
            step="1"
            class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Комментарий (необязательно)</label>
          <textarea
            v-model.trim="form.note"
            rows="3"
            class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
            placeholder="Например: на задачу по работам"
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
            :disabled="loading || !form.storage_id"
          >
            {{ loading ? 'Списываю…' : 'Взять' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useStorageStore } from '../stores/storage'

const emit = defineEmits<{ (e: 'withdraw-done'): void }>()

const authStore = useAuthStore()
const storageStore = useStorageStore()

const open = ref(false)
const loading = ref(false)
const error = ref<string | null>(null)

const form = ref<{ storage_id: number | null; quantity: number; note: string }>({
  storage_id: null,
  quantity: 1,
  note: ''
})

const selectedStorage = computed(() => {
  if (!form.value.storage_id) return null
  return storageStore.storages.find((s) => s.id === form.value.storage_id) ?? null
})

function openModal() {
  open.value = true
  error.value = null
  loading.value = false

  if (!storageStore.storages.length) {
    void storageStore.loadStorages()
  }

  if (!form.value.storage_id && storageStore.storages.length) {
    const first = storageStore.storages[0]
    if (first) form.value.storage_id = first.id
  }
}

function openModalWithStorage(m: { id: number }) {
  open.value = true
  error.value = null
  loading.value = false
  form.value.storage_id = m.id
  form.value.quantity = 1
}

function close() {
  open.value = false
  error.value = null
  loading.value = false
  form.value = { storage_id: null, quantity: 1, note: '' }
}

async function submit() {
  if (!form.value.storage_id || !form.value.quantity) return

  loading.value = true
  error.value = null

  try {
    const token = authStore.accessToken
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (token) headers.Authorization = `Bearer ${token}`

    const res = await fetch('http://0.0.0.0:8000/v1/storage/withdraw', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        storage_id: form.value.storage_id,
        quantity: form.value.quantity,
        note: form.value.note || null,
      }),
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Withdraw failed: ${res.status} ${text}`)
    }

    await storageStore.loadStorages()
    emit('withdraw-done')
    close()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // lazy
})

defineExpose({ openModal, openModalWithStorage })
</script>

