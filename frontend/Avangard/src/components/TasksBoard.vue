<template>
  <div class="bg-white rounded-2xl p-5 shadow-sm">
    <div class="flex justify-between mb-6">
      <h2 class="text-xl font-semibold">Задачи</h2>

    </div>

    <div class="space-y-4">
      <div class="border rounded-xl p-4">
        <div class="flex justify-between">
          <div class="font-semibold">В работе</div>
          <div class="text-red-500 text-sm">{{ activeTasks.length }}</div>
        </div>

        <div class="mt-3 space-y-3">
          <button
            v-for="t in limitedActiveTasks"
            :key="t.id"
            class="w-full text-left border rounded-lg p-3 hover:bg-gray-50"
            @click="openTask(t)"
          >
            <div class="font-semibold">{{ t.description }}</div>
            <div class="text-sm text-gray-500">Сотрудник: {{ t.assigned_to?.full_name ?? '—' }}</div>
          </button>

          <div v-if="extraActiveCount > 0" class="text-sm text-gray-500">+ {{ extraActiveCount }} задач</div>
          <div v-else-if="!activeTasks.length" class="text-sm text-gray-500">Нет задач</div>
        </div>
      </div>

      <!-- Выполнено -->
      <div class="border rounded-xl p-4">
        <div class="flex justify-between">
          <div class="font-semibold">Выполнено</div>
          <div class="text-green-600 text-sm">{{ completedTasks.length }}</div>
        </div>

        <div class="mt-3 space-y-3">
          <button
            v-for="t in limitedCompletedTasks"
            :key="t.id"
            class="w-full text-left border rounded-lg p-3 hover:bg-gray-50"
            @click="openTask(t)"
          >
            <div class="font-semibold">{{ t.description }}</div>
            <div class="text-sm text-gray-500">Подрядчик: {{ t.assigned_to?.full_name ?? '—' }}</div>
          </button>

          <div v-if="extraCompletedCount > 0" class="text-sm text-gray-500">+ {{ extraCompletedCount }} задач</div>
          <div v-else-if="!completedTasks.length" class="text-sm text-gray-500">Нет выполненных задач</div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div
      v-if="selectedTask"
      class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
      @click.self="closeTask"
    >
      <div class="bg-white rounded-2xl shadow-lg w-full max-w-xl p-5">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h3 class="text-xl font-bold">Задача #{{ selectedTask.id }}</h3>
            <div class="mt-2 text-gray-600">{{ selectedTask.description }}</div>
          </div>
          <button class="text-gray-500 hover:text-gray-800" @click="closeTask">✕</button>
        </div>

        <div class="mt-4 space-y-2 text-sm">
          <div><b>Cотрудник:</b> {{ selectedTask.assigned_to?.full_name ?? '—' }}</div>

          <div><b>Создана:</b> {{ formatDate(selectedTask.created_at) }}</div>

          <div>
            <b>Срок сдачи:</b> {{ selectedTask.due_at ? formatDate(selectedTask.due_at) : '—' }}
          </div>

          <div><b>Статус:</b> {{ selectedTask.status }}</div>

          <div>
            <b>Выполнена:</b>
            {{ selectedTask.completed_at ? formatDate(selectedTask.completed_at) : '—' }}
          </div>
        </div>


        <div class="mt-5 text-right">
          <button
            class="bg-[#1F5D3A] text-white px-4 py-2 rounded-xl"
            @click="closeTask"
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useTasksStore, type Task } from '../stores/tasks'

const tasksStore = useTasksStore()

onMounted(async () => {
  await tasksStore.loadTasks()
})

const activeTasks = computed(() => tasksStore.tasks.filter(t => t.status == 'В работе'))
const completedTasks = computed(() => tasksStore.tasks.filter(t => t.completed_at != null))

// limited lists for display (max 3)
const limitedActiveTasks = computed(() => activeTasks.value.slice(0, 3))
const limitedCompletedTasks = computed(() => completedTasks.value.slice(0, 3))

// extra counts
const extraActiveCount = computed(() => Math.max(activeTasks.value.length - 3, 0))
const extraCompletedCount = computed(() => Math.max(completedTasks.value.length - 3, 0))

const selectedTask = ref<Task | null>(null)

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
</script>
