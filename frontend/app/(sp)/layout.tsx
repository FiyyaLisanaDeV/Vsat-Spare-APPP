"use client";

import { useAuthStore } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { LogOut, Home, Package, Activity, MapPin } from "lucide-react";
import { authApi } from "@/lib/api/auth";

export default function SpLayout({ children }: { children: React.ReactNode }) {
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated || user?.role !== "user_sp") {
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

  if (!isAuthenticated || user?.role !== "user_sp") {
    return null;
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-5 flex items-center gap-3 border-b border-gray-100">
          <div className="bg-indigo-600 p-2 rounded-lg text-white">
            <MapPin size={20} />
          </div>
          <div>
            <h1 className="font-bold text-lg text-gray-900">Service Point</h1>
            <p className="text-xs text-gray-500">VSAT Management</p>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-3">
            <li>
              <a href="/dashboard/sp" className="flex items-center gap-3 rounded-lg px-3 py-2.5 bg-indigo-50 text-indigo-700 font-medium">
                <Home size={18} />
                <span>Dashboard</span>
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-gray-600 hover:bg-gray-50 hover:text-gray-900">
                <Package size={18} />
                <span>Stok Saya</span>
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-gray-600 hover:bg-gray-50 hover:text-gray-900">
                <Activity size={18} />
                <span>Transaksi</span>
              </a>
            </li>
          </ul>
        </nav>

        <div className="p-5 border-t border-gray-100 bg-gray-50">
          <div className="mb-4">
            <p className="text-sm font-semibold text-gray-900">{user.name}</p>
            <p className="text-xs text-gray-500 truncate">{user.email}</p>
          </div>
          <button
            onClick={handleLogout}
            className="flex w-full items-center justify-center gap-2 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 hover:text-red-600 transition-colors shadow-sm"
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
