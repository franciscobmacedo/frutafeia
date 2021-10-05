<template>
  <div>
    <v-row v-if="!success" justify="center" align="center" width="100%">
      <v-sheet
        style="margin-top: 30%"
        height="100%"
        class="text-center pa-10"
        elevation="8"
      >
        <div class="text-h4 mb-3">
          😔 Ainda não é possível realizar a cesta 😔
        </div>
        <v-alert type="error">
          {{ message }}
        </v-alert>
      </v-sheet>
    </v-row>
    <v-row v-else justify="center" align="center" width="100%">
      <div class="text-h4 mt-10 mb-5">Sugestão de cestas</div>
      <v-card
        class="pa-2 mt-5"
        height="100%"
        width="90%"
        v-for="(basket, index) of baskets"
        :key="index"
      >
        <v-card-title align-bottom>
          <v-icon large class="mr-2">mdi-basket</v-icon> Sugestão de cesta
          {{ index + 1 }}
        </v-card-title>
        <v-divider></v-divider>
        <v-row>
          <v-col cols="6">
            <div class="text-h6 pl-2 mt-1">Cesta Pequena</div>
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-left">Produto</th>
                    <th class="text-left">Quantidade</th>
                    <th class="text-left">Medida</th>
                    <th class="text-left">Preço</th>
                    <th class="text-left">Produtor</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(item, index1) in basketContent(basket.conteudo)"
                    :key="index1"
                  >
                    <td>{{ item.produto }}</td>
                    <td>{{ item.quantidade_pequena }}</td>
                    <td>{{ item.medida_name }}</td>
                    <td>{{ roundHalf(item.preco_unitario) }}</td>
                    <td>{{ item.produtor }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
            <v-row justify="center" align="end" class="mt-10 pt-5 mb-0">
              <v-col cols="2" class="text-center">
                <v-btn large fab color="red lighten-2" class="no-cursor">
                  <div class="white--text text-h6">
                    {{ roundHalf(basket.preco_pequena) }}
                  </div>
                  <v-icon color="yellow">mdi-currency-eur</v-icon>
                </v-btn>
                <div class="text-caption">Preço</div>
              </v-col>
              <v-col cols="2" class="text-center">
                <v-btn large fab color="green lighten-2" class="no-cursor">
                  <div class="white--text text-h6">
                    {{ roundHalf(basket.peso_pequena) }}
                  </div>
                  <v-icon color="yellow">mdi-weight-kilogram</v-icon>
                </v-btn>

                <div class="text-caption">Peso</div>
              </v-col>
            </v-row>
          </v-col>

          <v-col cols="6">
            <div class="text-h6 pl-2">Cesta Grande</div>
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-left">Produto</th>
                    <th class="text-left">Quantidade</th>
                    <th class="text-left">Medida</th>
                    <th class="text-left">Preço</th>
                    <th class="text-left">Produtor</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index2) in basket.conteudo" :key="index2">
                    <td>{{ item.produto }}</td>
                    <td>{{ item.quantidade_grande }}</td>
                    <td>{{ item.medida_name }}</td>
                    <td>{{ roundHalf(item.preco_unitario) }}</td>
                    <td>{{ item.produtor }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
            <v-row justify="center" align="center" class="mt-2">
              <v-col cols="2" class="text-center">
                <v-btn large fab color="red lighten-2" class="no-cursor">
                  <div class="white--text text-h6">
                    {{ roundHalf(basket.preco_grande) }}
                  </div>
                  <v-icon color="yellow">mdi-currency-eur</v-icon>
                </v-btn>
                <div class="text-caption">Preço</div>
              </v-col>
              <v-col cols="2" class="text-center">
                <v-btn large fab color="green lighten-2" class="no-cursor">
                  <div class="white--text text-h6">
                    {{ basket.peso_grande }}
                  </div>
                  <v-icon color="yellow">mdi-weight-kilogram</v-icon>
                </v-btn>

                <div class="text-caption">Peso</div>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-row>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      success: true,
    };
  },
  computed: {
    ...mapState(["baskets"]),
    dateFormated() {
      return this.date === null ? "" : this.localDate(this.date);
    },
  },
  methods: {
    basketContent(content) {
      return content.filter((item) => item.produto_extra);
    },
    localDate(date) {
      const d = new Date(date);
      var options = { year: "numeric", month: "long", day: "numeric" };

      return d.toLocaleDateString("pt-PT", options);
    },
    roundHalf(num) {
      return Math.round(num * 2) / 2;
    },
  },
};
</script>