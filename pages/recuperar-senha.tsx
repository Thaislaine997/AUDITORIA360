import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import { useState, FormEvent } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { authHelpers } from "../lib/supabaseClient";

const RecuperarSenha: NextPage = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [messageType, setMessageType] = useState<"success" | "error" | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setMessageType(null);

    try {
      const { error } = await authHelpers.resetPassword(email);
      if (error) {
        setMessage("Erro ao enviar e-mail. Verifique se o endereço está correto.");
        setMessageType("error");
      } else {
        setMessage("E-mail de recuperação enviado! Verifique sua caixa de entrada e spam.");
        setMessageType("success");
      }
    } catch {
      setMessage("Erro inesperado. Tente novamente em alguns momentos.");
      setMessageType("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Recuperar Senha - AUDITORIA360</title>
        <meta name="description" content="Recupere sua senha do Portal AUDITORIA360" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      </Head>
      
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-700 via-blue-800 to-slate-900 px-4 relative overflow-hidden font-sans">
        {/* Background animated shapes */}
        <div className="absolute inset-0">
          <motion.div
            className="absolute top-1/4 left-1/4 w-32 h-32 bg-blue-400/20 rounded-full blur-xl"
            animate={{
              x: [0, 30, 0],
              y: [0, -30, 0],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <motion.div
            className="absolute top-3/4 right-1/4 w-24 h-24 bg-purple-400/15 rounded-full blur-xl"
            animate={{
              x: [0, -20, 0],
              y: [0, 20, 0],
              scale: [1, 0.9, 1],
            }}
            transition={{
              duration: 6,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 1
            }}
          />
        </div>

        {/* Main content */}
        <motion.div 
          className="max-w-md w-full relative z-10"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        >
          {/* Header */}
          <motion.div 
            className="text-center mb-8"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h1 className="text-4xl font-extrabold text-white">
              AUDITORIA<span className="text-blue-300">360</span>
            </h1>
            <p className="mt-2 text-blue-100">Recuperar sua senha</p>
          </motion.div>

          {/* Glass Card */}
          <motion.div 
            className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-8 shadow-2xl"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <form className="space-y-6" onSubmit={handleSubmit}>
              {/* Email Input */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
              >
                <label htmlFor="email" className="block text-sm font-medium text-white mb-2">
                  Endereço de Email
                </label>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl backdrop-blur-sm bg-white/10 border border-white/20 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all"
                  placeholder="seu@email.com"
                />
              </motion.div>

              {/* Submit Button */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.5 }}
              >
                <button
                  type="submit"
                  disabled={loading}
                  className={`w-full py-3 px-4 rounded-xl text-white font-medium transition-all duration-300 transform hover:scale-105 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 ${
                    loading 
                      ? 'opacity-50 cursor-not-allowed' 
                      : 'hover:shadow-lg hover:shadow-blue-500/25'
                  }`}
                >
                  {loading ? (
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Enviando...
                    </div>
                  ) : (
                    'Enviar link de recuperação'
                  )}
                </button>
              </motion.div>

              {/* Animated Message */}
              <AnimatePresence>
                {message && (
                  <motion.div
                    initial={{ opacity: 0, y: 10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -10, scale: 0.95 }}
                    transition={{ duration: 0.3, ease: "easeOut" }}
                    className={`p-4 rounded-xl backdrop-blur-sm ${
                      messageType === "success"
                        ? "bg-green-500/20 border border-green-400/30 text-green-100"
                        : "bg-red-500/20 border border-red-400/30 text-red-100"
                    }`}
                  >
                    <div className="flex items-center">
                      <span className="mr-2">
                        {messageType === "success" ? "✅" : "⚠️"}
                      </span>
                      {message}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </form>
          </motion.div>

          {/* Back to Login Link */}
          <motion.div 
            className="mt-8 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <p className="text-blue-100 mb-3">Lembrou da senha?</p>
            <Link href="/login">
              <motion.span
                className="inline-flex items-center gap-2 text-blue-300 hover:text-white transition-colors duration-200 font-medium text-lg group"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Voltar ao login
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

export default RecuperarSenha;