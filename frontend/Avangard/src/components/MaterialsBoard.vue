<template>
  <div class="flex min-h-screen bg-[#F4F6F5]">
    <Sidebar />

    <div class="flex-1 flex flex-col">
      <Topbar />

      <main class="p-6">
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <div class="flex items-start justify-between gap-4 mb-5">
            <div>
              <h2 class="text-xl font-semibold">Склад</h2>
              <div class="text-sm text-gray-500 mt-1">Список материалов</div>
              <button @click="addMaterialModalRef?.openModal()" class="mt-2 bg-[#1F5D3A] text-white px-4 py-2 rounded-xl hover:bg-[#17482D] transition">Добавить материал</button>
            </div>
          </div>

          <div class="grid grid-cols-12 gap-3 mb-4">
            <div class="col-span-12">
              <input
                v-model="query"
                placeholder="Поиск по материалу"
                class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
              />
            </div>
          </div>

          <div class="space-y-3 max-h-[65vh] overflow-auto pr-1">
            <div
              v-for="m in filteredMaterials"
              :key="m.id"
              class="border rounded-xl p-4 hover:bg-gray-50 cursor-pointer flex items-start justify-between gap-4"
              @click="openDetails(m)"
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

            <div v-if="!filteredMaterials.length" class="text-sm text-gray-500">
              Материалов не найдено
            </div>
          </div>

          <MaterialDetailsModal ref="detailsModalRef" />
          <AddMaterialModal ref="addMaterialModalRef" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useStorageStore } from '../stores/storage'
import MaterialDetailsModal from './MaterialDetailsModal.vue'
import AddMaterialModal from './AddMaterialModal.vue'
import Sidebar from './Sidebar.vue'
import Topbar from './Topbar.vue'

type StorageRow = {
  id: number
  material_name: string
  description?: string | null
  remainder: number
}

const storageStore = useStorageStore()
const query = ref('')

const detailsModalRef = ref<InstanceType<typeof MaterialDetailsModal> | null>(null)
const addMaterialModalRef = ref<InstanceType<typeof AddMaterialModal> | null>(null)

onMounted(() => {
  if (!storageStore.storages.length) storageStore.loadStorages()
})

const materials = computed(() => storageStore.storages as StorageRow[])

const filteredMaterials = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return materials.value
  return materials.value.filter((m) => (m.material_name || '').toLowerCase().includes(q))
})

function openDetails(m: StorageRow) {
  detailsModalRef.value?.openModal(m)
}
</script>

