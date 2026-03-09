<template>
  <v-main>
    <v-container class="d-flex flex-column align-center" style="margin-top:2px;">
      <v-card elevation="3" class="pa-4" max-width="900" color="blue-grey lighten-5">
        <v-card-title class="text-h5 text-center">Bienvenue sur Demo4Flask — Boutique</v-card-title>
        <v-card-text class="mb-4 text-center">
          Shop — liste des différents produits. Cliquez pour voir le détail ou commander.
        </v-card-text>

        <v-divider></v-divider>

        <!-- Liste d'articles -->
        <v-virtual-scroll
          v-model="articles"
          :items="articles"
          height="60vh"
          item-height="70"
          class="v-virtual-scroll-padding-bottom"
        >
          <template v-slot:default="{ item }">
            <div
              class="article-item d-flex align-center justify-space-between"
              style="background: #fff; margin: 4px; border-radius: 6px; padding: 12px;"
            >
              <!-- Texte en colonne -->
              <div style="display: flex; flex-direction: column; gap: 4px; max-width: 70%;">
                <span class="text-h6" style="color: black;">{{ item.nom }}</span>
                <span class="text-body-2" style="color: black;">{{ item.description }}</span>
              </div>

              <!-- Bouton Détails -->
              <v-btn variant="outlined" color="primary" @click="openDetail(item)">
                Détails
                <v-icon end>mdi-open-in-new</v-icon>
              </v-btn>
            </div>
          </template>
        </v-virtual-scroll>
      </v-card>
    </v-container>

    <!-- Dialog commande -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title class="text-h6">{{ selectedArticle?.nom }}</v-card-title>
        <v-card-text>
          <div>{{ selectedArticle?.description }}</div>

          <!-- Quantité avec + / - -->
          <v-text-field
            v-model.number="quantity"
            label="Quantité"
            type="number"
            variant="outlined"
            hide-details
            :min="1"
            density="compact"
          >
            <template v-slot:prepend>
              <v-btn small text @click="decrementQuantity">-</v-btn>
            </template>

            <template v-slot:append>
              <v-btn small text @click="incrementQuantity">+</v-btn>
            </template>
          </v-text-field>
          <!-- Commentaire optionnel -->
          <v-textarea
            v-model="commentaire"
            label="Commentaire (optionnel)"
            variant="outlined"
          ></v-textarea>
        </v-card-text>

        <v-card-actions class="d-flex justify-end gap-2">
          <v-btn text @click="closeDialog">Retour</v-btn>
          <v-btn color="primary" @click="orderArticle">Commander</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-main>
</template>

<script>
import moment from "moment";

export default {
  data() {
    console.log("ShopView: using backend API base URL:", this.$back_api_base_url);
    console.log("ShopView: articles API URL:", this.$back_api_base_url + "/all_materiel");
    console.log("ShopView: single API URL:", this.$back_api_base_url + "/materiel/");
    return {
      articles: [],
      articles_api: this.$back_api_base_url + "/all_materiel",
      single_api_base: this.$back_api_base_url + "/materiel/",
      dialog: false,
      selectedArticle: null,
      quantity: 1,
      commentaire: "",
    };
  },
  created() {
    this.fetchArticles();
  },
  methods: {
    async fetchArticles() {
      try {
        const res = await fetch(this.articles_api);
        const list = await res.json();

        const detailed = await Promise.all(
          list.map(async (it) => {
            try {
              const r = await fetch(this.single_api_base + it.id);
              const d = r.ok ? await r.json() : {};
              return { id: it.id, nom: d.nom || it.nom, description: d.description || "" };
            } catch {
              return { id: it.id, nom: it.nom, description: "" };
            }
          })
        );

        this.articles = detailed;
      } catch (err) {
        console.error("Erreur fetch articles:", err);
      }
    },

    // ouvre la tuile
    openDetail(item) {
      this.selectedArticle = item;
      this.quantity = 1;
      this.commentaire = "";
      this.dialog = true;
    },

    closeDialog() {
      this.dialog = false;
    },

    incrementQuantity() {
      this.quantity = (this.quantity || 0) + 1;
    },
    decrementQuantity() {
      if (this.quantity > 1) this.quantity -= 1;
    },

    orderArticle() {
      const isoDate = moment().format();

      const payload = {
        materiel_id: this.selectedArticle.id,
        date_emission: isoDate,
        nombre_piece: this.quantity,
        commentaire_emission: this.commentaire,
      };

      // Ici tu appelleras ton API pour créer la commande
      ;(async () => {
        try {
          const res = await fetch(this.$back_api_base_url + "/commande", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          })

          const json = await res.json().catch(() => ({}))

          if (!res.ok) {
            // show backend message if any
            const msg = json && json.error ? json.error : json.message || res.statusText
            console.error('Order failed', res.status, msg)
            // try to use $toast if available
            if (this.$toast && this.$toast.add) {
              this.$toast.add({ severity: "error", summary: "Erreur", detail: String(msg), life: 4000 })
            } else {
              alert('Commande échouée: ' + String(msg))
            }
            return
          }

          // success: controller returns { message: ..., id: <id> }
          if (json && json.id) {
            if (this.$toast && this.$toast.add) {
              this.$toast.add({ severity: "success", summary: "Commande passée !", life: 3000 })
            } else {
              alert('Commande créée (id: ' + json.id + ')')
            }
            this.dialog = false
            // optionally refresh lists or UI
            // this.fetchArticles() // not necessary here, but left as option
          } else {
            // fallback success
            if (this.$toast && this.$toast.add) {
              this.$toast.add({ severity: "success", summary: json.message || "Commande OK", life: 3000 })
            }
            this.dialog = false
          }
        } catch (err) {
          console.error(err)
          if (this.$toast && this.$toast.add) {
            this.$toast.add({ severity: "error", summary: "Erreur réseau", detail: String(err), life: 4000 })
          } else {
            alert('Erreur réseau: ' + String(err))
          }
        }
      })();
    },
  },
};
</script>

<style scoped>
.article-item {
  background: #fff;
  border: 1px solid #eee;
  margin: 6px 4px;
  border-radius: 6px;
  padding: 10px;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.btn-black {
  color: black !important;
}

@media (max-width: 700px) {
  .article-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
