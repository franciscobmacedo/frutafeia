<template>
  <v-dialog v-model="show" max-width="500px" class="text-wrap">
    <v-card>
      <v-card-text>
        <div class="text-body-1 text-center pt-12">
          Tem a certeza que pretende apagar esta disponibilidade?
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="show = false"
          >Cancelar
        </v-btn>
        <v-btn color="error darken-1" text @click="deleteItem()">Sim</v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    value: Boolean,
    item: Object,
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  methods: {
    deleteItem() {
      this.$store.dispatch("deleteAvailability", this.item);
      this.show = false;
    },
  },
};
</script>

<style>
</style>