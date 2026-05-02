import React from "react";
import { Search, Plus, Filter } from "lucide-react";

interface DataTableProps {
  title: string;
  columns: { key: string; label: string; render?: (item: any) => React.ReactNode }[];
  data: any[];
  isLoading: boolean;
  onAdd: () => void;
  onSearch: (term: string) => void;
  searchTerm: string;
  showInactive: boolean;
  setShowInactive: (show: boolean) => void;
  pagination: { page: number; total_pages: number; total: number } | null;
  setPage: (page: number) => void;
  actions?: (item: any) => React.ReactNode;
}

export function DataTable({
  title,
  columns,
  data,
  isLoading,
  onAdd,
  onSearch,
  searchTerm,
  showInactive,
  setShowInactive,
  pagination,
  setPage,
  actions,
}: DataTableProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Header & Controls */}
      <div className="p-5 border-b border-gray-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-gray-50/50">
        <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input
              type="text"
              placeholder="Cari..."
              value={searchTerm}
              onChange={(e) => onSearch(e.target.value)}
              className="pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-64"
            />
          </div>
          
          <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
            <input
              type="checkbox"
              checked={showInactive}
              onChange={(e) => setShowInactive(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            Tampilkan Nonaktif
          </label>

          <button
            onClick={onAdd}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            <Plus size={16} />
            Tambah Data
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-200">
            <tr>
              {columns.map((col) => (
                <th key={col.key} className="px-6 py-4 font-medium tracking-wider">
                  {col.label}
                </th>
              ))}
              {actions && <th className="px-6 py-4 font-medium tracking-wider text-right">Aksi</th>}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {isLoading ? (
              <tr>
                <td colSpan={columns.length + (actions ? 1 : 0)} className="px-6 py-8 text-center text-gray-500">
                  Memuat data...
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (actions ? 1 : 0)} className="px-6 py-8 text-center text-gray-500">
                  Tidak ada data ditemukan.
                </td>
              </tr>
            ) : (
              data.map((item, idx) => (
                <tr key={item.id || idx} className={`hover:bg-gray-50 transition-colors ${!item.is_active ? 'bg-gray-50/50' : ''}`}>
                  {columns.map((col) => (
                    <td key={col.key} className="px-6 py-4 whitespace-nowrap">
                      {col.render ? col.render(item) : item[col.key]}
                    </td>
                  ))}
                  {actions && (
                    <td className="px-6 py-4 whitespace-nowrap text-right space-x-2">
                      {actions(item)}
                    </td>
                  )}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination && pagination.total_pages > 1 && (
        <div className="p-4 border-t border-gray-200 flex items-center justify-between bg-gray-50/50">
          <span className="text-sm text-gray-600">
            Total {pagination.total} data
          </span>
          <div className="flex items-center gap-2">
            <button
              disabled={pagination.page <= 1}
              onClick={() => setPage(pagination.page - 1)}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              Sebelumnya
            </button>
            <span className="text-sm font-medium text-gray-700 px-2">
              Halaman {pagination.page} dari {pagination.total_pages}
            </span>
            <button
              disabled={pagination.page >= pagination.total_pages}
              onClick={() => setPage(pagination.page + 1)}
              className="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              Selanjutnya
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
