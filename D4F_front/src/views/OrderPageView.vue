<template>
  <v-container fluid class="pa-4">
    <v-card outlined>
      <!-- En-tête de la carte -->
      <v-card-item>
        <v-card-title>
          <!-- Titre dynamique -->
          {{ title }}
        </v-card-title>

        <template v-slot:append>
          <div class="d-flex align-center gap-2">
            <!-- Bouton retour -->
            <v-btn icon>
              <v-icon>mdi-keyboard-backspace</v-icon>
            </v-btn>

            <!-- Boutons actions -->
            <div class="d-flex gap-2">
              <v-btn>Ajouter au panier</v-btn>
              <v-btn>Commander</v-btn>
            </div>
          </div>
        </template>
      </v-card-item>

      <!-- Liste d'informations -->
      <v-list subheader>
        <v-list-subheader>Informations commande</v-list-subheader>

        <v-list-item>
          Nom de l’équipement
        </v-list-item>

        <v-list-item>
          <v-text-field label="Nombre de pièces" type="number">
            <template v-slot:prepend>
              <v-btn icon>
                <v-icon>mdi-minus</v-icon>
              </v-btn>
            </template>
            <template v-slot:append>
              <v-btn icon>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
          </v-text-field>
        </v-list-item>

        <v-list-item>
          <v-autocomplete label="Motif" :items="[]"></v-autocomplete>
        </v-list-item>

        <v-list-item>
          <v-textarea label="Commentaire"></v-textarea>
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>
</template>

<script setup>
const title = 'Commande équipement'
</script>
