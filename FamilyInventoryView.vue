<script setup>
import NavBar from "@/components/NavBar.vue";
</script>
<!-- page of inventory family -->
<!-- Home page of the inventory. 
The user can access the inventory of each family of material. 
The user can also download the inventory in xlsx format.  
The user can also choose his DT if he is not in the database yet but part of defaut user -->
<template>
  <NavBar>
    <v-card class="main-card" variant="outlined">
      <v-card-item class="bg-orange-darken-4">
        <v-card-title>
          {{ $CONFIG_FRONT_TXT.mon_inventaire.title }}
        </v-card-title>
        <!-- donwload all inventory of a user in xlsx format -->
        <template v-slot:append>
          <v-btn class="ma-1" color="white" size="small" @click="download_inventaire">
            <v-icon> mdi-download </v-icon>
            <v-tooltip activator="parent" location="end">{{
              $CONFIG_FRONT_TXT.commun.download_xlsx
            }}</v-tooltip>
          </v-btn>
        </template>
      </v-card-item>

      <v-card-text class="pt-5">
        {{ $CONFIG_FRONT_TXT.mon_inventaire.description }}
      </v-card-text>

      <!-- <v-divider></v-divider> -->

      <!-- show all family existing in the db  -->
      <v-layout v-if="family_list.length > 0">
        <v-virtual-scroll
          v-model="family_list"
          :items="family_list"
          height="100vh"
          item-height="5"
          class="v-virtual-scroll-padding-bottom"
        >
          <template v-slot:default="{ item }">
            <v-list-item
              width="99%"
              style="
                background: #fefefe;
                border: solid;
                border-width: 1px;
                margin: 3px;
                border-radius: 1px;
              "
              class="inventaire_stock"
            >
              <template v-slot:prepend>
                <div class="div_materiel_names">
                  <v-avatar :color="'#90CAF9'" class="text-white" size="40">
                    <!-- {{ item }} -->
                  </v-avatar>
                  <v-list-item-title>{{
                    capitalizeFirstLetter(item.name)
                  }}</v-list-item-title>
                </div>
              </template>
              <template v-slot:append>
                <div class="inventaire_stock">
                  <router-link :to="item.route" style="display: block">
                    <v-btn
                      variant="outlined"
                      color="primary"
                      elevation="4"
                      class="btn_margin"
                    >
                      {{
                        $CONFIG_FRONT_TXT.mon_inventaire.access_matrial_class_btn_label
                      }}
                      <v-icon color="orange-darken-4" end> mdi-open-in-new </v-icon>
                    </v-btn>
                  </router-link>
                </div>
              </template>
            </v-list-item>
          </template>
        </v-virtual-scroll>
      </v-layout>
    </v-card>
  </NavBar>

  <!-- for your first connection, chose your dt if you where not created by another user with higher right -->
  <v-dialog
    v-if="list_dt.length > 0"
    v-model="dialog_sign_up"
    transition="dialog-bottom-transition"
    width="50%"
    :persistent="true"
  >
    <template v-slot:default="{ isActive }">
      <v-card>
        <v-toolbar color="primary" title="Je choisi mon DT"></v-toolbar>
        <v-card-text>
          <v-list-subheader>
            {{ $CONFIG_FRONT_TXT.mon_inventaire.choose_dt_label_1 }}
          </v-list-subheader>
          <v-list-subheader>
            {{ $CONFIG_FRONT_TXT.mon_inventaire.choose_dt_label_2 }}
          </v-list-subheader>
          <v-list-item title="DT">
            <v-select
              label="Select"
              v-model="dt"
              :items="list_dt"
              :item-props="dtItemProps"
              variant="underlined"
            ></v-select>
          </v-list-item>
        </v-card-text>

        <v-card-actions class="justify-end">
          <v-btn
            color="green"
            variant="elevated"
            @click="confirm_user_dt_change(isActive)"
            >Je valide</v-btn
          >
          <!-- <v-spacer></v-spacer> -->
          <!-- <v-btn color="red" variant="elevated" @click="isActive.value = false">Annuler</v-btn> -->
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import { useIventaireMetaStore } from "@/stores/inventaireMeta";
import { useUserStore } from "@/stores/user";
import { capitalizeFirstLetter } from "@/common_function";
import { utils, writeFile } from "xlsx";
import { usePanierStore } from "@/stores/panier";

export default {
  data() {
    return {
      family_list: [],
      userStore: useUserStore(),
      panierStore: usePanierStore(),
      dialog_sign_up: false,
      list_dt: [],
      user_connexion_type: "",
      dt: "",
      family_description: "",
      family_api: this.$back_api_base_url + "/familles",
      unique_family_api: `${this.$back_api_base_url}/famille`,
      unique_user_api: `${this.$back_api_base_url}/unique_user_controler`,
    };
  },

  created() {
    // this.panierStore.setUtilisateur(this.userStore.user.matricule, this.userStore.user.pseudo);

    this.fetch_family();
    // console.log("adresse : ",`${this.$back_api_base_url}/cart/${this.userStore.user.pseudo}`)
    this.panierStore.chargerPanier(this.$back_api_base_url, this.userStore.user.pseudo);
    // first connection (if user is not in the db yet)
    if (this.userStore.user.connexion_type == "signup") {
      this.user_connexion_type = "signup";
      this.fetch_dts();
      this.dialog_sign_up = true;
    }
  },

  watch: {
    user_connexion_type: {
      handler(new_value, old_value) {
        // user_connexion_type has a defaut value and will change on page load...
        if (old_value != old_value) {
          if (new_value == "signup") {
            this.dialog_sign_up = true;
          }
        }
      },
    },
  },

  methods: {
    dtItemProps(item) {
      // first connection, choose dt
      return {
        title: capitalizeFirstLetter(item.localisation),
        subtitle: `DT ${item.nom.toUpperCase()}`,
        value: item,
      };
    },
    fetch_dts() {
      // get all dt
      fetch(this.$back_api_base_url + "/dt")
        .then((response) => response.json())
        .then((json_response) => {
          this.list_dt = json_response;
          this.dt = this.list_dt[0];
        });
    },

    confirm_user_dt_change(is_dialog_sign_up_active) {
      // console.log("confirm user dt change");
      // console.log(this.dt)
      fetch(`${this.unique_user_api}/${this.userStore.user.pseudo}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          pseudo: this.userStore.user.pseudo,
          new_dt: this.dt,
        }),
      })
        .then((response) => response.json())
        .then((json_response) => {
          this.userStore.user.dt = json_response.dt;
          this.userStore.user.connexion_type = "signin";
          is_dialog_sign_up_active.value = false;
        });
    },

    /**
     * Fetches the family data asynchronously.
     * This function retrieves the family data from the server or API.
     * It is used to populate the family-related information in the view.
     *
     * @returns {Promise<void>} A promise that resolves when the family data is successfully fetched.
     */
    async fetch_family() {
      try {
        const response = await fetch(this.family_api);
        const data = await response.json();

        const IventaireMetaStore = useIventaireMetaStore();
        IventaireMetaStore.classInventaire = data.familles;

        this.family_list = Array.from(data.familles, (famille) => {
          return {
            id: famille.id,
            name: famille.nom,
            route: "/inventaire/" + famille.nom,
            route_commande: "/inventaire_commande/" + famille.nom,
            route_stock_dt: this.$front_base_resource_path + `/stock/${famille.nom}`,
          };
        }).sort((a, b) => a.name.localeCompare(b.name));
      } catch (error) {
        console.error("Error fetching data familles:", error);
      }
    },

    /**
     * Downloads the inventory data as xslx.
     * This function triggers the download of the inventory data in a specified format.
     * It is an asynchronous function that handles the download process.
     *
     * @returns {Promise<void>} A promise that resolves when the download is complete.
     */
    async download_inventaire() {
      // Create a new workbook
      const workbook = utils.book_new();

      // Iterate through each famille_item
      await Promise.all(
        this.family_list.map(async (famille_item) => {
          // Fetch data for each famille_item
          const res = await fetch(
            this.$back_api_base_url +
              "/materiels/" +
              famille_item.name +
              "/" +
              this.userStore.user.pseudo
          );
          const json_res = await res.json();

          console.log(json_res);

          // Convert fetched data to worksheetData
          const worksheetData = json_res.map((item) => [
            item.famille,
            item.nom,
            item.nombrePiece,
          ]);

          // Add header row
          const headers = ["famille", "nom", "nombrePiece"];
          worksheetData.unshift(headers);

          // Create a new worksheet
          const worksheet = utils.aoa_to_sheet(worksheetData);

          // Add the worksheet to the workbook with the sheet name as famille_item.name
          utils.book_append_sheet(workbook, worksheet, famille_item.name);
        })
      );

      // Write the workbook to a file
      const filename = `stocks_par_famille.xlsx`;
      writeFile(workbook, filename);

      console.log(`Excel file "${filename}" has been generated.`);
    },
  },
};
</script>

<style>
.div_materiel_names {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-items: center;
}
</style>

<style scoped>
/* .inventaire_stock {
    display: flex;
    width: 100%;
} */

.btn_margin {
  margin: 10px;
}

@media (max-width: 700px) {
  .inventaire_stock {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}
</style>
