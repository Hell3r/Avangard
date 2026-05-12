<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-2xl p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold">Материалы на исходе</h3>
          <div class="mt-1 text-sm text-gray-500">Всего: {{ items.length }}</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>

      <div class="mt-4 space-y-3 max-h-[70vh] overflow-auto">
        <div
          v-for="m in items"
          :key="m.id"
          class="border rounded-xl p-3 flex justify-between items-start gap-3"
        >
          <div class="min-w-0">
            <div class="font-semibold truncate">{{ m.material_name }}</div>
            <div class="text-sm text-gray-500 break-words">
              {{ m.description || '—' }}
            </div>
          </div>

          <div class="font-bold text-yellow-600 whitespace-nowrap">
            {{ m.remainder }}
          </div>
        </div>

        <div v-if="!items.length" class="text-sm text-gray-500">
          Материалов на исходе нет
        </div>
      </div>

      <div class="mt-5 text-right">
        <button
          class="bg-[#1F5D3A] text-white px-4 py-2 rounded-xl"
          @click="close"
        >
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useStorageStore, type Storage } from '../stores/storage'

const storageStore = useStorageStore()

const open = ref(false)

const items = computed(() => {
  return storageStore.storages.filter((s) => s.remainder <= 5)
})

function openModal() {
  open.value = true
  // подстрахуемся: если еще не подгружено — дернем загрузку
  if (!storageStore.storages.length && !storageStore.loading) {
    storageStore.loadStorages()
  }
}

function close() {
  open.value = false
}

onMounted(() => {
  if (!storageStore.storages.length) {
    storageStore.loadStorages()
  }
})

defineExpose({ openModal })
</script>

