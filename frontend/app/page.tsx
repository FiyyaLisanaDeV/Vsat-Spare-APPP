import { redirect } from "next/navigation";

export default function Home() {
  // Secara default redirect ke login
  // Middleware akan menangani jika user sudah login
  redirect("/login");
}
