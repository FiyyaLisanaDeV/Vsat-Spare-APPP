import axios from "axios";

// URL base API di-proxy via Next.js atau direct
const baseURL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const axiosInstance = axios.create({
  baseURL,
  withCredentials: true, // Penting untuk mengirim httpOnly cookie (refresh token)
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor untuk menyisipkan Access Token
axiosInstance.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Interceptor untuk menangani error dan refresh token
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Jika 401 dan bukan saat request refresh token itu sendiri
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== "/api/auth/refresh") {
      originalRequest._retry = true;

      try {
        // Coba refresh token
        const refreshRes = await axios.post(
          `${baseURL}/api/auth/refresh`,
          {},
          { withCredentials: true }
        );

        if (refreshRes.data.success) {
          const newToken = refreshRes.data.data.access_token;
          if (typeof window !== "undefined") {
            localStorage.setItem("access_token", newToken);
          }
          // Ulangi request dengan token baru
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return axios(originalRequest);
        }
      } catch (refreshError) {
        // Jika refresh gagal, redirect ke login
        if (typeof window !== "undefined") {
          localStorage.removeItem("access_token");
          localStorage.removeItem("user");
          window.location.href = "/login";
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
