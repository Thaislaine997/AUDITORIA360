import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import { authHelpers, supabase } from '../lib/supabaseClient'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isSignUp, setIsSignUp] = useState(false)
  const router = useRouter()

  useEffect(() => {
    // Check if user is already logged in
    const checkUser = async () => {
      const user = await authHelpers.getCurrentUser()
      if (user) {
        router.push('/dashboard')
      }
    }
    checkUser()
  }, [router])

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      if (isSignUp) {
        const { data, error } = await authHelpers.signUp(email, password)
        if (error) throw error
        if (data.user && !data.user.email_confirmed_at) {
          setError('Verifique seu email para confirmar a conta!')
          return
        }
      } else {
        const { data, error } = await authHelpers.signIn(email, password)
        if (error) throw error
      }

      // Redirect to dashboard on success
      router.push('/dashboard')
    } catch (error: any) {
      setError(error.message || 'Erro na autenticação')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Login - Portal AUDITORIA360</title>
        <meta name="description" content="Acesse o Portal AUDITORIA360 para gestão completa da folha de pagamento e auditoria inteligente." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <div className="text-center">
              <Link href="/" className="inline-block">
                <h1 className="text-3xl font-bold text-blue-600 mb-2">AUDITORIA360</h1>
              </Link>
              <p className="text-gray-600">Portal de Gestão e Auditoria</p>
            </div>
            <h2 className="mt-8 text-center text-3xl font-bold text-gray-900">
              {isSignUp ? 'Criar conta' : 'Entre na sua conta'}
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              {isSignUp ? (
                <>
                  Já tem uma conta?{' '}
                  <button
                    type="button"
                    onClick={() => setIsSignUp(false)}
                    className="font-medium text-blue-600 hover:text-blue-500"
                  >
                    Faça login
                  </button>
                </>
              ) : (
                <>
                  Não tem uma conta?{' '}
                  <button
                    type="button"
                    onClick={() => setIsSignUp(true)}
                    className="font-medium text-blue-600 hover:text-blue-500"
                  >
                    Registre-se
                  </button>
                </>
              )}
            </p>
          </div>

          <form className="mt-8 space-y-6" onSubmit={handleAuth}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Email
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="appearance-none rounded-t-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                  placeholder="Endereço de email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Senha
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="appearance-none rounded-b-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                  placeholder="Senha"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
                {error}
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Carregando...
                  </div>
                ) : isSignUp ? (
                  'Criar conta'
                ) : (
                  'Entrar'
                )}
              </button>
            </div>

            <div className="text-center">
              <Link href="/" className="text-sm text-blue-600 hover:text-blue-500">
                ← Voltar ao site institucional
              </Link>
            </div>
          </form>

          <div className="mt-8 text-center">
            <div className="text-sm text-gray-600">
              <p>Portal seguro e protegido</p>
              <div className="flex items-center justify-center mt-2 space-x-4 text-xs">
                <span className="flex items-center">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
                  SSL Seguro
                </span>
                <span className="flex items-center">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
                  Dados Protegidos
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}