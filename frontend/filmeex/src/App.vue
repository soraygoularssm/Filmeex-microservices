<template>
  <navbar></navbar>
  <router-view></router-view>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: "App",
  components: {Navbar},
};
</script> 

<style>
@font-face {
  font-family: "Sahel";
  src: url("//bayanbox.ir/download/8915532961602652846/Sahel-FD.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: "Sahel";
  src: url("//bayanbox.ir/download/3150743715538152419/Sahel-Black.woff2")
    format("woff");
  font-weight: bold;
  font-style: normal;
}

html {
  scroll-behavior: smooth;
}

* {
  font-family: Sahel, tahoma !important;
}

.rtl {
  direction: rtl;
  text-align: right;
}

.ltr {
  direction: ltr;
  text-align: left;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
}
</style>
