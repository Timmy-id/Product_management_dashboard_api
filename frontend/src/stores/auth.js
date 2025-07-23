import { defineStore } from "pinia";
import apiClient from "@/api";
import { jwtDecode } from "jwt-decode";

import router from "@/router";

export const useAuthStore = defineStore(
  "auth",
  {
    state: () => ({
      user: null,
      accessToken:
        localStorage.getItem(
          "accessToken"
        ) || null,
      refreshToken:
        localStorage.getItem(
          "refreshToken"
        ) || null,
    }),
    getters: {
      isAuthenticated: (state) =>
        !!state.accessToken,
      currentUser: (state) =>
        state.user,
      isAccessTokenExpired: (state) => {
        if (!state.accessToken)
          return true;
        try {
          const decoded = jwtDecode(
            state.accessToken
          );
          const currentTime =
            Date.now() / 1000;
          return (
            decoded.exp < currentTime
          );
        } catch (error) {
          return true;
        }
      },
      isRefreshTokenExpired: (
        state
      ) => {
        if (!state.refreshToken)
          return true;
        try {
          const decoded = jwtDecode(
            state.refreshToken
          );
          const currentTime =
            Date.now() / 1000;
          return (
            decoded.exp < currentTime
          );
        } catch (error) {
          return true;
        }
      },
    },
    actions: {
      setTokens(access, refresh) {
        this.accessToken = access;
        this.refreshToken = refresh;
        localStorage.setItem(
          "accessToken",
          access
        );
        localStorage.setItem(
          "refreshToken",
          refresh
        );
        this.fetchUser();
      },
      clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
        this.user = null;
        localStorage.removeItem(
          "accessToken"
        );
        localStorage.removeItem(
          "refreshToken"
        );
      },
      async login(credentials) {
        try {
          const response =
            await apiClient.post(
              "/token/",
              credentials
            );
          this.setTokens(
            response.data.access,
            response.data.refresh
          );
          router.push({
            name: "products",
          });
          return true;
        } catch (error) {
          console.error(
            "Login failed: ",
            error.response?.data ||
              error.message
          );
          throw error;
        }
      },
      async register(userData) {
        try {
          const response =
            await apiClient.post(
              "/users/register/",
              userData
            );
          router.push({
            name: "login",
          });
          return true;
        } catch (error) {
          console.error(
            "Registration failed: ",
            error.response?.data ||
              error.message
          );
          throw error;
        }
      },
      async logout() {
        this.clearTokens();
        router.push({ name: "login" });
      },
      async fetchUser() {
        if (!this.accessToken) {
          this.user = null;
          return;
        }
        try {
          const response =
            await apiClient.get(
              "/users/profile"
            );
          if (
            response.data &&
            response.data.results &&
            response.data.results
              .length > 0
          ) {
            this.user =
              response.data.results[0];
          } else {
            this.user = null; // No user found or list is empty
            this.logout(); // If token is valid but no user profile found, logout
          }
        } catch (error) {
          console.error(
            "Failed to fetch user: ",
            error.response?.data ||
              error.message
          );
          this.logout();
        }
      },
      async checkAuth() {
        if (
          this.isAuthenticated &&
          this.isAccessTokenExpired &&
          this.refreshToken
        ) {
          console.log(
            "Access token expired, attempting refresh..."
          );
          try {
            await this.refreshTokenAction();
            await this.fetchUser();
          } catch (error) {
            console.error(
              "Failed to refresh token",
              error
            );
            this.logout();
          }
        } else if (
          this.isAuthenticated &&
          !this.isAccessTokenExpired
        ) {
          await this.fetchUser();
        } else {
          this.clearTokens();
        }
      },
      async refreshTokenAction() {
        if (
          !this.refreshToken ||
          this.isRefreshTokenExpired
        ) {
          throw new Error(
            "No refresh token available or expired"
          );
        }
        try {
        } catch (error) {
          console.error(
            "Refresh token failed",
            error.response?.data ||
              error.message
          );
          this.logout();
          throw error;
        }
      },
    },
  }
);
