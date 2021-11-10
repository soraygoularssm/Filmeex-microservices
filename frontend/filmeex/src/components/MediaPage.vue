<template>
  <section
    class="detail-intro ptb100"
    :style="{
      'background-image':
        'linear-gradient(rgb(161, 31, 60, 0.95) 0%,rgb(147, 82, 179, 0.95) 100%),url(http://localhost:8000/files/photos/full/' +
        movie.poster +
        ')',
    }"
  >
    <div class="gradient-purple-layer"></div>
  </section>

  <section class="main-detail-intro pb-0" v-if="movie">
    <div class="container">
      <div class="row rtl">
        <div
          class="col-md-4 text-center"
          v-if="movie.imdbId"
          v-on:click="playMedia = !playMedia"
        >
          <a href="#playContent" class="play-video">
            <div class="overlay">
              <img
                class="rounded shadow-lg"
                v-bind:src="
                  'http://localhost:8000/files/photos/full/' + movie.poster
                "
                alt=""
              />
              <font-awesome-icon :icon="['fas', 'play']" class="play-icon" />
            </div>
          </a>
        </div>
        <div class="details col-md-8 text-center d-flex flex-column">
          <h2 class="pt-5 pb-2">{{ movie.name }}</h2>
          <ul class="list-inline px-0">
            <li class="list-inline-item">{{ movie.runtime }} دقیقه</li>
            <li class="list-inline-item px-3">
              {{ movie.genres.join(",") }}
            </li>
            <li class="font-weight-bold">
              10 / {{ movie.rating.rate }}
              <img
                class="mr-3"
                src="@/assets/imdb-logo.png"
                alt="Logo"
                style="width: 40px"
              />
            </li>
          </ul>
          <div class="row d-flex flex-grow-1 align-items-end mb-0 p-0">
            <div class="col-6 m-0 p-0 pl-2">
              <button
                v-if="movie.imdbId"
                type="button"
                class="btn shadow-none rounded-circle border bg-white text-center float-left ml-2 p-2"
                v-bind:class="{ bgpurple: isLoved }"
                style="width: 45px; height: 45px"
                v-on:click="likeMedia"
              >
                <font-awesome-icon
                  :icon="['far', 'heart']"
                  class="w-100 h-100"
                />
              </button>
            </div>
            <div class="col-6 m-0 p-0 pr-2">
              <button
                type="button"
                class="btn btn-rounded shadow-none border bg-white text-center float-right mr-2"
                style="font-size: 18px"
                v-bind:class="{ bgblack: isArchived }"
                v-on:click="archiveMedia"
              >
                <font-awesome-icon :icon="['far', 'bookmark']" class="ml-2" />
                ذخیره
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="playContent" class="pt-5" v-if="playMedia">
    <div class="container">
      <Play v-bind:imdbId="movie.imdbId"> </Play>
    </div>
  </section>

  <section class="pt-2">
    <div class="container">
      <div class="row rtl d-flex my-5">
        <div class="col-md-8 pt-2 d-flex flex-column" v-if="movie.summary">
          <h3 class="title">خلاصه فیلم</h3>
          <p>
            {{ movie.summary }}
          </p>

          <div class="row d-flex flex-grow-1 align-items-center">
            <ul class="list-group list-group-flush col-md-5 m-0 my-4 p-0">
              <li v-if="movie.year" class="list-group-item p-4">
                <strong class="px-2"> سال ساخت: </strong>
                {{ movie.year }}
              </li>
              <li v-if="movie.budget" class="list-group-item p-4">
                <strong class="px-2"> بودجه ساخت: </strong>
                {{ movie.budget }}
              </li>
              <li v-if="movie.countries" class="list-group-item p-4">
                <strong class="px-2"> کشور سازنده: </strong>
                {{ movie.countries.join(", ") }}
              </li>
              <li v-if="movie.languages" class="list-group-item p-4">
                <strong class="px-2"> زبان: </strong>
                {{ movie.languages.join(", ") }}
              </li>
            </ul>
          </div>
        </div>
        <div class="col-md-4 p-3">
          <ul class="list-group list-group-flush m-0 p-0 pb-3" v-if="directors">
            <h3 class="py-2 bgpurple text-white rounded-top text-center">
              کارگردان
            </h3>
            <li
              v-for="director in directors"
              v-bind:key="director.imdbid"
              class="m-0 p-1 list-group-item ltr shadow"
            >
              <span class="avatar pr-3">
                <img :src="director.headshot" />
              </span>
              {{ director.name }}
            </li>
          </ul>

          <ul class="list-group list-group-flush m-0 p-0" v-if="stars">
            <h3 class="py-2 bgpurple text-white rounded-top text-center">
              ستارگان
            </h3>
            <li
              v-for="star in stars"
              v-bind:key="star.imdbid"
              class="m-0 p-1 list-group-item ltr shadow"
            >
              <span class="avatar pr-3">
                <img :src="star.headshot" />
              </span>
              {{ star.name }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container rtl">
      <h3 class="px-4">فیلم های مشابه</h3>
      <div class="wrapper">
        <div
          v-for="sugMovie in suggestions"
          v-bind:key="sugMovie.imdbid"
          class="col-6 col-md-4 col-lg-3"
        >
          <router-link :to="'/media/' + sugMovie.imdbId">
            <img
              class="rounded sug-poster"
              v-bind:src="
                'http://localhost:8000/files/photos/full/' + sugMovie.poster
              "
              alt=""
            />
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Play from "./PlayPage";

export default {
  components: { Play },
  name: "Media",

  data: function () {
    return {
      movie: false,
      suggestions: false,
      stars: false,
      directors: false,
      isLoved: false,
      lovedList: false,
      isArchived: false,
      archivedList: false,
      playMedia: false,
    };
  },

  methods: {
    setProperties: function (data) {
      this.movie = data.movies[0];
      this.suggestions = data.suggestions;
      if (data.users) {
        this.lovedList = data.users[0].loved;
        if (this.lovedList.includes(this.imdbId)) {
          this.isLoved = true;
        }
        this.archivedList = data.users[0].archived;
        if (this.archivedList.includes(this.imdbId)) {
          this.isArchived = true;
        }
      }
    },
    setCrew: function (data) {
      var stars = [];
      var directors = [];
      for (var i = 0; i < data.cast.length; i++) {
        if (this.movie.crew.stars.includes(data.cast[i].imdbId)) {
          stars.push(data.cast[i]);
        } else if (this.movie.crew.directors.includes(data.cast[i].imdbId)) {
          directors.push(data.cast[i]);
        }
      }
      this.stars = stars;
      if (directors.length > 0) {
        this.directors = directors;
      }
    },
    getCrew: function () {
      var castIds = [];
      var starsIds = [];
      var starsLength = this.movie.crew.stars.length;
      for (var i = 0; i < starsLength; i++) {
        starsIds.push(this.movie.crew.stars[i].id);
      }
      this.movie.crew.stars = starsIds;
      castIds = starsIds.concat(this.movie.crew.directors);
      castIds = JSON.stringify(castIds);
      fetch("http://localhost:8000/graphql", {
        method: "post",
        body: JSON.stringify({
          query: "{cast(ids:" + castIds + "){imdbId , name , headshot}}",
        }),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((r) => r.json())
        .then((data) => this.setCrew(data.data));
    },
    getMedia: function () {
      fetch("http://localhost:8000/graphql", {
        method: "post",
        body: JSON.stringify({
          query:
            '{movies( ids:["' +
            this.$route.params.id +
            '"]){imdbId , name , runtime , poster , summary , year , budget , likes , genres , countries , languages , crew {stars{id} directors} , rating{rate , ratesAmount}, sources{urls{url}}}, suggestions(id:"' +
            this.$route.params.id +
            '"){imdbId , poster} , users{loved , archived}}',
        }),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((r) => r.json())
        .then((data) => this.setProperties(data.data))
        .then(() => this.getCrew());
    },
    likeMedia: function () {
      if (this.likes !== false) {
        var likes = 0;
        var lovedList = this.lovedList;
        if (this.isLoved) {
          likes = this.likes--;
          this.isLoved = false;
          lovedList.splice(lovedList.indexOf(this.imdbId), 1);
        } else {
          likes = this.likes++;
          this.isLoved = true;
          lovedList.push(this.imdbId);
        }

        fetch("http://localhost:8000/graphql", {
          method: "post",
          body: JSON.stringify({
            query:
              'mutation {updateMovie(id:"tt0468569",movieInput:{likes:' +
              likes +
              "}){ok} , UpdateUser(userInput:{loved:" +
              JSON.stringify(this.lovedList) +
              "}){ok}}",
          }),
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        });
      }
    },
    archiveMedia: function () {
      if (this.likes !== false) {
        if (this.isArchived) {
          this.isArchived = false;
          this.archivedList.splice(this.archivedList.indexOf(this.imdbId), 1);
        } else {
          this.isArchived = true;
          this.archivedList.push(this.imdbId);
        }

        fetch("http://localhost:8000/graphql", {
          method: "post",
          body: JSON.stringify({
            query:
              "mutation {UpdateUser(userInput:{archived:" +
              JSON.stringify(this.archivedList) +
              "}){ok}}",
          }),
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        });
      }
    },
  },

  watch: {
    $route() {
      this.getMedia();
    },
  },

  mounted() {
    this.getMedia();
  },
};
</script>

<style scoped>
img {
  max-width: 100%;
}

.bgpurple {
  background: linear-gradient(to bottom, #a11f3c 0%, #9352b3 100%);
  color: white;
}

.bgred {
  background-color: red !important;
  color: white;
}

.bgblack {
  background-color: black !important;
  color: white;
}

.ptb100 {
  padding: 100px 0;
}

.detail-intro {
  color: #fff;
  min-height: 500px;
  background-repeat: no-repeat !important;
  background-size: cover !important;
  background-position: center;
  /* filter: blur(8px);
  -webkit-filter: blur(8px); */
}

.overlay {
  position: relative;
  display: inline-block;
}

.overlay::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, #a11f3c 0%, #9352b3 100%);
  opacity: 0;
  transition: 0.5s ease;
}

.overlay:hover::before {
  opacity: 0.7;
}

.overlay:hover .play-icon {
  opacity: 1;
}

.play-icon {
  color: white;
  font-size: 60px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  z-index: 10;
  -webkit-transition: all 0.5s ease;
  transition: all 0.5s ease;
  text-align: center;
  opacity: 0;
}

.play-icon:hover {
  font-size: 90px;
}

.details {
  color: #fff;
}

.half-clear {
  opacity: 0.7;
}

.main-detail-intro {
  display: block;
  position: relative;
  margin-top: -300px;
}

.storyline h3 .title {
  color: #3e4555;
  font-size: 30px;
}

.storyline p {
  clear: #948a99;
  font-size: 20px;
}

.avatar img {
  border-radius: 4px;
  max-width: 60px;
  max-height: 60px;
  object-fit: cover;
  width: auto;
  height: auto;
}

.wrapper {
  display: flex;
  overflow-x: auto;
  direction: rtl;
}

.wrapper::-webkit-scrollbar {
  width: 0;
}

.sug-poster {
  object-fit: cover;
  flex-shrink: 0;
  min-width: 100%;
  min-height: 100%;
  /* height: 350px; */
}
</style>