import axios from "axios";
import { jwtDecode } from "jwt-decode";

import { useAuthStore } from "@/stores/auth";

const apiClient = axios.create({
  baseURL: import.meta.env
    .VITE_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

let isRefreshing = false;
let failedQueue = [];

const processQueue = (
  error,
  token = null
) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest =
      error.config;

    if (
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      const authStore = useAuthStore();
      const refreshToken =
        authStore.refreshToken;

      if (!refreshToken) {
        authStore.logout();
        return Promise.reject(error);
      }

      if (isRefreshing) {
        return new Promise(function (
          resolve,
          reject
        ) {
          failedQueue.push({
            resolve,
            reject,
          });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return apiClient(
              originalRequest
            );
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      }
      isRefreshing = true;

      try {
        const response =
          await axios.post(
            `${
              import.meta.env
                .VITE_API_BASE_URL
            }/token/refresh/`,
            {
              refresh: refreshToken,
            }
          );
        const newAccessToken =
          response.data.access;
        const newRefreshToken =
          response.data.refresh;

        authStore.setTokens(
          newAccessToken,
          newRefreshToken
        );
        processQueue(
          null,
          newAccessToken
        );
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return apiClient(
          originalRequest
        );
      } catch (refreshError) {
        console.log(
          "Token refresh failed",
          refreshError
        );
        authStore.logout();
        processQueue(
          refreshError,
          null
        );
        return Promise.reject(
          refreshError
        );
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
