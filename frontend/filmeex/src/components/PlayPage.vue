<template>
  <div class="w-100" v-if="mediaUrls">
    <video class="w-100 h-100" :key="playingMediaIndex" controls>
      <source v-bind:src="mediaUrls[playingMediaIndex].url" type="video/mp4" />
      Your browser does not support the video tag.
    </video>

    <div class="container">
      <ul class="list-inline" v-if="mediaUrls">
        <li
          v-for="(mediaUrl, index) in mediaUrls"
          v-bind:key="index"
          v-on:click="this.playingMediaIndex = index"
          class="col-1 m-0 list-inline-item text-center"
        >
          <a class="btn col-12 btn-dark">
            {{ mediaUrl.quality }}
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>



<script>
export default {
  name: "Play",
  props: ['imdbId'],
  data: function () {
    return {
      playingMediaIndex: 0,
      mediaUrls: false,
    };
  },
  methods: {
    setProperties: function (data) {
      this.mediaUrls = data.movies[0].sources.urls;
    },
    getMediaSources: function () {
      fetch("http://localhost:8000/graphql", {
        method: "post",
        body: JSON.stringify({
          query:
            '{movies( ids:["' +
            this.imdbId +
            '"]){sources{urls{url , quality}}}}',
        }),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          Authorization:
            "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNzM4ZDdjZDQtNzgyZS00MzZmLWFlOTMtODg0YjU2YzNlMmQzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjA4MDgwMTA2fQ.1PByIcMPogcYw5Ve6Xb_NXh1kqgJPlm1_XhC3LOKTJ4",
        },
      })
        .then((r) => r.json())
        .then((data) => this.setProperties(data.data));
    },
  },

  watch: {
    $route() {
      this.getMediaSources();
    },
  },

  mounted() {
    this.getMediaSources();
  },
};
</script>

<style scoped>
</style>