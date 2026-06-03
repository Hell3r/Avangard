<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-2xl p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold">Материал</h3>
          <div class="mt-1 text-sm text-gray-500">Информация и действия</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>

      <div v-if="item" class="mt-4 space-y-2 text-sm">
        <div><b>Наименование:</b> {{ item.material_name }}</div>
        <div><b>Описание:</b> {{ item.description || '—' }}</div>
        <div><b>Остаток:</b> {{ item.remainder }}</div>
      </div>

      <div v-else class="mt-4 text-sm text-gray-500">Выберите материал</div>

      <div class="mt-5 text-right">
        <button class="bg-[#1F5D3A] text-white px-4 py-2 rounded-xl" @click="close">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

type StorageRow = {
  id: number
  material_name: string
  description?: string | null
  remainder: number
}

const open = ref(false)
const item = ref<StorageRow | null>(null)

function openModal(i: StorageRow) {
  item.value = i
  open.value = true
}

function close() {
  open.value = false
  item.value = null
}

defineExpose({ openModal })
</script>

