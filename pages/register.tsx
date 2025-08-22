import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import { useState, FormEvent } from "react";
import { useRouter } from "next/router";
import Layout from "../components/layout/Layout";
import { authHelpers } from "../lib/supabaseClient";

const RegisterPage: NextPage = () => {
  const router = useRouter();
  const [cnpj, setCnpj] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const { data, error } = await authHelpers.signUp(email, password, cnpj);
      if (error) {
        setError(error.message);
      } else if (data.user) {
        router.push("/dashboard");
      }
    } catch {
      setError("Erro ao registrar. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Primeiro Acesso - AUDITORIA360</title>
      </Head>
      <Layout showHeader={false}>
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-800 via-blue-800 to-blue-900 px-4">
          <div className="max-w-md w-full">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-extrabold text-white">Primeiro Acesso</h1>
              <p className="mt-2 text-blue-100">Cadastre sua empresa e acesse a plataforma</p>
            </div>

            <div className="bg-white/90 backdrop-blur-lg rounded-2xl shadow-2xl p-8">
              <form className="space-y-6" onSubmit={handleSubmit}>
                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg animate-shake">
                    {error}
                  </div>
                )}

                <div>
                  <label htmlFor="cnpj" className="block text-sm font-medium text-gray-700">
                    CNPJ
                  </label>
                  <input
                    id="cnpj"
                    type="text"
                    required
                    value={cnpj}
                    onChange={(e) => setCnpj(e.target.value)}
                    className="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-blue-600"
                    placeholder="00.000.000/0001-00"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                    Email
                  </label>
                  <input
                    id="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-blue-600"
                    placeholder="seu@email.com"
                  />
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                    Senha
                  </label>
                  <input
                    id="password"
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-blue-600"
                    placeholder="Mínimo 6 caracteres"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 px-4 rounded-lg text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? "Registrando..." : "Registrar"}
                </button>
              </form>
            </div>

            <div className="mt-6 text-center text-sm text-blue-100">
              <p>Já tem conta?</p>
              <Link href="/login" className="mt-2 inline-block text-blue-300 hover:text-white transition">
                Fazer login →
              </Link>
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
};

export default RegisterPage;
