<template>
  <div class="bg-white rounded-2xl p-5 shadow-sm">
    <div class="flex items-start justify-between gap-4 mb-5">
      <div>
        <h2 class="text-xl font-semibold">Склад</h2>
        <div class="text-sm text-gray-500 mt-1">Последние остатки и пополнение</div>
      </div>

      <button
        class="bg-[#1F5D3A] hover:bg-[#17482D] transition text-white px-4 py-2 rounded-xl text-sm font-medium"
        @click="openAddMaterialModal"
      >
        +
      </button>
    </div>

    <div class="space-y-4">
      <div
        v-for="s in storagesLimited"
        :key="s.id"
        class="border-b pb-3 flex justify-between items-start"
      >
        <div class="min-w-0">
          <div class="font-medium truncate">{{ s.material_name }}</div>
          <div class="text-sm text-gray-500 break-words">{{ s.description || '—' }}</div>
        </div>

        <div
          class="font-bold whitespace-nowrap"
          :class="s.remainder <= 0 ? 'text-red-600' : s.remainder <= 5 ? 'text-yellow-600' : 'text-green-700'"
        >
          {{ s.remainder }}
        </div>
      </div>

      <div v-if="!storages.length" class="text-sm text-gray-500">
        Нет данных
      </div>
    </div>

    <div
      v-if="storages.length > storagesLimited.length"
      class="mt-4 text-sm text-gray-400"
    >
      + ещё {{ storages.length - storagesLimited.length }}
    </div>

    <button
      class="mt-6 w-full border border-gray-200 text-gray-700 hover:bg-gray-50 py-3 rounded-xl"
      @click="openAddMaterialModal"
    >
      Добавить материал на склад
    </button>

    <AddMaterialModal ref="addMaterialModalRef" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useStorageStore } from '../stores/storage'
import AddMaterialModal from './AddMaterialModal.vue'

const storageStore = useStorageStore()

const storages = computed(() => storageStore.storages)

const storagesLimited = computed(() => {
  const all = storages.value
  return [...all].slice(-2)
})

const addMaterialModalRef = ref<InstanceType<typeof AddMaterialModal> | null>(null)

function openAddMaterialModal() {
  addMaterialModalRef.value?.openModal()
}

onMounted(() => {
  storageStore.loadStorages()
})
</script>

