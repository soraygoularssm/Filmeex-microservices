<template>
  <div>
    <input
      class="w-100 my-3 text-center"
      v-model="genreSet"
      v-on:change="get_media"
      placeholder="genre"
    />
    <br />
    <div id="app">
      <Movie v-bind:moviesList="mylist" />
    </div>
  </div>
</template>

<script>
// import 'video.js/dist/video-js.min.css';

// import 'video.js/dist/video.min.js';
import Movie from "./Movie.vue";
import axios from "axios";

export default {
  name: "Home",
  components: {
    Movie,
  },

  data: function () {
    return {
      mylist: null,
      genreSet: "",
    };
  },

  methods: {
    getMedia: function () {
      axios
        .post("http://localhost:8000/graphql", {
          query:
            "{movies(limit:500){imdbId , name , poster , genres , rating{rate , ratesAmount}}}",
        })
        .then((response) => (this.mylist = response.data.data.movies));
    },
  },

  mounted() {
    this.getMedia();
  },
};
</script>

<style scoped>
</style>