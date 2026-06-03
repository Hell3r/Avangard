<template>
  <aside class="w-[260px] bg-[#1F5D3A] text-white min-h-screen p-5 flex flex-col justify-between">
    <div>
      <div class="text-3xl font-bold mb-10">Авангард</div>

      <nav class="space-y-2">
        <div
          class="px-4 py-3 rounded-xl hover:bg-[#2E7D32] transition cursor-pointer"
          :class="{ 'bg-[#2E7D32]': isActive('dashboard') }"
          @click="goToDashboard"
        >
          Панель управления
        </div>

        <div
          class="px-4 py-3 rounded-xl hover:bg-[#2E7D32] transition cursor-pointer"
          :class="{ 'bg-[#2E7D32]': isActive('objects') }"
          @click="goToObjects"
        >
          Объекты
        </div>

        <div
          class="px-4 py-3 rounded-xl hover:bg-[#2E7D32] transition cursor-pointer"
          :class="{ 'bg-[#2E7D32]': isActive('warehouse') }"
          @click="goToWarehouse"
        >
          Склад
        </div>

        <div
          class="px-4 py-3 rounded-xl hover:bg-[#2E7D32] transition cursor-pointer"
          :class="{ 'bg-[#2E7D32]': isActive('staff') }"
          @click="goToStaff"
        >
          Персонал
        </div>

      </nav>
    </div>

    <div class="bg-white/10 rounded-2xl p-4">
      <div class="font-semibold">{{ authUserDisplayName }}</div>
      <div class="text-sm text-gray-300">{{ authRoleDisplay }}</div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const authStore = useAuthStore()


const authUserDisplayName = computed(() => {
  const user = authStore.user as { full_name?: string | null; username?: string }
  return user.full_name ?? user.username ?? '—'
})

const authRoleDisplay = computed(() => {
  const role = authStore.user?.role
  if (role === 'admin') return 'Администратор'
  if (role === 'master') return 'Менеджер'
  return role ? role : 'Сотрудник'
})

function goToDashboard() {
  router.push({ name: 'dashboard' })
}

function isActive(routeName: string) {
  return route.name === routeName
}

function goToObjects() {
  router.push({ name: 'objects' })
}

function goToWarehouse() {
  router.push({ name: 'warehouse' })
}

function goToStaff() {
  router.push({ name: 'staff' })
}

</script>



