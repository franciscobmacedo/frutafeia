<template>
  <v-navigation-drawer
    v-if="!$vuetify.breakpoint.smAndDown"
    app
    permanent
    expand-on-hover
    clipped
    class="mt-100 pr-100"
    :width="400"
  >
    <v-divider class="mt-2"></v-divider>
    <v-list>
      <v-list-group
        v-for="item in items"
        :key="item.title"
        v-model="item.active"
        :prepend-icon="item.icon"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="item.title"></v-list-item-title>
          </v-list-item-content>
        </template>
        <v-list-item
          v-for="child in item.items"
          :key="child.title"
          link
          class="closer"
          :to="child.link"
        >
          <v-list-item-content>
            <v-list-item-title
              v-text="child.title"
              class="text-wrap"
            ></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "NavigationDrawer",
  data() {
    return {
      scrollOptions: {
        height: "80%",
        alwaysVisible: true,
      },
      items: [
        {
          icon: "mdi-podium",
          active: true,
          items: [{ title: "Mostar Ranking", link: { name: "ranking" } }],
          title: "Ranking",
        },
        {
          icon: "mdi-file-edit",
          items: [
            {
              title: "Registar Disponibilidades",
              link: { name: "registerAvailability" },
            },
            {
              title: "Mostrar Disponibilidades Antigas",
              action: "showOldAvailability",
            },
            {
              title: "Apagar Disponibilidades",
              action: "resetAvailabilityConfirm",
            },
          ],
          title: "Disponibilidades",
          link: { name: "registerAvailability" },
        },

        {
          icon: "mdi-basket",
          items: [
            { title: "Montar cesta da próxima semana", action: "showBaskets" },
            { title: "Mostrar cestas antigas", action: "showOldBaskets" },
          ],
          title: "Cestas",
        },

        {
          icon: "mdi-file-table-box-multiple",
          items: [
            { title: "Validar mapas de campo", action: "showMapConfirmation" },
          ],
          title: "Mapas de Campo",
        },
        {
          icon: "mdi-account-group",
          items: [{ title: "Produtores e Produtos", action: "showProviders" }],
          title: "Gerir Dados",
        },
      ],
    };
  },
};
</script>
