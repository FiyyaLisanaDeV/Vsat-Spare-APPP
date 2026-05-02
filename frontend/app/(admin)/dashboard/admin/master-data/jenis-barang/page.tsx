"use client";

import { useState, useEffect } from "react";
import { masterDataApi } from "@/lib/api/master-data";
import { DataTable } from "@/components/master-data/DataTable";
import { Edit2, Ban, CheckCircle } from "lucide-react";

export default function JenisBarangPage() {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [showInactive, setShowInactive] = useState(false);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState(null);
  
  const [debouncedSearch, setDebouncedSearch] = useState("");
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(searchTerm), 500);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const res = await masterDataApi.getItemTypes({
        page, search: debouncedSearch, show_inactive: showInactive,
      });
      if (res.success) {
        setData(res.data);
        setPagination(res.pagination);
      }
    } catch (error) {
      alert("Gagal memuat data jenis barang");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [page, debouncedSearch, showInactive]);

  const handleToggle = async (item: any) => {
    if (confirm(`Yakin ingin ${item.is_active ? 'menonaktifkan' : 'mengaktifkan'} ${item.name}?`)) {
      try {
        await masterDataApi.toggleItemType(item.id);
        fetchData();
      } catch (error: any) {
        alert(error.response?.data?.message || "Gagal mengubah status");
      }
    }
  };

  const columns = [
    { key: "name", label: "Nama Jenis Barang", render: (item: any) => (
        <div className="flex items-center gap-2">
          <span className="font-medium text-gray-900">{item.name}</span>
          {!item.is_active && <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-600 border border-gray-200">Nonaktif</span>}
        </div>
    )},
  ];

  const renderActions = (item: any) => (
    <div className="flex justify-end gap-2">
      <button onClick={() => alert("Fitur edit")} className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-md">
        <Edit2 size={16} />
      </button>
      <button onClick={() => handleToggle(item)} className={`p-1.5 rounded-md ${item.is_active ? 'text-red-600 hover:bg-red-50' : 'text-green-600 hover:bg-green-50'}`}>
        {item.is_active ? <Ban size={16} /> : <CheckCircle size={16} />}
      </button>
    </div>
  );

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Jenis Barang</h1>
        <p className="text-gray-500 mt-1">Kelola master data Jenis Barang (Item Type).</p>
      </div>

      <DataTable
        title="Daftar Jenis Barang"
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
