
<template>
  <v-card
    class="mx-3 mb-10 elevation-3 pb-5 pl-1 pr-2"
    style="max-width: 600px; overflow-y: auto"
    min-height="200px"
  >
    <v-row justify="space-between">
      <v-col cols="8" class="text-center">
        <div class="text-h6">
          <v-icon>mdi-account</v-icon>
          {{ item.produtor.nome }}
        </div>
      </v-col>
      <v-col>
        <v-btn text color="teal accent-4" @click="reveal = true">
          <v-icon left dark> mdi-account-box </v-icon>
          Detalhes
        </v-btn>
      </v-col>
    </v-row>
    <v-divider></v-divider>
    <div class="text-center mt-2 font-weight-light">Pontuação</div>
    <v-row
      align="center"
      justify="center"
      class=""
      :class="index > 0 ? 'mt-5' : 'mt-1'"
      v-for="(product, index) of item.produtos"
      :key="index"
    >
      <div class="body">
        {{ product.produto }}
      </div>

      <v-rating
        :value="roundHalf(product.pontuacao)"
        :length="length"
        readonly
        color="yellow darken-3"
        background-color="grey darken-1"
        half-increments
        :empty-icon="emptyIcon"
        size="15"
        :full-icon="fullIcon"
        :half-icon="halfIcon"
      >
      </v-rating>

      <v-sheet
        class="
          rounded-circle
          yellow
          darken-2
          text-center text-align
          pt-2
          text-caption
        "
        max-width="35"
        elevation="5"
        height="35"
        width="100%"
      >
        {{ roundHalf(product.pontuacao) }}
      </v-sheet>
    </v-row>
    <v-expand-transition>
      <v-card
        v-if="reveal"
        class="transition-fast-in-fast-out v-card--reveal"
        style="height: 100%"
      >
        <v-card-text class="pb-0">
          <v-list one-line dense>
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="indigo"> mdi-phone </v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title class="text-wrap"
                  >{{ item.produtor.telefone }}
                </v-list-item-title>
                <v-list-item-subtitle>Telefone</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-icon>
                <v-icon color="indigo"> mdi-map-marker </v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title class="text-wrap"
                  >{{ item.produtor.concelho }}
                </v-list-item-title>
                <v-list-item-subtitle>Concelho</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-divider inset></v-divider>

            <v-list-item>
              <v-list-item-icon>
                <v-icon color="indigo"> mdi-email </v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title class="text-wrap"
                  >{{ item.produtor.email }}
                </v-list-item-title>
                <v-list-item-subtitle>Email</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-icon>
                <v-icon color="indigo"> mdi-map-marker </v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title class="text-wrap"
                  >{{ item.produtor.morada }}
                </v-list-item-title>
                <v-list-item-subtitle>Morada</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions class="pt-0 pb-2">
          <v-btn text color="teal accent-4" @click="reveal = false">
            Fechar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-expand-transition>
  </v-card>
</template>

<script>
export default {
  props: {
    item: Object,
  },
  data: () => ({
    reveal: false,
    length: 10,
    emptyIcon: "mdi-star-outline",
    fullIcon: "mdi-star",
    halfIcon: "mdi-star-half",
  }),
  methods: {
    roundHalf(num) {
      return Math.round(num * 2) / 2;
    },
  },
};
</script>

<style>
.v-card--reveal {
  bottom: 0;
  left: 0;
  opacity: 1 !important;
  position: absolute;
  width: 100%;
}
</style>