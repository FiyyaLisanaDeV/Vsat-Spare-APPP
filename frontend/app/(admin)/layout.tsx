"use client";

import { useAuthStore } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Link from "next/link";
import { LogOut, Home, Database, Users, Shield, Box, Server } from "lucide-react";
import { authApi } from "@/lib/api/auth";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated || user?.role !== "admin_jakarta") {
      router.push("/login");
    }
  }, [isAuthenticated, user, router]);

  const handleLogout = async () => {
    try {
      await authApi.logout();
    } catch (e) {
      console.error(e);
    } finally {
      logout();
      router.push("/login");
    }
  };

  if (!isAuthenticated || user?.role !== "admin_jakarta") {
    return null;
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="p-4 flex items-center gap-3 border-b border-slate-800">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Server size={20} />
          </div>
          <div>
            <h1 className="font-bold text-lg">VSAT Admin</h1>
            <p className="text-xs text-slate-400">Pusat Manajemen</p>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-2">
            <li>
              <a href="/dashboard/admin" className="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-slate-800 text-slate-300 hover:text-white">
                <Home size={18} />
                <span>Dashboard</span>
              </a>
            </li>
            <li>
              <a href="/dashboard/admin/service-point" className="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-slate-800 text-slate-300 hover:text-white">
                <Database size={18} />
                <span>Service Point</span>
              </a>
            </li>
            <li className="pt-4 pb-1 px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              Master Data
            </li>
            <li>
              <a href="/dashboard/admin/master-data/jenis-barang" className="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-slate-800 text-slate-300 hover:text-white">
                <Box size={18} />
                <span>Jenis Barang</span>
              </a>
            </li>
            <li>
              <a href="/dashboard/admin/master-data/kategori-barang" className="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-slate-800 text-slate-300 hover:text-white">
                <Box size={18} />
                <span>Kategori Barang</span>
              </a>
            </li>
            <li>
              <a href="/dashboard/admin/master-data/spare-item" className="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-slate-800 text-slate-300 hover:text-white">
                <Box size={18} />
                <span>Spare Item</span>
              </a>
            </li>
            <li className="pt-4 pb-1 px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              Sistem
            </li>
            <li>
              <a href="/dashboard/admin/backup" className="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-slate-800 text-slate-300 hover:text-white">
                <Shield size={18} />
                <span>Backup & Restore</span>
              </a>
            </li>
            <li>
              <a href="/dashboard/admin/pengguna" className="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-slate-800 text-slate-300 hover:text-white">
                <Users size={18} />
                <span>Pengguna</span>
              </a>
            </li>
          </ul>
        </nav>

        <div className="p-4 border-t border-slate-800">
          <div className="mb-4">
            <p className="text-sm font-medium">{user.name}</p>
            <p className="text-xs text-slate-400">{user.email}</p>
          </div>
          <button
            onClick={handleLogout}
            className="flex w-full items-center justify-center gap-2 rounded-md bg-red-600/10 px-3 py-2 text-sm text-red-500 hover:bg-red-600/20 transition-colors"
          >
            <LogOut size={16} />
            Keluar
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
