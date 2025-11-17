<template>
  <v-app>
    <!-- NavBar fixée en haut -->
    <NavBar title="Page Exemple" />

    <!-- v-main s'adapte à la présence de l'app-bar -->
    <v-main>
      <!-- container prend toute la hauteur disponible ; d-flex + align/justify centre le contenu -->
      <v-container class="fill-height d-flex align-center justify-center">
        <v-card class="pa-6" elevation="3" max-width="900">
          <h1 class="text-h5 mb-4 text-center">Titre de la page</h1>

          <div class="text-body-1">
            <p>
              Ceci est une page basique avec un corps de texte centré. Remplace ce texte
              par le contenu souhaité (paragraphe, composants, formulaires, etc.).
            </p>

            <p>
              La barre de navigation est fixe en haut et les icônes à droite mènent aux autres pages.
            </p>
          </div>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
</script>

<style scoped>
/* si tu veux un background neutre par défaut */
.v-application {
  background-color: #fafafa;
}
</style>
