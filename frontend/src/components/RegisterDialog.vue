<template>
  <v-dialog v-model="show" width="800">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="show = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title
          >{{ edit ? "Editar" : "Adicionar" }} Disponibilidade</v-toolbar-title
        >
        <v-spacer></v-spacer>
      </v-toolbar>

      <v-card-text>
        <v-container>
          <v-form v-model="valid" lazy-validation ref="form">
            <v-container>
              <v-row>
                <v-col cols="12" sm="4">
                  <v-menu
                    ref="dateMenu"
                    v-model="dateMenu"
                    :close-on-content-click="false"
                    :return-value.sync="item.data"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        v-model="item.data"
                        label="Data em que esteve disponível"
                        prepend-icon="mdi-calendar"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                        :rules="[
                          (v) => !!v || 'É necessário selecionar uma data',
                        ]"
                      >
                      </v-text-field>
                    </template>
                    <v-date-picker v-model="item.data" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="dateMenu = false">
                        Cancel
                      </v-btn>
                      <v-btn
                        text
                        color="primary"
                        @click="$refs.dateMenu.save(item.data)"
                      >
                        OK
                      </v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-col>
                <v-col cols="12" md="4">
                  <v-autocomplete
                    v-model="item.produtor"
                    :items="providers"
                    :disabled="providers.length <= 0"
                    item-text="nome"
                    :rules="[
                      (v) => !!v || 'É necessário selecionar um produtor',
                    ]"
                    label="Produtor"
                    no-data-text="Seleccione um produtor"
                    required
                    return-object
                  >
                  </v-autocomplete>
                </v-col>
                <v-col cols="12" md="4">
                  <v-autocomplete
                    v-model="item.produto"
                    :items="emptyProducer ? [] : item.produtor.produtos"
                    :disabled="
                      emptyProducer ? true : item.produtor.produtos.length <= 0
                    "
                    item-text="nome"
                    :rules="[
                      (v) => !!v || 'É necessário selecionar um produto',
                    ]"
                    label="Produto"
                    no-data-text="Seleccione um produto"
                    required
                    return-object
                  >
                  </v-autocomplete>
                </v-col>
                <v-col cols="7">
                  <v-text-field
                    v-model="item.quantidade"
                    type="number"
                    :rules="[
                      (v) =>
                        v > 0 || 'A quantidade não pode ser 0 nem negativa!',
                    ]"
                    label="Quantidade"
                  ></v-text-field>
                </v-col>
                <v-col cols="2">
                  <v-autocomplete
                    class="mt-2"
                    v-model="item.medida_dict"
                    :items="units"
                    item-text="nome"
                    :rules="[
                      (v) => !!v || 'É necessário selecionar uma unidade',
                    ]"
                    label="Medida"
                    return-object
                    required
                  ></v-autocomplete>
                </v-col>
                <v-col cols="2" offset="1">
                  <v-text-field
                    v-model="item.preco"
                    class="mt-2"
                    type="number"
                    :rules="[
                      (v) => v > 0 || 'O preço não pode ser 0 nem negativo!',
                    ]"
                    label="Preço"
                    :suffix="priceSuffix"
                  >
                  </v-text-field>
                </v-col>

                <v-row>
                  <v-spacer></v-spacer>
                  <v-btn color="error" class="mr-4" @click="close()">
                    Cancelar
                  </v-btn>
                  <v-btn
                    :disabled="!valid"
                    color="success"
                    class="mr-4"
                    @click="validate"
                  >
                    {{ edit ? "Editar" : "Adicionar" }}
                  </v-btn>
                </v-row>
              </v-row>
            </v-container>
          </v-form>
        </v-container>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    value: Boolean,
    item: Object,
    edit: {
      typeof: Boolean,
      default: false,
    },
  },

  data() {
    return {
      dateMenu: false,
      valid: false,
    };
  },
  computed: {
    ...mapState(["providers", "products", "units"]),
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
    isEmpty() {
      return Object.keys(this.item).length === 0;
    },
    emptyProducer() {
      return this.item.produtor === undefined;
    },
    priceSuffix() {
      if (this.item.medida == null) {
        return "€";
      } else {
        return `€/${this.item.medida_dict.nome}`;
      }
    },
  },
  methods: {
    async validate() {
      const result = this.$refs.form.validate();
      if (result) {
        console.log("valid", this.item);
        this.$store.dispatch(
          this.edit ? "editAvailability" : "addAvailability",
          this.item
        );
        this.close();
      }
    },
    close() {
      this.show = false;
    },
  },
};
</script>

<style>
</style>