export default function AdminDashboardPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard Admin</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Total Service Point</h3>
          <p className="text-3xl font-bold text-gray-900">3</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Pengguna Aktif</h3>
          <p className="text-3xl font-bold text-gray-900">1</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Total Item Barang</h3>
          <p className="text-3xl font-bold text-gray-900">5</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-orange-500">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Pending Approval</h3>
          <p className="text-3xl font-bold text-orange-600">0</p>
          <p className="text-xs text-gray-400 mt-1">Akan datang di Mission 2</p>
        </div>
      </div>
    </div>
  );
}
