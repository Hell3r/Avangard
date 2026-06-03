<template>
  <header class="bg-white border-b h-[80px] px-6 flex items-center justify-between">
    <button
      class="bg-[#1F5D3A] hover:bg-[#17482D] text-white px-5 py-3 rounded-xl"
      @click="openCreateTaskModal"
    >
      + Создать задачу
    </button>

    <div class="flex items-center space-x-4">
      <button
        class="bg-red-600 hover:bg-red-700 text-white px-5 py-3 rounded-xl"
        @click="logout"
      >
        Выйти
      </button>
      <CreateTaskModal ref="createTaskModalRef" />
    </div>
  </header>
</template>


<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import CreateTaskModal from './CreateTaskModal.vue'

const createTaskModalRef = ref<InstanceType<typeof CreateTaskModal> | null>(null)


const router = useRouter()
const authStore = useAuthStore()

function openCreateTaskModal() {
  createTaskModalRef.value?.openModal()
}

function logout() {
  authStore.logout()
  router.push({ name: 'login-page' })
}
</script>



