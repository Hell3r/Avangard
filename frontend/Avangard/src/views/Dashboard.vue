<template>
  <DashboardLayout>
    <div class="space-y-6">

      <div>
        <h1 class="text-3xl font-bold text-gray-800">
          Панель управления
        </h1>
      </div>

      <div class="grid grid-cols-4 gap-4">
        <StatCard title="Сейчас на объекте" :value="onSiteCount.toString()" color="green" />
        <StatCard title="Отсутствуют" :value="offSiteCount.toString()" color="red" />
        <div class="cursor-pointer" @click="openLowMaterialsModal">
          <StatCard
            title="Материалы на исходе"
            :value="materialsOutCount.toString()"
            color="yellow"
          />
        </div>
        <div class="cursor-pointer" @click="openOverdueModal">
          <StatCard :title="'Просроченные задачи'" :value="overdueTasksCount.toString()" color="orange" />
        </div>

        <OverdueTasksModal ref="overdueModalRef" />

        <LowMaterialsModal ref="lowMaterialsModalRef" />
      </div>




      <div class="grid grid-cols-12 gap-6">
        <div class="col-span-4">
          <WarehouseCard />
        </div>

        <div class="col-span-5">
          <TasksBoard />
        </div>

        <div class="col-span-3">
          <StaffCard />
        </div>
      </div>

      <EventJournal />

    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import StatCard from '../components/StatCard.vue'
import WarehouseCard from '../components/WarehouseCard.vue'
import TasksBoard from '../components/TasksBoard.vue'
import StaffCard from '../components/StaffCard.vue'
import EventJournal from '../components/EventJournal.vue'
import OverdueTasksModal from '../components/OverdueTasksModal.vue'
import LowMaterialsModal from '../components/LowMaterialsModal.vue'
import { useStorageStore } from '../stores/storage'
import { useAuthStore } from '../stores/auth'
import { useTasksStore } from '../stores/tasks'

const storageStore = useStorageStore()
const authStore = useAuthStore()

const tasksStore = useTasksStore()
const overdueTasksCount = computed(() => {
  return tasksStore.tasks.filter((t) => t.status === 'Просрочено').length
})

const overdueModalRef = ref<InstanceType<typeof OverdueTasksModal> | null>(null)
const lowMaterialsModalRef = ref<InstanceType<typeof LowMaterialsModal> | null>(null)

function openOverdueModal() {
  overdueModalRef.value?.openModal()
}

function openLowMaterialsModal() {
  lowMaterialsModalRef.value?.openModal()
}


const onSiteCount = ref(0)
const offSiteCount = ref(0)

const materialsOutCount = computed(() => {
  return storageStore.storages.filter((s) => s.remainder <= 5).length
})

async function loadStaffStats() {

  const token = authStore.accessToken
  const headers: Record<string, string> = token
    ? { Authorization: `Bearer ${token}` }
    : {}

  // Сначала пробуем получить on-site список
  // (мастер и админ используют разные endpoints, но оба возвращают список on-site)
  try {
    // Попробуем мастер endpoint
    const resMaster = await fetch('http://0.0.0.0:8000/v1/users/on-site?skip=0&limit=100', {
      headers
    })

    let onSiteUsers: any[] = []

    if (resMaster.ok) {
      onSiteUsers = (await resMaster.json()) as any[]
    } else {
      // Если мастер endpoint запрещён — значит админ/другие роли
      const resAdmin = await fetch('http://0.0.0.0:8000/v1/users/on-site/all?skip=0&limit=100', {
        headers
      })
      if (resAdmin.ok) {
        onSiteUsers = (await resAdmin.json()) as any[]
      }
    }

    onSiteCount.value = onSiteUsers.length

    try {
    const resAll = await fetch('http://0.0.0.0:8000/v1/users/active?skip=0&limit=1000', {
        headers
      })

      if (resAll.ok) {
        const allUsers = (await resAll.json()) as any[]
        const onSiteIds = new Set(onSiteUsers.map((u) => u.id))
        offSiteCount.value = allUsers.filter((u) => !onSiteIds.has(u.id)).length
      } else {
        offSiteCount.value = 0
      }
    } catch {
      offSiteCount.value = 0
    }
  } catch {
    onSiteCount.value = 0
    offSiteCount.value = 0
  }
}

onMounted(async () => {
  await storageStore.loadStorages()
  await loadStaffStats()
})
</script>


