import {
  createRouter,
  createWebHistory,
} from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";

import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(
    import.meta.env.BASE_URL
  ),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
  ],
});

router.beforeEach(
  async (to, from, next) => {
    const authStore = useAuthStore();
    await authStore.checkAuth();

    if (
      to.meta.requiresAuth &&
      !authStore.isAuthenticated
    ) {
      next({ name: "login" });
    } else if (
      (to.name === "login" ||
        to.name === "register") &&
      authStore.isAuthenticated
    ) {
      next({ name: "products" });
    } else {
      next();
    }
  }
);

export default router;
