<template>
  <div>
    <RegisterDialog
      v-if="showRegisterDialog"
      v-model="showRegisterDialog"
      :item="editedItem"
      :edit="edit"
    />
    <DeleteDialog
      v-if="showDeleteDialog"
      v-model="showDeleteDialog"
      :item="editedItem"
    />
    <v-row justify="space-between" align="center" class="mb-2 text-right">
      <v-col>
        <div class="text-h4 text-left">Disponibilidades</div>
      </v-col>
      <v-col>
        <v-btn color="primary" dark @click="addItem()">
          Adicionar Disponibilidade
        </v-btn>
      </v-col>
      <v-col>
        <v-btn class="mt-2" color="primary" dark @click="addItem()">
          Ver disponibilidades antigas
        </v-btn>
      </v-col>
    </v-row>

    <v-data-table
      :loading="loading"
      :headers="headers"
      :items="availability"
      :search="searchAvailability"
      :items-per-page="5"
      :footer-props="{
        'items-per-page-text': 'Linhas por página',
        locale: 'pt-PT',
      }"
      loading-text="A carregar dados..."
      no-data-text="Sem novas disponibilidades"
      class="elevation-1"
    >
      <template v-slot:item.actions="{ item }">
        <v-tooltip left>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              small
              class="mr-2"
              v-bind="attrs"
              v-on="on"
              @click="editItem(item)"
            >
              mdi-pencil
            </v-icon>
          </template>
          <span>Editar</span>
        </v-tooltip>
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              small
              class="mr-2"
              v-bind="attrs"
              v-on="on"
              @click="deleteItem(item)"
            >
              mdi-delete
            </v-icon>
          </template>
          <span>Apagar</span>
        </v-tooltip>
      </template>
    </v-data-table>

    <v-snackbar v-model="snackbar" :timeout="5000">
      {{ snackbarText }}

      <template v-slot:action="{ attrs }">
        <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
          Fechar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from "vuex";
import RegisterDialog from "@/components/RegisterDialog";
import DeleteDialog from "@/components/DeleteDialog";
import actions from "@/enum";
export default {
  components: { RegisterDialog, DeleteDialog },
  data() {
    return {
      edit: false,
      showRegisterDialog: false,
      showDeleteDialog: false,
      loading: false,
      headers: [
        { text: "Data", value: "data" },
        { text: "Produto", value: "produto.nome" },
        { text: "Produtor", value: "produtor.nome" },
        { text: "Quantidade", value: "quantidade" },
        { text: "Medida", value: "medida_dict.nome" },
        { text: "Preço", value: "preco" },
        { text: "Ações", value: "actions", sortable: false },
      ],
      searchAvailability: "",
      editedItem: {},
      snackbar: false,
    };
  },
  computed: {
    ...mapState(["availability", "action"]),
    snackbarText() {
      switch (this.action) {
        case actions.ADD:
          return "Disponibilidade adicionada com sucesso";
        case actions.EDIT:
          return "Disponibilidade editada com sucesso";
        case actions.DELETE:
          return "Disponibilidade removida com sucesso";
        default:
          return "";
      }
    },
  },
  watch: {
    availability() {
      this.snackbar = true;
    },
  },
  methods: {
    editItem(item) {
      this.snackbar = false;
      this.editedIndex = this.availability.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.edit = true;
      this.showRegisterDialog = true;
    },
    addItem() {
      this.snackbar = false;
      this.editedItem = {};
      this.edit = false;
      this.showRegisterDialog = true;
    },
    deleteItem(item) {
      this.snackbar = false;
      this.editedIndex = this.availability.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.showDeleteDialog = true;
    },
    deleteAll() {
      this.$store.dispatch("deleteAllAvalilability");
    },
  },
};
</script>

<style>
</style>