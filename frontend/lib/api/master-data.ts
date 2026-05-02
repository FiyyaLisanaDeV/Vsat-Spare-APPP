import axios from "../axios";

export const masterDataApi = {
  // === Service Points ===
  getServicePoints: async (params?: any) => {
    const res = await axios.get("/api/service-points", { params });
    return res.data;
  },
  createServicePoint: async (data: any) => {
    const res = await axios.post("/api/service-points", data);
    return res.data;
  },
  updateServicePoint: async (id: number, data: any) => {
    const res = await axios.put(`/api/service-points/${id}`, data);
    return res.data;
  },
  toggleServicePoint: async (id: number) => {
    const res = await axios.patch(`/api/service-points/${id}/toggle-active`);
    return res.data;
  },

  // === Item Types (Jenis Barang) ===
  getItemTypes: async (params?: any) => {
    const res = await axios.get("/api/items/types", { params });
    return res.data;
  },
  createItemType: async (data: any) => {
    const res = await axios.post("/api/items/types", data);
    return res.data;
  },
  updateItemType: async (id: number, data: any) => {
    const res = await axios.put(`/api/items/types/${id}`, data);
    return res.data;
  },
  toggleItemType: async (id: number) => {
    const res = await axios.patch(`/api/items/types/${id}/toggle-active`);
    return res.data;
  },

  // === Item Categories (Kategori Barang) ===
  getItemCategories: async (params?: any) => {
    const res = await axios.get("/api/items/categories", { params });
    return res.data;
  },
  createItemCategory: async (data: any) => {
    const res = await axios.post("/api/items/categories", data);
    return res.data;
  },
  updateItemCategory: async (id: number, data: any) => {
    const res = await axios.put(`/api/items/categories/${id}`, data);
    return res.data;
  },
  toggleItemCategory: async (id: number) => {
    const res = await axios.patch(`/api/items/categories/${id}/toggle-active`);
    return res.data;
  },

  // === Spare Items ===
  getSpareItems: async (params?: any) => {
    const res = await axios.get("/api/items/spare", { params });
    return res.data;
  },
  createSpareItem: async (data: any) => {
    const res = await axios.post("/api/items/spare", data);
    return res.data;
  },
  updateSpareItem: async (id: number, data: any) => {
    const res = await axios.put(`/api/items/spare/${id}`, data);
    return res.data;
  },
  toggleSpareItem: async (id: number) => {
    const res = await axios.patch(`/api/items/spare/${id}/toggle-active`);
    return res.data;
  },

  // === Users ===
  getUsers: async (params?: any) => {
    const res = await axios.get("/api/users", { params });
    return res.data;
  },
  createUser: async (data: any) => {
    const res = await axios.post("/api/users", data);
    return res.data;
  },
  updateUser: async (id: number, data: any) => {
    const res = await axios.put(`/api/users/${id}`, data);
    return res.data;
  },
  toggleUser: async (id: number) => {
    const res = await axios.patch(`/api/users/${id}/toggle-active`);
    return res.data;
  },
  resetPassword: async (id: number) => {
    const res = await axios.post(`/api/users/${id}/reset-password`);
    return res.data;
  },

  // === Backup & Restore ===
  getBackups: async () => {
    const res = await axios.get("/api/backup/list");
    return res.data;
  },
  createBackup: async () => {
    const res = await axios.post("/api/backup/create");
    return res.data;
  },
  restoreFromExisting: async (filename: string) => {
    const res = await axios.post(`/api/backup/restore/${filename}`);
    return res.data;
  },
  restoreFromUpload: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("/api/backup/restore/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  },
};
