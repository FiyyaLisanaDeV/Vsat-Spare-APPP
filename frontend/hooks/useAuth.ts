import { create } from "zustand";

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  service_point_id: number | null;
  force_password_change: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  setAuth: (user, token) => {
    localStorage.setItem("access_token", token);
    localStorage.setItem("user", JSON.stringify(user));
    set({ user, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    set({ user: null, isAuthenticated: false });
  },
}));

// Helper untuk inisialisasi state di client
export const initAuth = () => {
  if (typeof window !== "undefined") {
    const userStr = localStorage.getItem("user");
    const token = localStorage.getItem("access_token");
    if (userStr && token) {
      try {
        const user = JSON.parse(userStr);
        useAuthStore.getState().setAuth(user, token);
      } catch (e) {
        localStorage.removeItem("user");
        localStorage.removeItem("access_token");
      }
    }
  }
};
