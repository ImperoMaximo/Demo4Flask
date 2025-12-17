<template>
  <v-main>
    <v-container class="d-flex flex-column align-center" style="margin-top:2px;">
      <v-card elevation="3" class="pa-4" max-width="900" color="blue-grey lighten-5">
        <v-card-title class="text-h5 text-center">Commandes</v-card-title>
        <v-card-text class="mb-4 text-center">Liste de toutes les commandes (nom article, description, quantité, date)</v-card-text>
        <v-divider></v-divider>
        <v-card-text>
          <v-virtual-scroll
            v-model="commandes"
            :items="commandes"
            height="60vh"
            item-height="84"
            class="v-virtual-scroll-padding-bottom"
          >
            <template v-slot:default="{ item }">
              <div class="commande-item d-flex align-center justify-space-between">
                <!-- Texte -->
                <div style="display: flex; flex-direction: column; gap: 4px; max-width: 65%;">
                  <span class="text-h6 item-nom">{{ item.nom }}</span>
                  <span class="text-body-2 item-desc d-block">{{ item.description }}</span>
                  <div class="meta small">Quantité: <strong>{{ item.nombrePiece }}</strong> • Date: {{ item.date_emission }}</div>
                </div>
                <!-- Boutons -->
                <div class="d-flex gap-2">
                  <v-btn color="error" variant="outlined" class="ma-1" @click="confirmDelete(item.id)">Supprimer</v-btn>
                  <v-btn color="primary" variant="outlined" class="ma-1" @click="modifyCommande(item.id, item.nombrePiece)">Modifier</v-btn>
                </div>
              </div>
            </template>
          </v-virtual-scroll>
        </v-card-text>
      </v-card>
    </v-container>
  </v-main>
</template>

<script>
export default {
  data() {
    return {
      commandes: [],
      list_api: this.$back_api_base_url + '/all_commande',
      single_api: this.$back_api_base_url + '/commande/',
      materiel_api: this.$back_api_base_url + '/materiel/',
    }
  },
  created() {
    this.fetchCommandes()
  },
  methods: {
    async fetchCommandes() {
      try {
        const res = await fetch(this.list_api)
        if (!res.ok) {
          console.error('Failed to fetch commandes', res.status, res.statusText)
          return
        }
        const list = await res.json()

        // For each commande, fetch detail (date, materiel_id) then materiel description
        const detailed = await Promise.all(list.map(async (c) => {
          try {
            const r = await fetch(this.single_api + c.id)
            if (!r.ok) return { id: c.id, nom: c['nom materiel'] || c.nom, nombrePiece: c['nombre piece'] || c.nombrePiece, date_emission: '', description: '' }
            const data = await r.json()
            let description = ''
            try {
              const m = await fetch(this.materiel_api + data.materiel_id)
              if (m.ok) {
                const md = await m.json()
                description = md.description || ''
              }
            } catch (e) {
              // ignore
            }
            return {
              id: data.id,
              nom: data.materiel_nom || c['nom materiel'] || '',
              description,
              nombrePiece: data.nombrePiece,
              date_emission: data.date_emission || '',
              commentaire: data.commentaire_emission || c.commentaire || ''
            }
          } catch (e) {
            return { id: c.id, nom: c['nom materiel'] || '', description: '', nombrePiece: c['nombre piece'] || 0, date_emission: '', commentaire: '' }
          }
        }))

        this.commandes = detailed
      } catch (e) {
        console.error('Error fetching commandes', e)
      }
    },

    async confirmDelete(id) {
      if (!confirm('Supprimer cette commande ?')) return
      try {
        const res = await fetch(this.single_api + id, { method: 'DELETE' })
        if (!res.ok) {
          const txt = await res.text().catch(() => '')
          console.error('Delete failed', res.status, txt)
          alert('Suppression échouée')
          return
        }
        // optimistic UI: remove locally without refetch
        this.commandes = this.commandes.filter(c => c.id !== id)
        if (this.$toast && this.$toast.add) {
          this.$toast.add({ severity: 'success', summary: 'Supprimé', detail: 'Commande supprimée', life: 3000 })
        }
      } catch (e) {
        console.error('Delete error', e)
      }
    },

    async modifyCommande(id, currentQuantity) {
      const answer = prompt('Nouvelle quantité', String(currentQuantity || ''))
      if (answer === null) return
      const q = parseInt(answer)
      if (Number.isNaN(q)) { alert('Quantité invalide'); return }
      try {
        // If user sets quantity to 0, interpret as delete
        if (q === 0) {
          if (!confirm('La quantité est 0 — supprimer la commande ?')) return
          const delRes = await fetch(this.single_api + id, { method: 'DELETE' })
          if (!delRes.ok) {
            const txt = await delRes.text().catch(() => '')
            console.error('Delete (via modify) failed', delRes.status, txt)
            alert('Suppression échouée')
            return
          }
          // remove locally
          this.commandes = this.commandes.filter(c => c.id !== id)
          if (this.$toast && this.$toast.add) this.$toast.add({ severity: 'success', summary: 'Supprimé', detail: 'Commande supprimée', life: 3000 })
          return
        }

        // Normal update
        const res = await fetch(this.single_api + id, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ nombre_piece: q })
        })
        if (!res.ok) {
          const txt = await res.text().catch(() => '')
          console.error('Update failed', res.status, txt)
          alert('Mise à jour échouée')
          return
        }

        // Optimistically update local data without full refetch
        this.commandes = this.commandes.map(c => c.id === id ? { ...c, nombrePiece: q } : c)
        if (this.$toast && this.$toast.add) this.$toast.add({ severity: 'success', summary: 'Modifié', detail: 'Quantité mise à jour', life: 2500 })
      } catch (e) {
        console.error('Update error', e)
      }
    }
  }
}
</script>

<style scoped>
.commande-item {
  background: #fff;
  border: 1px solid #eee;
  margin: 6px 4px;
  border-radius: 6px;
  padding: 12px;
  display: flex;
  align-items: center;
}
.item-nom,
.item-desc {
  color: #000 !important; /* noir, ou #333 pour gris foncé */
}


.v-main {
  padding-top: 10px !important;    
}

.meta.small { font-size: 0.9rem; color: #555; margin-top: 6px }

@media (max-width:700px) {
  .commande-item { flex-direction: column; align-items: flex-start }
}
</style>