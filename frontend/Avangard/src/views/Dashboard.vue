<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-blue-900 p-8">
    <div class="max-w-6xl mx-auto">
      <header class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-4xl font-bold text-white">Панель управления</h1>
          <p class="text-slate-400">Добро пожаловать, {{ user?.name || user?.email }}!</p>
        </div>
        <button @click="signOut" class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-xl font-medium transition-colors">
          Выйти
        </button>
      </header>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/20">
          <h3 class="text-xl font-bold text-white mb-4">Строительные задачи</h3>
          <p class="text-slate-400">Список активных задач...</p>
        </div>
        <div class="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/20">
          <h3 class="text-xl font-bold text-white mb-4">Склад</h3>
          <p class="text-slate-400">Управление запасами...</p>
        </div>
        <div class="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/20">
          <h3 class="text-xl font-bold text-white mb-4">Адреса</h3>
          <p class="text-slate-400">Объекты строительства...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const user = authStore.user

const signOut = async () => {
  await authStore.signOut()
}
</script>

