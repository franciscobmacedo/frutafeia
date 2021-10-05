<template>
  <v-container>
    <div v-if="!loading">
      <v-form v-model="valid" lazy-validation ref="form">
        <v-container>
          <v-row>
            <v-col cols="12" sm="4">
              <v-menu
                ref="dateMenu"
                v-model="dateMenu"
                :close-on-content-click="false"
                :return-value.sync="date"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="date"
                    label="Data De contacto"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    :rules="[(v) => !!v || 'É necessário selecionar uma data']"
                  >
                  </v-text-field>
                </template>
                <v-date-picker v-model="date" no-title scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="dateMenu = false">
                    Cancel
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.dateMenu.save(date)"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12" md="4">
              <v-autocomplete
                v-model="selectedProvider"
                :items="providers"
                item-text="nome"
                :rules="[(v) => !!v || 'É necessário selecionar um produtor']"
                label="Produtor"
                return-object
                required
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" sm="4">
              <v-autocomplete
                v-model="selectedProduct"
                :items="products"
                item-text="nome"
                return-object
                :disabled="products.length <= 0"
                :rules="[(v) => !!v || 'É necessário selecionar produto']"
                label="Produto"
                no-data-text="Seleccione um produtor com produtos!"
                required
              >
              </v-autocomplete>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="7">
              <v-slider
                v-model="quantity"
                label="Quantidade"
                class="align-center"
              >
                <template v-slot:append>
                  <v-text-field
                    v-model="quantity"
                    type="number"
                    :rules="[
                      (v) =>
                        v > 0 || 'A quantidade não pode ser 0 nem negativa!',
                    ]"
                    label="Quantidade"
                  ></v-text-field>
                </template>
              </v-slider>
            </v-col>
            <v-col cols="2">
              <v-autocomplete
                class="mt-2"
                v-model="selectedUnit"
                :items="units"
                :rules="[(v) => !!v || 'É necessário selecionar uma unidade']"
                label="Medida"
                item-text="nome"
                return-object
                required
              ></v-autocomplete>
            </v-col>
            <v-col cols="2" offset="1">
              <v-text-field
                v-model="price"
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
          </v-row>
          <v-row justify="center" align="center">
            <v-checkbox large v-model="urgent" label="Urgente?"></v-checkbox>
          </v-row>
          <v-row>
            <v-btn
              :disabled="!valid"
              color="success"
              class="mr-4"
              @click="validate"
            >
              Registar
            </v-btn>
          </v-row>
        </v-container>
      </v-form>
    </div>
    <div v-else>
      <v-row justify="center" align="center">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-row>
    </div>
  </v-container>
</template>

<script>
export default {
  name: "HelloWorld",

  data: () => ({
    loading: false,
    valid: false,
    units: [],
    selectedUnit: null,
    // products: [],
    providers: [],
    providersNames: [],
    selectedProduct: null,
    selectedProvider: null,
    dateMenu: false,
    date: null,
    quantity: 0,
    price: 0,
    urgent: false,
  }),
  async created() {
    this.loading = true;
    this.loading = false;
    // this.setProductsOptions(this.products)
    // this.setProvidersOptions(this.providers)
  },
  computed: {
    priceSuffix() {
      if (this.selectedUnit == null) {
        return "€";
      } else {
        return `€/${this.selectedUnit.nome}`;
      }
    },
    products() {
      return this.selectedProvider === null
        ? []
        : this.selectedProvider.produtos;
    },
  },
  watch: {
    products() {
      this.selectedProduct = null;
    },
  },
  methods: {
    async setProvidersOptions(providers) {
      this.providers = providers;
    },
    setUnitsOptions(options) {
      this.units = options;
      this.selectedUnit = options[0];
    },

    async validate() {
      const result = this.$refs.form.validate();
      if (result) {
        const data = {
          produtor: this.selectedProvider.nome,
          data: this.date,
          quantidade: this.quantity,
          produto: this.selectedProduct.nome,
          preco: this.price,
          medida: this.selectedUnit,
          urgente: this.urgent,
        };
        console.log(data);
      }
    },
  },
};
</script>
