import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import { authHelpers } from '../lib/supabaseClient'

interface User {
  id: string
  email?: string
  user_metadata?: {
    full_name?: string
  }
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    checkUser()
  }, [])

  const checkUser = async () => {
    try {
      const currentUser = await authHelpers.getCurrentUser()
      if (!currentUser) {
        router.push('/login')
        return
      }
      setUser(currentUser)
    } catch (error) {
      console.error('Error checking user:', error)
      router.push('/login')
    } finally {
      setLoading(false)
    }
  }

  const handleSignOut = async () => {
    try {
      await authHelpers.signOut()
      router.push('/')
    } catch (error) {
      console.error('Error signing out:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null // Will redirect to login
  }

  return (
    <>
      <Head>
        <title>Dashboard - Portal AUDITORIA360</title>
        <meta name="description" content="Dashboard do Portal AUDITORIA360 - Gestão completa da folha de pagamento e auditoria inteligente." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold text-blue-600">AUDITORIA360</h1>
                <span className="ml-3 text-sm text-gray-500">Portal de Gestão</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">
                  Olá, {user.user_metadata?.full_name || user.email}
                </span>
                <button
                  onClick={handleSignOut}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
                >
                  Sair
                </button>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Welcome Section */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Bem-vindo ao Portal AUDITORIA360
            </h2>
            <p className="text-gray-600">
              Sua central de controle para gestão da folha de pagamento e auditoria inteligente.
            </p>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatsCard
              title="Folhas Processadas"
              value="127"
              subtitle="Este mês"
              color="blue"
            />
            <StatsCard
              title="Auditorias Ativas"
              value="34"
              subtitle="Em andamento"
              color="green"
            />
            <StatsCard
              title="Demandas Abertas"
              value="12"
              subtitle="Aguardando análise"
              color="yellow"
            />
            <StatsCard
              title="Compliance"
              value="98.5%"
              subtitle="Taxa de conformidade"
              color="purple"
            />
          </div>

          {/* Dashboard Modules */}
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            <DashboardModule
              title="Controle da Folha Mensal"
              description="Resumo, status, valores e gráficos da folha de pagamento"
              icon="📊"
              href="/folha"
            />
            <DashboardModule
              title="Portal de Demandas"
              description="Gestão de tickets: abertos, em andamento, finalizados"
              icon="🎫"
              href="/demandas"
            />
            <DashboardModule
              title="Portal de Auditoria"
              description="Upload de resumos e análise automática integrada"
              icon="🔍"
              href="/auditoria"
            />
            <DashboardModule
              title="Tabelas Oficiais"
              description="INSS, FGTS, IRRF, salário família e mínimo atualizados"
              icon="📋"
              href="/tabelas"
            />
            <DashboardModule
              title="Portal CCT"
              description="Convenções coletivas: importar, status e buscas online"
              icon="📄"
              href="/cct"
            />
            <DashboardModule
              title="Gestão e Relatórios"
              description="Relatórios integrados com todas as funcionalidades"
              icon="📈"
              href="/relatorios"
            />
          </div>

          {/* Recent Activity */}
          <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Atividade Recente</h3>
            <div className="space-y-4">
              <ActivityItem
                title="Folha processada com sucesso"
                description="Empresa XYZ Ltda - Novembro/2024"
                time="2 horas atrás"
                status="success"
              />
              <ActivityItem
                title="Nova demanda recebida"
                description="Solicitação de recálculo de férias - Ticket #1234"
                time="4 horas atrás"
                status="info"
              />
              <ActivityItem
                title="Auditoria finalizada"
                description="Análise de conformidade - Empresa ABC S.A."
                time="1 dia atrás"
                status="success"
              />
              <ActivityItem
                title="CCT atualizada"
                description="Sindicato dos Metalúrgicos - Nova convenção importada"
                time="2 dias atrás"
                status="info"
              />
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-8 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white">
            <h3 className="text-lg font-semibold mb-4">Ações Rápidas</h3>
            <div className="flex flex-wrap gap-4">
              <button className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                Nova Auditoria
              </button>
              <button className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                Processar Folha
              </button>
              <button className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                Gerar Relatório
              </button>
              <button className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                Importar CCT
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

function StatsCard({ title, value, subtitle, color }: {
  title: string
  value: string
  subtitle: string
  color: 'blue' | 'green' | 'yellow' | 'purple'
}) {
  const colorClasses = {
    blue: 'text-blue-600 bg-blue-50 border-blue-200',
    green: 'text-green-600 bg-green-50 border-green-200',
    yellow: 'text-yellow-600 bg-yellow-50 border-yellow-200',
    purple: 'text-purple-600 bg-purple-50 border-purple-200'
  }

  return (
    <div className={`p-6 rounded-lg border ${colorClasses[color]}`}>
      <h3 className="text-sm font-medium text-gray-600">{title}</h3>
      <p className={`text-2xl font-bold mt-1 ${colorClasses[color].split(' ')[0]}`}>{value}</p>
      <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
    </div>
  )
}

function DashboardModule({ title, description, icon, href }: {
  title: string
  description: string
  icon: string
  href: string
}) {
  return (
    <Link href={href}>
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
        <div className="flex items-start">
          <div className="text-3xl mr-4">{icon}</div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
            <p className="text-gray-600 text-sm">{description}</p>
          </div>
        </div>
      </div>
    </Link>
  )
}

function ActivityItem({ title, description, time, status }: {
  title: string
  description: string
  time: string
  status: 'success' | 'info' | 'warning'
}) {
  const statusClasses = {
    success: 'bg-green-100 text-green-600',
    info: 'bg-blue-100 text-blue-600',
    warning: 'bg-yellow-100 text-yellow-600'
  }

  return (
    <div className="flex items-start space-x-3 py-2">
      <div className={`w-2 h-2 rounded-full mt-2 ${statusClasses[status].replace('text-', 'bg-').replace('100', '600')}`}></div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-600">{description}</p>
        <p className="text-xs text-gray-400 mt-1">{time}</p>
      </div>
    </div>
  )
}