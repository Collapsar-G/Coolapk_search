<template>
  <v-app>
    <v-app-bar
      app
      color="green darken-1"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.jsdelivr.net/gh/Collapsar-G/image/img/20201214234732.png"
          transition="scale-transition"
          width="80"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.jsdelivr.net/gh/Collapsar-G/image/img/20201215104244.png"
          width="300"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/Collapsar-G"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <Search/>
    </v-main>
  </v-app>
</template>

<script>
import Search from './components/Search';

export default {
  name: 'App',

  components: {
    Search: Search,
  },

  data: () => ({
    //
  }),
};
</script>
