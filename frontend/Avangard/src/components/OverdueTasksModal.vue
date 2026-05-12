<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-2xl p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold">Просроченные задачи</h3>
          <div class="mt-1 text-sm text-gray-500">Всего: {{ tasks.length }}</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>

      <div class="mt-4 space-y-3 max-h-[70vh] overflow-auto">
        <div
          v-for="t in tasks"
          :key="t.id"
          class="border rounded-xl p-3 hover:bg-gray-50 cursor-pointer"
          @click="openTask(t)"
        >
          <div class="font-semibold">{{ t.description }}</div>
          <div class="text-sm text-gray-500 mt-1">
            Назначен: {{ t.assigned_to?.full_name ?? '—' }}
          </div>
          <div class="text-xs text-gray-400 mt-1">Срок: {{ formatDate(t.due_at) }}</div>
        </div>

        <div v-if="!tasks.length" class="text-sm text-gray-500">
          Нет просроченных задач
        </div>
      </div>

      <!-- detail modal (task) -->
      <div
        v-if="selectedTask"
        class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
        @click.self="closeTask"
      >
        <div class="bg-white rounded-2xl shadow-lg w-full max-w-xl p-5">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h3 class="text-xl font-bold">Задача #{{ selectedTask.id }}</h3>
              <div class="mt-2 text-gray-700">{{ selectedTask.description }}</div>
            </div>
            <button class="text-gray-500 hover:text-gray-800" @click="closeTask">✕</button>
          </div>

          <div class="mt-4 space-y-2 text-sm">
            <div><b>Назначен:</b> {{ selectedTask.assigned_to?.full_name ?? '—' }}</div>
            <div><b>Создана:</b> {{ formatDate(selectedTask.created_at) }}</div>
            <div><b>Срок сдачи:</b> {{ selectedTask.due_at ? formatDate(selectedTask.due_at) : '—' }}</div>
            <div><b>Статус:</b> {{ selectedTask.status }}</div>
            <div><b>Выполнена:</b> {{ selectedTask.completed_at ? formatDate(selectedTask.completed_at) : '—' }}</div>
          </div>

          <div class="mt-5 text-right">
            <button class="bg-[#1F5D3A] text-white px-4 py-2 rounded-xl" @click="closeTask">
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useTasksStore, type Task } from '../stores/tasks'

const tasksStore = useTasksStore()

const open = ref(false)
const selectedTask = ref<Task | null>(null)

const tasks = computed(() => {
  return tasksStore.tasks.filter((t) => t.status === 'Просрочено')
})

function openModal() {
  open.value = true
}

function close() {
  open.value = false
  selectedTask.value = null
}


async function refreshTasks() {
  await tasksStore.loadTasks()
}


function openTask(t: Task) {
  selectedTask.value = t
}

function closeTask() {
  selectedTask.value = null
}

function formatDate(iso: string) {
  try {
    return new Date(iso).toLocaleString('ru-RU')
  } catch {
    return iso
  }
}

// expose to parent
defineExpose({ openModal })
</script>

