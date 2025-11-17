<template>
  <v-app-bar app fixed flat color="blue lighten-1" class="px-4">
    <!-- Titre de la page (clic -> home) -->
    <router-link to="/" style="text-decoration:none; color:inherit;">
      <v-toolbar-title class="text-white" style="cursor: pointer;">
        {{ title }}
      </v-toolbar-title>
    </router-link>

    <v-spacer></v-spacer>

    <!-- Icône panier -> shop -->
    <router-link to="/shop" style="text-decoration:none; color:inherit;">
      <v-btn icon>
        <v-icon :icon="mdiCart" />
      </v-btn>
    </router-link>

    <!-- Icône livraison -> commands -->
    <router-link to="/commands" style="text-decoration:none; color:inherit;">
      <v-btn icon>
        <v-icon :icon="mdiTruck" />
      </v-btn>
    </router-link>
  </v-app-bar>
</template>

<script setup>
import { mdiHome, mdiCart, mdiTruck } from '@mdi/js'

const props = defineProps({
  title: {
    type: String,
    default: 'Demo4Flask',
  },
})
</script>
