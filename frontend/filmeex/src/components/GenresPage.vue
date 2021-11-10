<template>
  <div class="container-fluid">
    <div class="row">
      <div v-for="(genre, index) in genresList" v-bind:key="index">
        <h1 class="text-center py-4 my-4 w-100 bg-warning" dir="rtl">
          {{ genre.name }}
        </h1>

        <ul class="list-inline w-100">
          <li
            v-for="movie in genre.media"
            v-bind:key="movie.imdbid"
            class="col-sm-6 col-md-4 col-lg-3 list-inline-item mx-0"
          >
            <router-link :to="'/media/' + movie.imdbId">
              <img
                v-bind:src="
                  'http://localhost:8000/files/photos/full/' + movie.poster
                "
                alt=""
              />
            </router-link>
            <br />
            <p>
              {{ movie.name }}
            </p>
            {{ movie.rating.rate }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Genres",

  data: function () {
    return {
      genresList: false,
    };
  },

  mounted() {
    axios
      .post("http://localhost:8000/graphql", {
        query:
          "{allGenres{name , media{imdbId, name, poster, rating{rate} } }}",
      })
      .then((response) => (this.genresList = response.data.data.allGenres));
  },
};
</script>

<style scoped>
</style>