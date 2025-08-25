import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import { useState, FormEvent } from "react";
import { useRouter } from "next/router";
import { motion } from "framer-motion";
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
        <meta name="description" content="Crie sua conta no Portal AUDITORIA360" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      </Head>
      
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 px-4 overflow-hidden relative font-sans">
        {/* Background animated shapes */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-32 h-32 bg-blue-400/10 rounded-full blur-xl animate-pulse"></div>
          <div className="absolute top-1/4 right-16 w-24 h-24 bg-indigo-400/15 rounded-full blur-lg animate-bounce"></div>
          <div className="absolute bottom-32 left-1/4 w-40 h-40 bg-purple-400/8 rounded-full blur-2xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-20 h-20 bg-blue-300/20 rounded-full blur-lg animate-bounce delay-1000"></div>
        </div>

        {/* Main content */}
        <motion.div 
          className="max-w-md w-full relative z-10"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          {/* Logo and title */}
          <motion.div 
            className="text-center mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <motion.h1 
              className="text-5xl font-extrabold text-white mb-2"
              animate={{ 
                textShadow: [
                  "0 0 20px rgba(59, 130, 246, 0.5)",
                  "0 0 30px rgba(59, 130, 246, 0.8)",
                  "0 0 20px rgba(59, 130, 246, 0.5)"
                ]
              }}
              transition={{ 
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              AUDITORIA<span className="text-blue-300">360</span>
            </motion.h1>
            <motion.p 
              className="text-blue-100 text-lg font-medium"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              Primeiro Acesso
            </motion.p>
          </motion.div>

          {/* Registration card */}
          <motion.div
            className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-8 shadow-2xl"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <form className="space-y-6" onSubmit={handleSubmit}>
              {error && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="bg-red-50/90 backdrop-blur-sm border border-red-200 text-red-700 px-4 py-3 rounded-xl flex items-center gap-3"
                >
                  <motion.div
                    animate={{ rotate: [0, 10, -10, 0] }}
                    transition={{ duration: 0.5 }}
                    className="w-5 h-5 text-red-500"
                  >
                    ⚠️
                  </motion.div>
                  <span className="font-medium">{error}</span>
                </motion.div>
              )}

              <div>
                <label htmlFor="cnpj" className="block text-sm font-medium text-white mb-2">
                  CNPJ
                </label>
                <input
                  id="cnpj"
                  type="text"
                  value={cnpj}
                  onChange={(e) => setCnpj(e.target.value)}
                  required
                  placeholder="00.000.000/0001-00"
                  className="w-full px-4 py-3 rounded-xl backdrop-blur-sm bg-white/10 border border-white/20 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all"
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-white mb-2">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="seu@email.com"
                  className="w-full px-4 py-3 rounded-xl backdrop-blur-sm bg-white/10 border border-white/20 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-white mb-2">
                  Senha
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="Mínimo 6 caracteres"
                  className="w-full px-4 py-3 rounded-xl backdrop-blur-sm bg-white/10 border border-white/20 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className={`w-full py-3 px-6 rounded-xl font-bold text-white transition-all duration-300 transform hover:scale-105 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 ${
                  loading 
                    ? 'opacity-50 cursor-not-allowed' 
                    : 'hover:shadow-lg hover:shadow-blue-500/25'
                }`}
              >
                {loading ? (
                  <div className="flex items-center justify-center gap-2">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Criando conta...
                  </div>
                ) : (
                  'Criar Conta'
                )}
              </button>
            </form>
          </motion.div>

          {/* Login link */}
          <motion.div 
            className="mt-8 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <p className="text-blue-100 mb-3">Já possui uma conta?</p>
            <Link href="/login">
              <motion.span
                className="inline-flex items-center gap-2 text-blue-300 hover:text-white transition-colors duration-200 font-medium text-lg group"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Fazer login
                <motion.span
                  className="inline-block"
                  animate={{ x: [0, 5, 0] }}
                  transition={{ 
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                >
                  →
                </motion.span>
              </motion.span>
            </Link>
          </motion.div>

          {/* Back to home */}
          <motion.div 
            className="mt-6 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <Link href="/">
              <span className="text-blue-200 hover:text-white transition-colors duration-200 text-sm font-medium">
                ← Voltar ao início
              </span>
            </Link>
          </motion.div>
        </motion.div>

        {/* Gradient overlay for depth */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent pointer-events-none" />
      </div>
    </>
  );
};

export default RegisterPage;
