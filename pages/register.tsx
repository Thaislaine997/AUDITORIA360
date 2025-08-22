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
        <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
          {/* Enhanced gradient background with animation */}
          <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 animate-gradient-shift"></div>
          <div className="absolute inset-0 bg-gradient-to-tr from-blue-800/20 via-transparent to-purple-900/20"></div>
          
          {/* Floating decorative shapes */}
          <div className="absolute top-20 left-10 w-32 h-32 bg-blue-400/10 rounded-full blur-xl animate-float-1"></div>
          <div className="absolute top-1/4 right-16 w-24 h-24 bg-indigo-400/15 rounded-full blur-lg animate-float-2"></div>
          <div className="absolute bottom-32 left-1/4 w-40 h-40 bg-purple-400/8 rounded-full blur-2xl animate-float-3"></div>
          <div className="absolute bottom-20 right-20 w-28 h-28 bg-cyan-400/12 rounded-full blur-xl animate-float-1" style={{animationDelay: '10s'}}></div>
          <div className="absolute top-1/3 left-1/3 w-16 h-16 bg-blue-300/20 rounded-full blur-md animate-float-2" style={{animationDelay: '5s'}}></div>
          
          <div className="relative z-10 max-w-md w-full px-4">
            {/* Header with enhanced animation */}
            <div className="text-center mb-8 animate-fade-in">
              <h1 className="text-4xl font-extrabold text-white mb-2 animate-glow">
                Primeiro <span className="text-blue-300">Acesso</span>
              </h1>
              <p className="text-lg text-blue-100/80">
                Cadastre sua empresa e acesse a plataforma
              </p>
              <div className="w-20 h-1 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto mt-4 rounded-full"></div>
            </div>

            {/* Enhanced glassmorphism card */}
            <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 animate-glass-float">
              {/* Card shimmer effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-shimmer rounded-3xl"></div>
              
              <form className="space-y-6 relative z-10 animate-scale-in" onSubmit={handleSubmit}>
                {error && (
                  <div className="bg-red-500/20 backdrop-blur-sm border border-red-400/30 text-red-100 px-4 py-3 rounded-xl animate-enhanced-shake flex items-center space-x-3">
                    <svg className="w-5 h-5 text-red-300" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    <span>{error}</span>
                  </div>
                )}

                <div className="space-y-6">
                  <div className="group">
                    <label htmlFor="cnpj" className="block text-sm font-semibold text-white/90 mb-2">
                      CNPJ
                    </label>
                    <input
                      id="cnpj"
                      type="text"
                      required
                      value={cnpj}
                      onChange={(e) => setCnpj(e.target.value)}
                      className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50 transition-all duration-300 hover:bg-white/25"
                      placeholder="00.000.000/0001-00"
                    />
                  </div>

                  <div className="group">
                    <label htmlFor="email" className="block text-sm font-semibold text-white/90 mb-2">
                      Email
                    </label>
                    <input
                      id="email"
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50 transition-all duration-300 hover:bg-white/25"
                      placeholder="seu@email.com"
                    />
                  </div>

                  <div className="group">
                    <label htmlFor="password" className="block text-sm font-semibold text-white/90 mb-2">
                      Senha
                    </label>
                    <input
                      id="password"
                      type="password"
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50 transition-all duration-300 hover:bg-white/25"
                      placeholder="Mínimo 6 caracteres"
                    />
                  </div>
                </div>

                {/* Enhanced animated button */}
                <button
                  type="submit"
                  disabled={loading}
                  className={`
                    w-full py-4 px-6 rounded-xl font-semibold text-white text-lg
                    bg-gradient-to-r from-blue-500 to-indigo-600 
                    hover:from-blue-600 hover:to-indigo-700
                    focus:outline-none focus:ring-2 focus:ring-blue-400/50
                    disabled:opacity-50 disabled:cursor-not-allowed
                    transform transition-all duration-300
                    hover:scale-[1.02] hover:shadow-xl hover:shadow-blue-500/25
                    active:scale-[0.98]
                    relative overflow-hidden
                    ${loading ? 'animate-button-pulse' : ''}
                  `}
                >
                  {/* Button shimmer effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer"></div>
                  <span className="relative z-10 flex items-center justify-center">
                    {loading ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Registrando...
                      </>
                    ) : (
                      "Criar Conta"
                    )}
                  </span>
                </button>
              </form>
            </div>

            {/* Enhanced footer */}
            <div className="mt-8 text-center animate-fade-in" style={{animationDelay: '0.3s'}}>
              <p className="text-blue-100/80 mb-3">Já tem conta?</p>
              <Link 
                href="/login" 
                className="inline-flex items-center space-x-2 text-blue-300 hover:text-white transition-all duration-300 text-lg font-medium group"
              >
                <span>Fazer login</span>
                <svg className="w-5 h-5 transform transition-transform group-hover:translate-x-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </Layout>
      
      <style jsx>{`
        /* Enhanced responsivity */
        @media (max-width: 768px) {
          .floating-shape {
            transform: scale(0.7);
          }
        }
        
        @media (max-width: 480px) {
          .floating-shape {
            transform: scale(0.5);
          }
        }
      `}</style>
    </>
  );
};

export default RegisterPage;
