import { NextPage } from "next";
import Head from "next/head";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Layout from "../components/layout/Layout";
import { authHelpers } from "../lib/supabaseClient";

const DashboardPage: NextPage = () => {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const currentUser = await authHelpers.getCurrentUser();
        if (!currentUser) {
          router.push("/login");
          return;
        }
        setUser(currentUser);
      } catch (error) {
        console.error("Error checking auth:", error);
        router.push("/login");
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  const handleLogout = async () => {
    try {
      await authHelpers.signOut();
      router.push("/");
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Carregando...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <>
      <Head>
        <title>Dashboard - AUDITORIA360</title>
        <meta name="description" content="Dashboard AUDITORIA360" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Layout>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">Bem-vindo, {user?.email}</p>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              Sair
            </button>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center">
                <div className="bg-blue-100 p-3 rounded-full">
                  <span className="text-blue-600 text-xl">📊</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Auditorias</p>
                  <p className="text-2xl font-semibold text-gray-900">124</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center">
                <div className="bg-green-100 p-3 rounded-full">
                  <span className="text-green-600 text-xl">👥</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Clientes</p>
                  <p className="text-2xl font-semibold text-gray-900">48</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center">
                <div className="bg-yellow-100 p-3 rounded-full">
                  <span className="text-yellow-600 text-xl">⚠️</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Pendências</p>
                  <p className="text-2xl font-semibold text-gray-900">12</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center">
                <div className="bg-purple-100 p-3 rounded-full">
                  <span className="text-purple-600 text-xl">📈</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Compliance</p>
                  <p className="text-2xl font-semibold text-gray-900">98%</p>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Recent Activities */}
            <div className="bg-white rounded-lg shadow-md">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">
                  Atividades Recentes
                </h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-sm text-gray-600">
                      Auditoria finalizada - Cliente ABC Ltda
                    </span>
                    <span className="text-xs text-gray-400">2h atrás</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <span className="text-sm text-gray-600">
                      Novo cliente cadastrado - XYZ Corp
                    </span>
                    <span className="text-xs text-gray-400">4h atrás</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                    <span className="text-sm text-gray-600">
                      Pendência identificada - DEF S/A
                    </span>
                    <span className="text-xs text-gray-400">1d atrás</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-md">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">
                  Ações Rápidas
                </h2>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-2 gap-4">
                  <button className="bg-blue-50 hover:bg-blue-100 p-4 rounded-lg text-center transition-colors">
                    <div className="text-2xl mb-2">🆕</div>
                    <span className="text-sm font-medium text-blue-600">
                      Nova Auditoria
                    </span>
                  </button>
                  <button className="bg-green-50 hover:bg-green-100 p-4 rounded-lg text-center transition-colors">
                    <div className="text-2xl mb-2">👤</div>
                    <span className="text-sm font-medium text-green-600">
                      Novo Cliente
                    </span>
                  </button>
                  <button className="bg-purple-50 hover:bg-purple-100 p-4 rounded-lg text-center transition-colors">
                    <div className="text-2xl mb-2">📊</div>
                    <span className="text-sm font-medium text-purple-600">
                      Relatórios
                    </span>
                  </button>
                  <button className="bg-orange-50 hover:bg-orange-100 p-4 rounded-lg text-center transition-colors">
                    <div className="text-2xl mb-2">⚙️</div>
                    <span className="text-sm font-medium text-orange-600">
                      Configurações
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
};

export default DashboardPage;
