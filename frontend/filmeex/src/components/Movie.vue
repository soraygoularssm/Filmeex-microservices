<template>
  <div class="container-fluid">
    <div class="row equal">
      <div
        v-for="movie in moviesList"
        v-bind:key="movie.imdbid"
        class="col-sm-6 col-md-3 col-lg-2 text-center"
      >
          <router-link :to="'/media/' + movie.imdbId">
            <img
              class="card-img-top poster"
              v-bind:src="
                'http://localhost:8000/files/photos/full/' + movie.poster
              "
              v-bind:alt="movie.name"
            />
            <div class="card-body">
              <h5 class="card-title">{{ movie.name }}</h5>
            </div>
          </router-link>
          <div class="rating">
            <i class="fa fa-star"></i>
                <span>{{movie.rating.rate}}</span>
          </div>
      </div>
    </div>
  </div>
</template>



<script>
// import 'video.js/dist/video-js.min.css';

// import 'video.js/dist/video.min.js';

export default {
  name: "Movie",
  props: {
    moviesList: Array,
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
}

p {
  text-align: center;
}

.poster {
  object-fit: cover;
}
</style>