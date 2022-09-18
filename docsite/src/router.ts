import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"
import HomeView from "./views/HomeView.vue"
import { libName } from "./conf"

const baseTitle = libName;

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: HomeView,
    meta: {
      title: "Home"
    }
  },
  {
    path: "/apidoc",
    component: () => import("./views/ApidocView.vue"),
    meta: {
      title: "Apidoc"
    }
  },
  {
    path: "/apidoc/:file",
    component: () => import("./views/ApidocDetailView.vue"),
    meta: {
      title: "Apidoc"
    }
  },
  {
    path: "/example/:file",
    component: () => import("./views/ExamplesDetailView.vue"),
    meta: {
      title: "Example"
    }
  },
  {
    path: "/examples",
    component: () => import("./views/ExamplesView.vue"),
    meta: {
      title: "Examples"
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.afterEach((to, from) => { // eslint-disable-line
  document.title = `${baseTitle} - ${to.meta?.title}`
});

export default router