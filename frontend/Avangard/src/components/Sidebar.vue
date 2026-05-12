<template>
  <aside class="w-[260px] bg-[#1F5D3A] text-white min-h-screen p-5 flex flex-col justify-between">
    <div>
      <div class="text-3xl font-bold mb-10">Авангард</div>

      <nav class="space-y-2">
        <div class="bg-[#2E7D32] px-4 py-3 rounded-xl font-medium">Панель управления</div>
        <div class="px-4 py-3 rounded-xl hover:bg-[#2E7D32] transition">Объекты</div>
        <div class="px-4 py-3 rounded-xl hover:bg-[#2E7D32] transition">Склад</div>
        <div class="px-4 py-3 rounded-xl hover:bg-[#2E7D32] transition">Персонал</div>
        <div class="px-4 py-3 rounded-xl hover:bg-[#2E7D32] transition">Задачи</div>
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

const authStore = useAuthStore()

const authUserDisplayName = computed(() => {
  
  return (authStore.user as any)?.full_name ?? authStore.user?.username ?? '—'
})

const authRoleDisplay = computed(() => {
  const role = authStore.user?.role
  if (role === 'admin') return 'Администратор'
  if (role === 'master') return 'Менеджер'
  return role ? role : 'Сотрудник'
})
</script>

