<template>
  <v-app>
    <NavBar />

    <v-main>
      <v-container fluid class="pa-4">
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import { RouterView } from 'vue-router'
</script>
