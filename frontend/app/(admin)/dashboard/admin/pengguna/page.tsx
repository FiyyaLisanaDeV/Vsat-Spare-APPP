"use client";

import { useState, useEffect } from "react";
import { masterDataApi } from "@/lib/api/master-data";
import { DataTable } from "@/components/master-data/DataTable";
import { Edit2, Ban, CheckCircle, KeyRound } from "lucide-react";
import { useAuthStore } from "@/hooks/useAuth";

export default function PenggunaPage() {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [showInactive, setShowInactive] = useState(false);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState(null);
  const currentUser = useAuthStore((state) => state.user);
  
  const [debouncedSearch, setDebouncedSearch] = useState("");
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(searchTerm), 500);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const res = await masterDataApi.getUsers({
        page, search: debouncedSearch, show_inactive: showInactive,
      });
      if (res.success) {
        setData(res.data);
        setPagination(res.pagination);
      }
    } catch (error) {
      alert("Gagal memuat data pengguna");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [page, debouncedSearch, showInactive]);

  const handleToggle = async (item: any) => {
    if (item.id === currentUser?.id) {
      alert("Anda tidak bisa menonaktifkan akun sendiri.");
      return;
    }
    if (confirm(`Yakin ingin ${item.is_active ? 'menonaktifkan' : 'mengaktifkan'} user ${item.name}?`)) {
      try {
        await masterDataApi.toggleUser(item.id);
        fetchData();
      } catch (error: any) {
        alert(error.response?.data?.message || "Gagal mengubah status");
      }
    }
  };

  const handleResetPassword = async (item: any) => {
    if (confirm(`Yakin ingin mereset password untuk ${item.name}? User akan dipaksa mengganti password saat login berikutnya.`)) {
      try {
        await masterDataApi.resetPassword(item.id);
        alert("Password berhasil direset menjadi: Vsat123!");
        fetchData();
      } catch (error: any) {
        alert(error.response?.data?.message || "Gagal mereset password");
      }
    }
  };

  const columns = [
    { key: "name", label: "Pengguna", render: (item: any) => (
        <div>
          <span className="font-medium text-gray-900 flex items-center gap-2">
            {item.name}
            {item.id === currentUser?.id && <span className="text-[10px] bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">Anda</span>}
          </span>
          <span className="text-xs text-gray-500 block">{item.email}</span>
          {!item.is_active && <span className="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-600 border border-gray-200">Nonaktif</span>}
        </div>
    )},
    { key: "role", label: "Role", render: (item: any) => (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${item.role === 'admin_jakarta' ? 'bg-purple-100 text-purple-700' : 'bg-indigo-100 text-indigo-700'}`}>
        {item.role === 'admin_jakarta' ? 'Admin Jakarta' : 'User SP'}
      </span>
    )},
    { key: "service_point", label: "Lokasi", render: (item: any) => (
      <span className="text-gray-600 text-sm">{item.service_point_name || '-'}</span>
    )},
    { key: "last_login", label: "Login Terakhir", render: (item: any) => (
      <span className="text-gray-500 text-xs">
        {item.last_login ? new Date(item.last_login).toLocaleString('id-ID') : 'Belum pernah'}
      </span>
    )},
  ];

  const renderActions = (item: any) => (
    <div className="flex justify-end gap-2">
      <button onClick={() => handleResetPassword(item)} className="p-1.5 text-orange-600 hover:bg-orange-50 rounded-md" title="Reset Password">
        <KeyRound size={16} />
      </button>
      <button onClick={() => alert("Fitur edit")} className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-md" title="Edit">
        <Edit2 size={16} />
      </button>
      <button 
        onClick={() => handleToggle(item)} 
        disabled={item.id === currentUser?.id}
        className={`p-1.5 rounded-md disabled:opacity-30 ${item.is_active ? 'text-red-600 hover:bg-red-50' : 'text-green-600 hover:bg-green-50'}`}
      >
        {item.is_active ? <Ban size={16} /> : <CheckCircle size={16} />}
      </button>
    </div>
  );

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Pengguna Sistem</h1>
        <p className="text-gray-500 mt-1">Kelola akun pengguna, reset password, dan hak akses.</p>
      </div>

      <DataTable
        title="Daftar Pengguna"
        columns={columns}
        data={data}
        isLoading={isLoading}
        onAdd={() => alert("Fitur tambah")}
        onSearch={setSearchTerm}
        searchTerm={searchTerm}
        showInactive={showInactive}
        setShowInactive={setShowInactive}
        pagination={pagination}
        setPage={setPage}
        actions={renderActions}
      />
    </div>
  );
}
