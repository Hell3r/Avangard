<template>
  <div class="rounded-2xl p-5 text-white shadow-lg" :class="cardColor">
    <div class="text-4xl font-bold">
      {{ value }}
    </div>

    <div class="mt-2 text-sm">
      {{ title }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  value: string
  color: string
}>()

const cardColor = computed(() => {
  switch (props.color) {
    case 'green':
      return 'bg-green-600'
    case 'red':
      return 'bg-red-500'
    case 'yellow':
      return 'bg-yellow-500'
    case 'orange':
      return 'bg-orange-500'
    default:
      return 'bg-gray-500'
  }
})
</script>
