<script setup>
import NavBar from "@/components/NavBar.vue";

</script>
<!-- Oder selected equipement  -->
<template>
  <NavBar>
    <v-card class="main-card" variant="outlined">
      <v-card-item class="bg-orange-darken-4">
        <v-card-title class="text-wrap">
          {{ alrdyIn2Cart ? $CONFIG_FRONT_TXT.order_equipement.cart_label : $CONFIG_FRONT_TXT.order_equipement.equipement_to_order_label }}
          {{ materielNameToOrder }}
        </v-card-title>

        <template v-slot:append>
          <div class="d-flex align-center ga-2">
            <!-- Bouton de retour -->
            <router-link :to="{ path: previous_path }" custom v-slot="{ href, navigate }">
              <v-btn :href="href" @click="navigate"
                icon class="ma-2 pa-2"
                >
                <v-icon>mdi-keyboard-backspace</v-icon>
                <v-tooltip activator="parent" location="start">
                  {{ $CONFIG_FRONT_TXT.commun.back_btn_label }}
                </v-tooltip>
              </v-btn>
            </router-link>
          </div>
          <!-- ancien bouton retour mauvais hover donc refait differemennt
          <router-link :to="{ path: previous_path }" tag="v-list-item">
            <v-btn href="#" icon="" :class="{ 'ma-2 pa-2': true }">
              <v-icon> mdi-keyboard-backspace </v-icon>
              <v-tooltip activator="parent" location="start">{{
                $CONFIG_FRONT_TXT.commun.back_btn_label
              }}</v-tooltip>
            </v-btn>
          </router-link>-->

          <div class="d-flex flex-column flex-sm-row align-center ga-2">
            <!-- Bouton ajouter au panier -->
            <v-btn href="#" @click="addArticleToCart">
              {{ alrdyIn2Cart ? $CONFIG_FRONT_TXT.order_equipement.toModif2Cart_label : $CONFIG_FRONT_TXT.order_equipement.addToCart_button }}
            </v-btn>
            <!-- bouton commander sans panier-->
            <v-btn v-if="isCartEmpty" href="#" @click="order">
              {{ $CONFIG_FRONT_TXT.order_equipement.order_equipement_button }}
            </v-btn> 
            <!-- bon bouton a supprimer par la suite-->
            <!-- <v-btn v-else href="#" @click="orderArticle">
              {{ $CONFIG_FRONT_TXT.order_equipement.order_equipement_button }}
            </v-btn> -->
          </div>
        </template>
      </v-card-item>

      <v-list subheader>
        <v-list-subheader>
          {{
            $CONFIG_FRONT_TXT.order_equipement.equipement_order_info_label
          }}</v-list-subheader
        >

        <v-list-item
          >{{ $CONFIG_FRONT_TXT.order_equipement.equipement_to_order_label }}
          {{ materielNameToOrder }}
        </v-list-item>

        <v-list-item title="Nombre de pièces à commander :">
          <v-text-field
            v-model="nombrePiece"
            label="Piece"
            :rules="numberRule"
            type="number"
            variant="outlined"
            density="compact"
            hide-details
            :min="minValue"
            :max="maxValue"
            :step="stepValue"
          >
            <template v-slot:prepend>
              <v-btn
                color="indigo-darken-3"
                density="compact"
                icon="mdi-minus"
                @click="decrement()"
              ></v-btn>
            </template>

            <template v-slot:append>
              <v-btn
                color="indigo-darken-3"
                density="compact"
                icon="mdi-plus"
                @click="increment()"
              ></v-btn>
            </template>
          </v-text-field>
        </v-list-item>
        <v-list-item title="">
          <v-autocomplete
            v-model="motif_emission"
            label="Motif"
            required
            :items="list_motifs"
          ></v-autocomplete>
        </v-list-item>

        <v-list-item title="">
          <v-textarea
            v-model="commentaire_emission"
            label="Commentaire"
            variant="outlined"
          ></v-textarea>
        </v-list-item>
      </v-list>
    </v-card>
  </NavBar>

  <!-- <Toast /> -->
</template>

<script>
import { useUserStore } from "@/stores/user";
import { usePanierStore } from "@/stores/panier";
import moment from "moment";

export default {
  data() {
    return {
      panierStore: usePanierStore(),

      materielNameToOrder: "",
      minValue: 1,
      maxValue: 10000,
      stepValue: 1,
      nombrePiece: 1,
      alrdyIn2Cart: false,
      userStore: useUserStore(),
      commentaire_emission: "",
      motif_emission: "",
      list_motifs: [
        "Supplément : Besoin de matériel supplémentaire",
        "Défectueux : le matériel ne fonctionne plus",
        "Absent : le matériel n'a jamais été remis",
        "Perdu : le matériel a été perdu",
        "Donné: le matériel a été donné",
        "Obsolète : le matériel est à renouveler car la version n'est plus adaptée",
      ],
      previous_path: "",
      materie_crud_api: `${this.$back_api_base_url}/materielcrud`,
      numberRule: [
        (val) => {
          if (val < 1) return "Please enter a positive number";
          if (val > this.maxValue) return "Please enter a positive number";
          return true;
        },
      ],
    };
  },

  computed: {
    isCartEmpty() {
      return this.panierStore.size === 0;
    },
  },

  created() {
    this.previous_path = "/inventaire_commande/" + this.$route.params.famille;

    fetch(`${this.materie_crud_api}/${this.$route.params.materiel_id}`)
      .then((reponse) => reponse.json())
      .then((josn_repsonse) => {
        this.materielNameToOrder = josn_repsonse.nom;
        this.materiel_id = this.$route.params.materiel_id;
      });
    this.motif_emission = this.list_motifs[0];

    // Stop the page from loading after 5 seconds
    // setTimeout(function () {
    //     window.stop();

    // }.bind(this), 1000);

    // this.ajouterExemple();
    // console.log("panier",panierStore.articles);
  },

  watch: {
    nombrePiece: {
      handler(new_value, old_value) {
        if (new_value > 10) {
          this.$toast.add({
            severity: "error",
            summary: "Giga commande",
            detail: "Nombre de pièces commandé supérieur à 10",
            life: 3000, // Adjust the duration the toast will be visible
          });
        }
      },
    },
  },

  mounted() {
    const art = this.panierStore.articles.find(
      i => i.materiel_id == this.$route.params.materiel_id && i.inventaire_id == this.$route.params.inventaire_id);
    if(art) {
      this.nombrePiece = art.nombre_piece;
      this.commentaire_emission = art.commentaire_emission;
      this.motif_emission = art.motif_emission;
      this.alrdyIn2Cart = true;
    }
    else
      this.alrdyIn2Cart=false;
  },

  methods: {
    increment() {
      if (this.nombrePiece < this.maxValue) {
        this.nombrePiece = Number(this.nombrePiece);
        this.nombrePiece += this.stepValue;
        this.changed = true;
        this.isBlinking = true;
      }
    },
    decrement() {
      if (this.nombrePiece > this.minValue) {
        this.nombrePiece = Number(this.nombrePiece);
        this.nombrePiece -= this.stepValue;
        this.changed = true;
        this.isBlinking = true;
      }
    },

    addArticleToCart() {
      let article = {
        user_pseudo: this.userStore.user.pseudo,
        inventaire_id: this.$route.params.inventaire_id,
        materiel_id: this.$route.params.materiel_id,
        motif_emission: this.motif_emission,
        commentaire_emission: this.commentaire_emission,
        nombre_piece: this.nombrePiece,
        famille : this.$route.params.famille
      };
      try {
        this.panierStore.ajouterArticle(this.$back_api_base_url, article);
        setTimeout(() => {
          this.$router.push({
            path: '/inventaire_commande/' + this.$route.params.famille,
            query: { toast: 'toast', message: this.alrdyIn2Cart ?
            this.$CONFIG_FRONT_TXT.order_equipement.modifiedCart_label : this.$CONFIG_FRONT_TXT.order_equipement.addedToCart_label, life: 2000 }
          });
        }, 100);
      } catch(error) {
        console.log(error)
        this.$toast.add({
          severity: "error",
          summary: "Impossible d'ajouter au panier",
          life: 3000,
        })
      }
    }, 

    order() {
      // Implement the logic for the 'commander' button for the specific item
      // console.log(`Commander ${this.materielNameToOrder} with value ${this.nombrePiece}`);
      let date = moment(new Date());
      const isoString = date.format();

      let postData = {
        inventaire_id: this.$route.params.inventaire_id,
        utilisateur_demandeur: {
          matricule: this.userStore.user.matricule,
          pseudo: this.userStore.user.pseudo,
        },
        materiel_id: this.$route.params.materiel_id,
        date_emission: isoString,
        motif_emission: this.motif_emission,
        commentaire_emission: this.commentaire_emission,
        nombre_piece: this.nombrePiece,
        group_command: false
      };

      fetch(this.$back_api_base_url + "/commande", {
        method: "Post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      })
        .then((response) => response.json())
        .then((josn_repsonse) => {
          let depot_commande_response_json = josn_repsonse;
          if (depot_commande_response_json.error == 0) {
            //affiche un toast sur la page précédente
            setTimeout(() => {
              this.$router.push({ path: '/inventaire_commande/' + this.$route.params.famille,
              query: { toast: 'toast', message: this.$CONFIG_FRONT_TXT.order_equipement.ordered_label, life: 3000 } });
            });
          } else if (depot_commande_response_json.error == 1) {
            // Show a toast
            this.$toast.add({
              severity: "error",
              summary: "commande echoué",
              detail: depot_commande_response_json.message,
              life: 3000, // Adjust the duration the toast will be visible
            });
          }
        });
    },
  }
};
</script>

<style>
.blink {
  background-color: red;
  color: aqua;
  animation: blinkAnimation 1s infinite;
  /* Adjust the duration as needed */
}

@keyframes blinkAnimation {
  0%,
  100% {
    opacity: 1;
    background-color: rgb(255, 255, 255);
  }

  50% {
    opacity: 0.5;
    background-color: rgb(255, 0, 0);
  }
}

.mobile {
  display: flex;
  flex-direction: row;
}
</style>

<style scoped>
@media (max-width: 700px) {
  .v-list-item {
    display: flex;
    flex-direction: column;
  }
}
</style>
