"use client";

import { useAuthStore } from "@/hooks/useAuth";

export default function SpDashboardPage() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Selamat Datang, {user?.name}</h1>
        <p className="text-gray-500 mt-1">Ini adalah pusat kontrol stok spare item di lokasi Anda.</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 col-span-2">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Ringkasan Stok</h2>
          <div className="flex items-center justify-center h-48 bg-gray-50 rounded-lg border border-dashed border-gray-300">
            <p className="text-gray-500">Data stok akan tampil di sini (Mission 2)</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Informasi Service Point</h2>
          <div className="space-y-4">
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Status</p>
              <p className="text-sm font-medium text-green-600 flex items-center gap-1 mt-1">
                <span className="w-2 h-2 rounded-full bg-green-500 inline-block"></span>
                Aktif
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Tipe Akses</p>
              <p className="text-sm font-medium text-gray-900 mt-1">Subcon / Service Representative</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
