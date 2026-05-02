import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("refresh_token")?.value;
  const path = request.nextUrl.pathname;

  // Izinkan akses ke halaman public atau API Auth
  const isAuthPage = path.startsWith("/login");
  
  if (!token && !isAuthPage) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (token && isAuthPage) {
    // Jika sudah login, tidak perlu ke halaman login
    // Kita arahkan ke root dan biarkan frontend fetch role untuk re-routing yang tepat
    // (Bisa juga decode JWT tapi Next.js middleware butuh jose atau library lain, kita bypass ke client/dashboard)
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api/auth (auth API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api/auth|_next/static|_next/image|favicon.ico).*)",
  ],
};
