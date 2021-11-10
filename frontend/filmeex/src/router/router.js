import { createWebHistory, createRouter } from "vue-router";
// import Home from "@components/Home"
import Home from "@/components/HomePage";
import Media from "@/components/MediaPage";
import Genres from "@/components/GenresPage";
import Register from "@/components/RegisterPage";
import Login from "@/components/LoginPage";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/media/:id",
    name: "Media",
    component: Media,
  },
  {
    path: "/genres",
    name: "Genres",
    component: Genres,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;