"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { authApi } from "@/lib/api/auth";
import { useAuthStore } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";

const formSchema = z.object({
  current_password: z.string().min(1, { message: "Password lama tidak boleh kosong" }),
  new_password: z.string()
    .min(8, { message: "Password minimal 8 karakter" })
    .regex(/[A-Z]/, { message: "Harus mengandung minimal 1 huruf besar" })
    .regex(/[0-9]/, { message: "Harus mengandung minimal 1 angka" }),
});

export default function ChangePasswordPage() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const setAuth = useAuthStore((state) => state.setAuth);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      current_password: "",
      new_password: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      setIsLoading(true);
      setError("");
      const res = await authApi.changePassword(values);
      if (res.success) {
        // Update state
        if (user) {
          const updatedUser = { ...user, force_password_change: false };
          const token = localStorage.getItem("access_token") || "";
          setAuth(updatedUser, token);
          
          router.push(updatedUser.role === "admin_jakarta" ? "/dashboard/admin" : "/dashboard/sp");
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Terjadi kesalahan saat mengganti password");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex h-screen w-full items-center justify-center bg-gray-50">
      <div className="w-full max-w-md rounded-xl bg-white p-8 shadow-lg ring-1 ring-gray-200">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-gray-900">Ganti Password</h1>
          <p className="mt-2 text-sm text-gray-600">Anda diwajibkan mengganti password untuk melanjutkan.</p>
        </div>

        {error && (
          <div className="mb-6 rounded-md bg-red-50 p-4 text-sm text-red-600 ring-1 ring-red-200">
            {error}
          </div>
        )}

        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Password Lama</label>
            <input
              type="password"
              {...form.register("current_password")}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              disabled={isLoading}
            />
            {form.formState.errors.current_password && (
              <p className="mt-1 text-sm text-red-600">{form.formState.errors.current_password.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Password Baru</label>
            <input
              type="password"
              {...form.register("new_password")}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              disabled={isLoading}
            />
            {form.formState.errors.new_password && (
              <p className="mt-1 text-sm text-red-600">{form.formState.errors.new_password.message}</p>
            )}
            <p className="mt-2 text-xs text-gray-500">Minimal 8 karakter, mengandung huruf besar dan angka.</p>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="flex w-full justify-center rounded-md bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50"
          >
            {isLoading ? "Memproses..." : "Simpan Password"}
          </button>
        </form>
      </div>
    </div>
  );
}
