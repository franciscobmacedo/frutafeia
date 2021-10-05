<template>
  <div>
    <div class="text-h3 text-center mb-5">Semana de 11 a 15 de Outubro</div>
    <v-row>
      <v-col cols="8">
        <Availability />
        <div class="mt-10">
          <v-row align="center" justify="center">
            <v-progress-circular :value="30" :size="300" :width="10">
              <div class="d-flex flex-column text-center">
                <v-icon :size="130">mdi-basket</v-icon>
                <div>Faltam 5 verdes para uma cesta completa</div>
              </div>
            </v-progress-circular>
          </v-row>
        </div>
      </v-col>
      <v-col cols="4">
        <Ranking />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Availability from "./Availability.vue";
import Ranking from "./Ranking.vue";
export default {
  components: {
    Availability,
    Ranking,
  },
};
</script>

<style>
</style>