import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import { useState, FormEvent } from "react";
import { useRouter } from "next/router";
import { motion } from "framer-motion";
import Layout from "../components/layout/Layout";
import { authHelpers } from "../lib/supabaseClient";
import FloatingShapes from "../components/ui/FloatingShapes";
import GlassCard from "../components/ui/GlassCard";
import ModernInput from "../components/ui/ModernInput";
import ModernButton from "../components/ui/ModernButton";

const LoginPage: NextPage = () => {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const { data, error } = await authHelpers.signIn(email, password);
      if (error) {
        setError(error.message);
      } else if (data.user) {
        router.push("/dashboard");
      }
    } catch {
      setError("Erro ao fazer login. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Login - AUDITORIA360</title>
      </Head>
      <Layout showHeader={false}>
        <div className="min-h-screen relative flex items-center justify-center bg-gradient-to-br from-blue-900 via-indigo-900 to-purple-900 px-4 overflow-hidden">
          {/* Floating background shapes */}
          <FloatingShapes />
          
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
                Acesse sua conta
              </motion.p>
            </motion.div>

            {/* Glass login card */}
            <GlassCard className="p-8" opacity={0.95}>
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

                <ModernInput
                  id="email"
                  type="email"
                  label="Email"
                  placeholder="seu@email.com"
                  value={email}
                  onChange={setEmail}
                  required
                  error=""
                />

                <ModernInput
                  id="password"
                  type="password"
                  label="Senha"
                  placeholder="••••••••"
                  value={password}
                  onChange={setPassword}
                  required
                  error=""
                />

                <div className="flex justify-end">
                  <Link 
                    href="/recuperar-senha" 
                    className="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors duration-200 hover:underline"
                  >
                    Esqueceu a senha?
                  </Link>
                </div>

                <ModernButton
                  type="submit"
                  variant="primary"
                  size="lg"
                  disabled={loading}
                  loading={loading}
                  className="w-full"
                >
                  {loading ? "Entrando..." : "Entrar"}
                </ModernButton>
              </form>
            </GlassCard>

            {/* Register link */}
            <motion.div 
              className="mt-8 text-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <p className="text-blue-100 mb-3">Primeiro acesso?</p>
              <Link href="/register">
                <motion.span
                  className="inline-flex items-center gap-2 text-blue-300 hover:text-white transition-colors duration-200 font-medium text-lg group"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Criar conta
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
          </motion.div>

          {/* Gradient overlay for depth */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent pointer-events-none" />
        </div>
      </Layout>
    </>
  );
};

export default LoginPage;
