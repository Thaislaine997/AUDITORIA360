import Link from "next/link";
import { useRouter } from "next/router";
import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
  title?: string;
  showHeader?: boolean;
}

export default function Layout({
  children,
  title = "AUDITORIA360",
  showHeader = true,
}: LayoutProps) {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-50">
      {showHeader && (
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center">
                <Link href="/" className="flex items-center">
                  <h1 className="text-2xl font-bold text-blue-600">
                    AUDITORIA360
                  </h1>
                  <span className="ml-3 text-sm text-gray-500">
                    Portal de Gestão
                  </span>
                </Link>
              </div>
              <nav className="flex items-center space-x-4">
                {router.pathname.startsWith("/dashboard") ? (
                  <Link
                    href="/"
                    className="text-sm text-gray-600 hover:text-blue-600"
                  >
                    ← Voltar ao site
                  </Link>
                ) : (
                  <Link
                    href="/login"
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                  >
                    Acessar Portal
                  </Link>
                )}
              </nav>
            </div>
          </div>
        </header>
      )}
      <main>{children}</main>
    </div>
  );
}
