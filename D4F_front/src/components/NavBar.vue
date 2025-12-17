<template>
  <v-app-bar app fixed flat color="blue lighten-1" class="px-4">
    <v-spacer></v-spacer>
    <router-link to="/" class="title-link nav-btn center-title" style="text-decoration:none; color:inherit;">
      <v-btn text title="Accueil" class="brand title-btn" style="cursor: pointer;" aria-label="Accueil">
        {{ title }}
      </v-btn>
    </router-link>

    <v-spacer></v-spacer>

    <router-link to="/shop" class="nav-btn" style="text-decoration:none; color:inherit;">
      <v-btn icon title="Shop">
        <v-icon :icon="mdiCart" />
      </v-btn>
    </router-link>

    <router-link to="/commands" class="nav-btn" style="text-decoration:none; color:inherit;">
      <v-btn icon title="Commandes">
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

<style scoped>
/* Title sizing and centering */
.title-link {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 1 auto;
}

.brand {
  font-size: 1.45rem;
  font-weight: 600;
  line-height: 1;
  text-align: center;
}

.v-app-bar {
  position: relative;
}

.center-title {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 5;
  white-space: nowrap;
}

@media (max-width: 600px) {
  .brand {
    font-size: 1.1rem;
  }
}

/* Stronger hover for navbar icon buttons */
.nav-btn {
  display: inline-flex;
  align-items: center;
}

.nav-btn .v-btn {
  transition: transform 0.12s ease, background-color 0.12s ease, box-shadow 0.12s ease;
  border-radius: 8px;
}

.nav-btn .v-btn:hover {
  transform: translateY(-3px) scale(1.08);
  background-color: rgba(255,255,255,0.12) !important;
  box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}

.nav-btn .v-btn:active {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}

/* Apply same hover/active visual style to the centered items */

.title-link .brand {
  transition: transform 0.12s ease, background-color 0.12s ease, box-shadow 0.12s ease;
  padding: 6px 10px;
  border-radius: 8px;
}

.title-link:hover .brand {
  transform: translateY(-3px) scale(1.08);
  background-color: rgba(255,255,255,0.12) !important;
  box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}

.title-link:active .brand {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}
</style>
