<template>
  <div class="flex min-h-screen bg-[#F4F6F5]">
    <Sidebar />

    <div class="flex-1 flex flex-col">
      <Topbar />

      <main class="p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
import Topbar from '../components/Topbar.vue'
</script>
