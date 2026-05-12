<template>
  <div class="min-h-screen flex items-center justify-center bg-[#F4F6F5]">
    <div class="w-[380px] bg-white rounded-2xl shadow-lg p-8 text-center">

      <div class="mb-6">
        <h1 class="text-2xl font-bold text-[#1F5D3A]">
          Авангард
        </h1>

        <p class="text-sm text-gray-500">
          Система управления строительством
        </p>
      </div>

      <h2 class="text-xl font-semibold mb-6">
        Вход в систему
      </h2>

      <div v-if="error" class="mb-4 text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl p-3">
        {{ error }}
      </div>

      <form class="space-y-4" @submit.prevent="onSubmit">

        <input
          v-model="username"
          type="text"
          placeholder="Введите логин"
          class="w-full px-4 py-3 border rounded-xl"
          autocomplete="username"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Введите пароль"
          class="w-full px-4 py-3 border rounded-xl"
          autocomplete="current-password"
        />

        <button
          type="submit"
          class="w-full bg-[#1F5D3A] hover:bg-[#17482D] text-white py-3 rounded-xl"
          :disabled="loading"
        >
          <span v-if="!loading">Войти</span>
          <span v-else>Проверка...</span>
        </button>

      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

const forbiddenQuery = computed(() => route.query.error === 'forbidden')

watch(
  forbiddenQuery,
  (val) => {
    if (val) error.value = 'Доступ только для admin'
  },
  { immediate: true }
)

async function onSubmit() {
  error.value = null

  if (!username.value.trim() || !password.value) {
    error.value = 'Введите логин и пароль'
    return
  }

  loading.value = true
  try {
    await auth.login(username.value.trim(), password.value)

    if (auth.user?.role !== 'admin') {
      error.value = 'Доступ только для admin'
      auth.logout()
      return
    }

    await router.push({ name: 'dashboard' })
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

