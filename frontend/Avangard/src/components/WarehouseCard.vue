<template>
  <div class="bg-white rounded-2xl p-5 shadow-sm">
    <h2 class="text-xl font-semibold mb-5">Склад</h2>

    <div class="space-y-4">
      <div
        v-for="s in storagesLimited"
        :key="s.id"
        class="border-b pb-3 flex justify-between"
      >
        <div>
          <div class="font-medium">{{ s.material_name }}</div>
          <div class="text-sm text-gray-500">{{ s.description || '—' }}</div>
        </div>

        <div
          :class="[
            'font-bold',
            s.remainder <= 5 ? 'text-red-500' : 'text-yellow-500'
          ]"
        >
          {{ s.remainder }}
        </div>
      </div>

      <div v-if="!storages.length" class="text-sm text-gray-500">
        Нет данных
      </div>
    </div>

    <button class="mt-6 w-full bg-[#1F5D3A] text-white py-3 rounded-xl">
      Добавить материал
    </button>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useStorageStore } from '../stores/storage'

const storageStore = useStorageStore()

const storages = computed(() => storageStore.storages)

// выводим только 2 последних (как в шаблоне)
const storagesLimited = computed(() => {
  const all = storages.value
  return [...all].slice(-2)
})

onMounted(() => {
  storageStore.loadStorages()
})
</script>
