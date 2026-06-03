<template>
  <div class="flex min-h-screen bg-[#F4F6F5]">
    <Sidebar />

    <div class="flex-1 flex flex-col">
      <Topbar />

      <main class="p-6">
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <div class="flex items-start justify-between gap-4 mb-5">
            <div>
              <h2 class="text-xl font-semibold">Объекты</h2>
              <div class="text-sm text-gray-500 mt-1">Список объектов (адресов)</div>
            </div>
            <button
              @click="openCreateAddressModal"
              class="px-4 py-2 bg-[#1F5D3A] text-white rounded-xl hover:bg-[#17482D] transition flex items-center gap-2"
            >
              <span>+</span>
              <span>Добавить адрес</span>
            </button>
          </div>

          <div class="grid grid-cols-12 gap-3 mb-4">
            <div class="col-span-12">
              <input
                v-model="query"
                placeholder="Поиск по адресу"
                class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
              />
            </div>
          </div>

          <div class="space-y-3 max-h-[65vh] overflow-auto pr-1">
            <div
              v-for="addr in filteredAddresses"
              :key="addr.id"
              class="border rounded-xl p-4 hover:bg-gray-50 cursor-pointer"
              @click="openDetails(addr)"
            >
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <div class="font-semibold truncate">{{ addr.name }}</div>
                  <div class="text-sm text-gray-500">ID: {{ addr.id }}</div>
                </div>
                <div class="text-sm font-semibold text-[#1F5D3A] whitespace-nowrap">
                  {{ getStatusBadge(addr.id) }}
                </div>
              </div>
            </div>

            <div v-if="!filteredAddresses.length" class="text-sm text-gray-500">Объекты не найдены</div>
          </div>

          <ObjectDetailsModal ref="detailsModalRef" />
          <CreateAddressModal ref="createAddressModalRef" @address-created="onAddressCreated" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import Topbar from '../components/Topbar.vue'
import ObjectDetailsModal from '../components/ObjectDetailsModal.vue'
import { useAuthStore } from '../stores/auth'
import CreateAddressModal from '../components/CreateAddressModal.vue'

type AddressRow = {
  id: number
  name: string
}

type AddressWithUsersMeta = {
  address_id: number
  on_site_count?: number
}

const auth = useAuthStore()
const query = ref('')
const addresses = ref<AddressRow[]>([])
const detailsModalRef = ref<InstanceType<typeof ObjectDetailsModal> | null>(null)
const createAddressModalRef = ref<InstanceType<typeof CreateAddressModal> | null>(null)

const filteredAddresses = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return addresses.value
  return addresses.value.filter((a) => (a.name || '').toLowerCase().includes(q))
})

function getStatusBadge(_addressId: number) {
  return 'Открыть информацию по объекту'
}

async function loadAddresses() {
  const headers: Record<string, string> = auth.accessToken ? { Authorization: `Bearer ${auth.accessToken}` } : {}
  const res = await fetch(`http://0.0.0.0:8000/v1/addresses?skip=0&limit=1000`, { headers })

  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Failed to load addresses: ${res.status} ${text}`)
  }

  addresses.value = (await res.json()) as AddressRow[]
}

function openDetails(addr: AddressRow) {
  detailsModalRef.value?.openModal(addr)
}

function openCreateAddressModal() {
  createAddressModalRef.value?.openModal()
}

function onAddressCreated(newAddr: any) {
  // prepend or push new address and refresh list
  addresses.value = [newAddr, ...addresses.value]
}

onMounted(async () => {
  await loadAddresses()
})
</script>

