"use client";

import { useState, useEffect, useRef } from "react";
import { masterDataApi } from "@/lib/api/master-data";
import { Download, Upload, ServerCrash, AlertTriangle, RefreshCw } from "lucide-react";
import { authApi } from "@/lib/api/auth";

export default function BackupRestorePage() {
  const [backups, setBackups] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchBackups = async () => {
    try {
      setIsLoading(true);
      const res = await masterDataApi.getBackups();
      if (res.success) {
        setBackups(res.data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBackups();
  }, []);

  const handleCreateBackup = async () => {
    try {
      setIsProcessing(true);
      const res = await masterDataApi.createBackup();
      if (res.success) {
        alert(`Backup berhasil dibuat: ${res.data.filename}`);
        fetchBackups();
      }
    } catch (error: any) {
      alert(error.response?.data?.message || "Gagal membuat backup");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRestore = async (filename: string) => {
    if (!confirm("PERINGATAN!\n\nRestore akan menimpa seluruh database saat ini.\nTindakan ini TIDAK DAPAT DIBATALKAN.\n\nPastikan tidak ada pengguna lain yang sedang menggunakan sistem. Lanjutkan?")) {
      return;
    }

    try {
      setIsProcessing(true);
      const res = await masterDataApi.restoreFromExisting(filename);
      if (res.success) {
        alert(res.message);
        // Sesi direset oleh backend, jadi paksa logout di frontend
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    } catch (error: any) {
      alert(error.response?.data?.message || "Gagal melakukan restore");
      setIsProcessing(false);
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith(".sql")) {
      alert("Hanya file berekstensi .sql yang diperbolehkan.");
      return;
    }

    if (file.size > 200 * 1024 * 1024) {
      alert("Ukuran file maksimal 200MB.");
      return;
    }

    if (!confirm(`Anda akan merestore database dari file: ${file.name}\n\nSemua data saat ini akan ditimpa. Lanjutkan?`)) {
      if (fileInputRef.current) fileInputRef.current.value = "";
      return;
    }

    try {
      setIsProcessing(true);
      const res = await masterDataApi.restoreFromUpload(file);
      if (res.success) {
        alert(res.message);
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    } catch (error: any) {
      alert(error.response?.data?.message || "Gagal melakukan upload & restore");
      setIsProcessing(false);
    } finally {
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Backup & Restore</h1>
        <p className="text-gray-500 mt-1">Kelola pencadangan dan pemulihan database sistem.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Card Backup */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-100 text-blue-700 rounded-lg"><Download size={20} /></div>
            <h2 className="text-lg font-semibold text-gray-900">Backup Database</h2>
          </div>
          <p className="text-sm text-gray-600 mb-6">
            Sistem secara otomatis melakukan backup setiap hari pukul 01:00 WIB. Anda juga dapat membuat backup manual kapan saja.
          </p>
          <button
            onClick={handleCreateBackup}
            disabled={isProcessing}
            className="w-full flex items-center justify-center gap-2 bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {isProcessing ? <RefreshCw className="animate-spin" size={18} /> : "Buat Backup Sekarang"}
          </button>
        </div>

        {/* Card Restore Upload */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-red-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-red-100 text-red-700 rounded-lg"><Upload size={20} /></div>
            <h2 className="text-lg font-semibold text-gray-900">Upload & Restore</h2>
          </div>
          <div className="bg-red-50 p-3 rounded-lg flex gap-3 mb-4 border border-red-100">
            <AlertTriangle className="text-red-600 shrink-0" size={20} />
            <p className="text-xs text-red-800 leading-relaxed">
              <strong>Peringatan!</strong> Proses ini akan menimpa seluruh database aktif. Sistem akan otomatis logout setelah restore selesai.
            </p>
          </div>
          <input 
            type="file" 
            accept=".sql" 
            ref={fileInputRef} 
            onChange={handleUpload} 
            className="hidden" 
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isProcessing}
            className="w-full flex items-center justify-center gap-2 bg-red-600 text-white py-2.5 rounded-lg hover:bg-red-700 transition disabled:opacity-50"
          >
            {isProcessing ? <RefreshCw className="animate-spin" size={18} /> : "Upload File SQL"}
          </button>
        </div>
      </div>

      {/* Tabel Backup */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="p-5 border-b border-gray-200 bg-gray-50/50">
          <h2 className="text-lg font-semibold text-gray-900">Riwayat Backup</h2>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 font-medium tracking-wider">Nama File</th>
                <th className="px-6 py-4 font-medium tracking-wider">Tanggal & Waktu</th>
                <th className="px-6 py-4 font-medium tracking-wider">Ukuran</th>
                <th className="px-6 py-4 font-medium tracking-wider text-right">Aksi</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {isLoading ? (
                <tr><td colSpan={4} className="px-6 py-8 text-center text-gray-500">Memuat data...</td></tr>
              ) : backups.length === 0 ? (
                <tr><td colSpan={4} className="px-6 py-8 text-center text-gray-500">Belum ada file backup.</td></tr>
              ) : (
                backups.map((item: any) => (
                  <tr key={item.filename} className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-mono text-xs text-gray-900">{item.filename}</td>
                    <td className="px-6 py-4 text-gray-600">{item.created_at}</td>
                    <td className="px-6 py-4 text-gray-600">{item.size}</td>
                    <td className="px-6 py-4 text-right space-x-3">
                      <a 
                        href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/backup/download/${item.filename}`}
                        target="_blank"
                        className="text-blue-600 hover:text-blue-800 font-medium text-xs uppercase"
                      >
                        Download
                      </a>
                      <button 
                        onClick={() => handleRestore(item.filename)}
                        disabled={isProcessing}
                        className="text-red-600 hover:text-red-800 font-medium text-xs uppercase disabled:opacity-50"
                      >
                        Restore
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
