<template>
  <div>
    <div class="text-center text-h4"><v-icon>mdi-phone</v-icon> Ranking</div>
    <div class="fade">
      <v-card
        class="overflow-y-auto mt-5"
        max-height="80vh"
        elevation="0"
        rounded="false"
      >
        <RankingCard
          v-for="(item, index) of ranking"
          :key="index"
          :item="item"
        />
      </v-card>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import RankingCard from "@/components/RankingCard";
export default {
  components: {
    RankingCard,
  },

  computed: {
    ...mapState(["ranking"]),
  },
};
</script>

<style>
.fade {
  position: relative;
}

.fade:after {
  content: "";
  position: absolute;
  z-index: 1;
  bottom: 0;
  left: 0;
  pointer-events: none;
  background-image: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0),
    rgba(255, 255, 255, 1) 90%
  );
  width: 100%;
  height: 6em;
}
</style>