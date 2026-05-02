import axios from "../axios";

export const authApi = {
  login: async (data: any) => {
    const response = await axios.post("/api/auth/login", data);
    return response.data;
  },
  logout: async () => {
    const response = await axios.post("/api/auth/logout");
    return response.data;
  },
  getMe: async () => {
    const response = await axios.get("/api/auth/me");
    return response.data;
  },
  changePassword: async (data: any) => {
    const response = await axios.post("/api/auth/change-password", data);
    return response.data;
  },
};
