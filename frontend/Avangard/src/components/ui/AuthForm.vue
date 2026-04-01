<template>
  <div>
    <div>
      <label class="block text-sm font-medium text-slate-300 mb-2">Имя пользователя</label>
      <input
        v-model="form.email"
        type="email"
        class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200"
        placeholder="your@email.com"
        :disabled="loading"
      />
      <p v-if="errors.email" class="mt-1 text-sm text-orange-400">{{ errors.email }}</p>
    </div>

    <div>
      <label class="block text-sm font-medium text-slate-300 mb-2">Пароль</label>
      <input
        v-model="form.password"
        type="password"
        class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200"
        placeholder="••••••••"
        :disabled="loading"
      />
      <p v-if="errors.password" class="mt-1 text-sm text-orange-400">{{ errors.password }}</p>
    </div>

    <button
      type="button"
      @click="handleButtonClick"
      :disabled="loading || hasError"
      class="w-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-semibold py-4 px-6 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2 mt-4"
    >
      <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></span>
      <span>Войти</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import type { LoginCredentials } from '@/types/auth'

const emit = defineEmits<{ (e: 'submit', credentials: LoginCredentials): void }>()

interface Props {
  loading?: boolean
}

const props = defineProps<Props>()

const form = reactive<LoginCredentials>({
  email: '',
  password: ''
})

const errors = ref({
  email: '',
  password: ''
})

const hasError = computed(() => errors.value.email || errors.value.password)

const validate = () => {
  errors.value.email = ''
  if (!form.email) {
    errors.value.email = 'Email обязателен'
    return false
  }
  if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.value.email = 'Неверный email'
    return false
  }

  errors.value.password = ''
  if (!form.password) {
    errors.value.password = 'Пароль обязателен'
    return false
  }
  if (form.password.length < 6) {
    errors.value.password = 'Пароль не менее 6 символов'
    return false
  }
  return true
}

const handleButtonClick = () => {
  if (validate()) {
    emit('submit', { ...form })
  }
}

defineExpose({
  form,
  validate
})
</script>

