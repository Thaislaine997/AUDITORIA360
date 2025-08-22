import { NextPage } from "next";
import Head from "next/head";
import { useState, FormEvent } from "react";
import Layout from "../components/layout/Layout";
import { authHelpers } from "../lib/supabaseClient";

const RecuperarSenha: NextPage = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const { error } = await authHelpers.resetPassword(email);
    if (error) {
      setMessage("Erro ao enviar e-mail.");
    } else {
      setMessage("E-mail de recuperação enviado. Verifique sua caixa de entrada.");
    }
  };

  return (
    <>
      <Head>
        <title>Recuperar Senha - AUDITORIA360</title>
      </Head>
      <Layout showHeader={false}>
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-800 to-blue-900 px-4">
          <div className="max-w-md w-full bg-white/90 backdrop-blur-lg p-8 rounded-2xl shadow-2xl">
            <h1 className="text-2xl font-bold text-gray-800 mb-4">Recuperar Senha</h1>
            <form className="space-y-4" onSubmit={handleSubmit}>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg focus:ring-blue-600"
                placeholder="Digite seu email"
              />
              <button
                type="submit"
                className="w-full py-3 px-4 rounded-lg text-white bg-blue-600 hover:bg-blue-700"
              >
                Enviar link de recuperação
              </button>
            </form>
            {message && <p className="mt-4 text-sm text-gray-600">{message}</p>}
          </div>
        </div>
      </Layout>
    </>
  );
};

export default RecuperarSenha;
