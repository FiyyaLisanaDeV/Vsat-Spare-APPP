"use client";

import { useState, useEffect } from "react";
import { masterDataApi } from "@/lib/api/master-data";
import { DataTable } from "@/components/master-data/DataTable";
import { Edit2, Ban, CheckCircle } from "lucide-react";

export default function ServicePointPage() {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [showInactive, setShowInactive] = useState(false);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState(null);
  
  // Debounce search
  const [debouncedSearch, setDebouncedSearch] = useState("");
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(searchTerm), 500);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const res = await masterDataApi.getServicePoints({
        page,
        search: debouncedSearch,
        show_inactive: showInactive,
      });
      if (res.success) {
        setData(res.data);
        setPagination(res.pagination);
      }
    } catch (error) {
      console.error(error);
      alert("Gagal memuat data service point");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [page, debouncedSearch, showInactive]);

  const handleToggle = async (item: any) => {
    if (confirm(`Apakah Anda yakin ingin ${item.is_active ? 'menonaktifkan' : 'mengaktifkan'} ${item.name}?`)) {
      try {
        await masterDataApi.toggleServicePoint(item.id);
        fetchData();
      } catch (error: any) {
        alert(error.response?.data?.message || "Gagal mengubah status");
      }
    }
  };

  const handleAdd = () => {
    alert("Fitur Tambah Service Point akan membuka modal form di sini.");
  };

  const handleEdit = (item: any) => {
    alert(`Fitur Edit Service Point (${item.name}) akan membuka modal form di sini.`);
  };

  const columns = [
    { key: "name", label: "Nama SP", render: (item: any) => (
        <div>
          <p className="font-medium text-gray-900">{item.name}</p>
          {!item.is_active && <span className="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-600 border border-gray-200">Nonaktif</span>}
        </div>
    )},
    { key: "type", label: "Tipe", render: (item: any) => (
      <span className="capitalize text-gray-600">{item.type.replace(/_/g, " ")}</span>
    )},
    { key: "location", label: "Lokasi", render: (item: any) => (
      <span className="text-gray-600">{item.city}, {item.province}</span>
    )},
    { key: "pic", label: "PIC", render: (item: any) => (
      <div>
        <p className="text-gray-900">{item.pic_name}</p>
        <p className="text-xs text-gray-500">{item.pic_phone}</p>
      </div>
    )},
  ];

  const renderActions = (item: any) => (
    <div className="flex justify-end gap-2">
      <button onClick={() => handleEdit(item)} className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-md" title="Edit">
        <Edit2 size={16} />
      </button>
      <button 
        onClick={() => handleToggle(item)} 
        className={`p-1.5 rounded-md ${item.is_active ? 'text-red-600 hover:bg-red-50' : 'text-green-600 hover:bg-green-50'}`}
        title={item.is_active ? "Nonaktifkan" : "Aktifkan"}
      >
        {item.is_active ? <Ban size={16} /> : <CheckCircle size={16} />}
      </button>
    </div>
  );

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Service Point</h1>
        <p className="text-gray-500 mt-1">Kelola data Service Point, Subcon, dan PIC Lokasi.</p>
      </div>

      <DataTable
        title="Daftar Service Point"
        columns={columns}
        data={data}
        isLoading={isLoading}
        onAdd={handleAdd}
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
