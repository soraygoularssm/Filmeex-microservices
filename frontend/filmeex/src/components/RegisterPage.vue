<template>
  <div class="container">
    <div class="p-5 m-5">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="exampleInputEmail1">Email address</label>
          <input
            type="email"
            class="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
            placeholder="Enter email"
            v-model="email"
          />
          <small id="emailHelp" class="form-text text-muted"
            >We'll never share your email with anyone else.</small
          >
        </div>
        <div class="form-group">
          <label for="exampleInputPassword1">Password</label>
          <input
            type="password"
            class="form-control"
            id="exampleInputPassword1"
            placeholder="Password"
            v-model="password"
          />
        </div>
        <div class="form-check">
          <input type="checkbox" class="form-check-input" id="exampleCheck1" />
          <label class="form-check-label" for="exampleCheck1"
            >Check me out</label
          >
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>
</template>



<script>
export default {
  name: "Register",
  data: function () {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    login: function () {
      fetch("http://localhost:8000/auth/jwt/login", {
        body: "username="+ this.email +"&password=" + this.password,
        headers: {
          Accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: "POST",
      })
        .then((r) => r.json())
        .then((data) => localStorage.setItem('token' , data.access_token))
        .then(() => this.email = "" ,  this.password = "");
    },
    handleSubmit: function () {
      fetch("http://localhost:8000/auth/register", {
        method: "post",
        body: JSON.stringify({
          email: this.email,
          password: this.password,
        }),
        // headers: {
        //   "Content-Type": "application/json",
        //   Accept: "application/json",
        //   Authorization:
        //     "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNzM4ZDdjZDQtNzgyZS00MzZmLWFlOTMtODg0YjU2YzNlMmQzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjA4MDgwMTA2fQ.1PByIcMPogcYw5Ve6Xb_NXh1kqgJPlm1_XhC3LOKTJ4",
        // },
      }).then(() => this.login());
    },
  },
};
</script>

<style scoped>
</style>