<template>
  <v-app>
    <Navigation />

    <v-main>
      <div class="ml-10 mr-10 mt-10 mb-10">
        <router-view />
      </div>
    </v-main>
    <!-- <MusicPlayerWraper /> -->

    <!-- <BottomNavigation v-if="$vuetify.breakpoint.mdAndDown" /> -->
  </v-app>
</template>

<script>
import Navigation from "./components/Navigation";

export default {
  name: "App",

  components: {
    Navigation,
  },

  data: () => ({
    //
  }),
};
</script>
