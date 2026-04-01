<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900/50 to-slate-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white/5 backdrop-blur-xl shadow-2xl rounded-3xl border border-white/20 p-8 space-y-8">
      <!-- Header -->
      <div class="text-center space-y-4">
        <div class="w-24 h-24 bg-gradient-to-r from-orange-500 to-amber-500 rounded-2xl mx-auto flex items-center justify-center shadow-xl">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tight text-white">Avangard</h1>
          <p class="text-slate-300 text-lg">Строительная компания</p>
        </div>
        <p class="text-slate-400 text-sm max-w-xs mx-auto">Войдите в свой аккаунт для доступа к панели управления</p>
      </div>

      <AuthForm :loading="loading" @submit="handleSubmit" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import AuthForm from '@/components/ui/AuthForm.vue'
import type { LoginCredentials } from '@/types/auth'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)

const handleSubmit = async (credentials: LoginCredentials) => {
  loading.value = true
  try {
    await authStore.signIn(credentials)
  } catch (error) {
    console.error('Auth error:', error)
    alert('Ошибка авторизации')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped></style>

