import Head from 'next/head'
import Link from 'next/link'
import { useState } from 'react'

export default function Home() {
  return (
    <>
      <Head>
        <title>DPEIXER | Assessoria & Terceirização de Departamento Pessoal</title>
        <meta 
          name="description" 
          content="DPEIXER oferece terceirização completa de folha de pagamento, eSocial, FGTS Digital e DCTFWeb. Planos flexíveis e suporte especializado para contabilidades e empresas." 
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold text-blue-600">DPEIXER</h1>
                <span className="ml-2 text-sm text-gray-600">Assessoria & Terceirização</span>
              </div>
              <nav className="hidden md:flex space-x-8">
                <a href="#sobre" className="text-gray-700 hover:text-blue-600 font-medium">Sobre</a>
                <a href="#servicos" className="text-gray-700 hover:text-blue-600 font-medium">Serviços</a>
                <a href="#planos" className="text-gray-700 hover:text-blue-600 font-medium">Planos</a>
                <Link href="/login" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 font-medium">
                  Portal AUDITORIA360
                </Link>
              </nav>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-7xl mx-auto text-center">
            <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Terceirização de Departamento Pessoal
              <span className="block text-blue-600">com Excelência e Conformidade</span>
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              A DPEIXER oferece soluções completas em Departamento Pessoal e Recursos Humanos, 
              voltadas para contabilidades e empresas que buscam precisão, segurança jurídica e eficiência operacional.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/login" className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors">
                Acessar Portal
              </Link>
              <a href="#planos" className="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-50 transition-colors">
                Ver Planos
              </a>
            </div>
          </div>
        </section>

        {/* About Section */}
        <section id="sobre" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h3 className="text-3xl font-bold text-gray-900 mb-4">Sobre a Empresa</h3>
              <div className="w-24 h-1 bg-blue-600 mx-auto"></div>
            </div>
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <p className="text-lg text-gray-700 mb-6">
                  Somos especialistas em processamento de folha de pagamento, gestão de admissões, férias, rescisões, 
                  integração com eSocial, DCTFWeb, FGTS Digital e cumprimento de obrigações acessórias.
                </p>
                <p className="text-lg text-gray-700 mb-6">
                  Utilizamos tecnologia de ponta, processos auditáveis e equipe altamente comprometida para garantir 
                  compliance, redução de riscos trabalhistas e tranquilidade aos nossos clientes.
                </p>
                <div className="grid grid-cols-2 gap-4 mt-8">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600">100%</div>
                    <div className="text-sm text-gray-600">Processos Digitais</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">24/7</div>
                    <div className="text-sm text-gray-600">Suporte Disponível</div>
                  </div>
                </div>
              </div>
              <div className="bg-blue-50 p-8 rounded-xl">
                <h4 className="text-xl font-semibold text-gray-900 mb-4">Nossos Diferenciais</h4>
                <ul className="space-y-3">
                  <li className="flex items-center text-gray-700">
                    <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
                    Ponto digital com geolocalização
                  </li>
                  <li className="flex items-center text-gray-700">
                    <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
                    Gestão automatizada de benefícios
                  </li>
                  <li className="flex items-center text-gray-700">
                    <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
                    Assinatura eletrônica integrada
                  </li>
                  <li className="flex items-center text-gray-700">
                    <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
                    Processos auditáveis e seguros
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Services Section */}
        <section id="servicos" className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h3 className="text-3xl font-bold text-gray-900 mb-4">Nossos Serviços</h3>
              <div className="w-24 h-1 bg-blue-600 mx-auto"></div>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              <ServiceCard 
                title="Processamento Mensal da Folha"
                description="Cálculo detalhado de salários, benefícios, descontos. Emissão e envio de holerites, guias (INSS, FGTS, IRRF). Integração direta com eSocial, DCTFWeb e FGTS Digital."
              />
              <ServiceCard 
                title="Compliance e Obrigações"
                description="Gestão completa de declarações e acompanhamento de devoluções. Aplicação de convenções coletivas, revisões fiscais e previdenciárias."
              />
              <ServiceCard 
                title="Consultoria Trabalhista"
                description="Diagnóstico de passivos, revisão de contratos e políticas internas. Recomendações técnicas para mitigação de riscos."
              />
              <ServiceCard 
                title="Gestão de Informação"
                description="Integração segura com sistemas do cliente, backups automáticos, controle de versões. Operação via plataforma própria."
              />
              <ServiceCard 
                title="Serviços Sob Demanda"
                description="Admissão/rescisão digital, recálculos, homologações online por videochamada. Preço por evento, flexível para demandas pontuais."
              />
              <ServiceCard 
                title="Portal AUDITORIA360"
                description="Plataforma completa de auditoria e gestão, com dashboard inteligente, relatórios automatizados e análise de dados."
              />
            </div>
          </div>
        </section>

        {/* Plans Section */}
        <section id="planos" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h3 className="text-3xl font-bold text-gray-900 mb-4">Planos e Valores</h3>
              <div className="w-24 h-1 bg-blue-600 mx-auto"></div>
              <p className="text-lg text-gray-600 mt-4">Escolha o plano ideal para sua necessidade</p>
            </div>
            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <PlanCard 
                name="Plus"
                price="39,90"
                description="Todos os serviços regulares, exceto admissões/rescisões e documentos personalizados"
                features={[
                  "Processamento da folha mensal",
                  "Integração eSocial/DCTFWeb",
                  "Relatórios básicos",
                  "Suporte por email"
                ]}
                popular={false}
              />
              <PlanCard 
                name="Premium"
                price="49,90"
                description="Tudo do Plus + admissões/rescisões digitais, homologações por vídeo"
                features={[
                  "Todos os recursos do Plus",
                  "Admissões/rescisões digitais",
                  "Homologações por videochamada",
                  "Portal AUDITORIA360 básico",
                  "Suporte prioritário"
                ]}
                popular={true}
              />
              <PlanCard 
                name="Diamante"
                price="69,90"
                description="Premium + documentação personalizada, reuniões exclusivas, People Analytics"
                features={[
                  "Todos os recursos do Premium",
                  "Documentação personalizada",
                  "Reuniões exclusivas mensais",
                  "People Analytics avançado",
                  "Portal AUDITORIA360 completo",
                  "Suporte dedicado 24/7"
                ]}
                popular={false}
              />
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-gray-900 text-white py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-4 gap-8">
              <div>
                <h4 className="text-lg font-semibold mb-4">DPEIXER</h4>
                <p className="text-gray-400">
                  Assessoria & Terceirização de Departamento Pessoal com excelência e conformidade.
                </p>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-4">Serviços</h4>
                <ul className="space-y-2 text-gray-400">
                  <li>Processamento da Folha</li>
                  <li>Compliance Trabalhista</li>
                  <li>Portal AUDITORIA360</li>
                  <li>Consultoria Especializada</li>
                </ul>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-4">Planos</h4>
                <ul className="space-y-2 text-gray-400">
                  <li>Plus - R$ 39,90</li>
                  <li>Premium - R$ 49,90</li>
                  <li>Diamante - R$ 69,90</li>
                </ul>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-4">Portal</h4>
                <Link href="/login" className="text-blue-400 hover:text-blue-300 block mb-2">
                  Acessar AUDITORIA360
                </Link>
                <p className="text-gray-400 text-sm">
                  Gestão completa e auditoria inteligente
                </p>
              </div>
            </div>
            <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
              <p>&copy; 2024 DPEIXER. Todos os direitos reservados.</p>
            </div>
          </div>
        </footer>
      </main>
    </>
  )
}

function ServiceCard({ title, description }: { title: string, description: string }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <h4 className="text-xl font-semibold text-gray-900 mb-3">{title}</h4>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function PlanCard({ 
  name, 
  price, 
  description, 
  features, 
  popular 
}: { 
  name: string
  price: string
  description: string
  features: string[]
  popular: boolean
}) {
  return (
    <div className={`bg-white p-8 rounded-xl border-2 ${popular ? 'border-blue-500 shadow-lg' : 'border-gray-200'} relative`}>
      {popular && (
        <span className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
          Mais Popular
        </span>
      )}
      <div className="text-center">
        <h4 className="text-2xl font-bold text-gray-900 mb-2">{name}</h4>
        <div className="mb-4">
          <span className="text-3xl font-bold text-blue-600">R$ {price}</span>
          <span className="text-gray-600">/mês por vida</span>
        </div>
        <p className="text-gray-600 mb-6 text-sm">{description}</p>
      </div>
      <ul className="space-y-3 mb-8">
        {features.map((feature, index) => (
          <li key={index} className="flex items-center text-sm">
            <span className="w-2 h-2 bg-green-500 rounded-full mr-3 flex-shrink-0"></span>
            {feature}
          </li>
        ))}
      </ul>
      <button className={`w-full py-3 rounded-lg font-semibold transition-colors ${
        popular 
          ? 'bg-blue-600 text-white hover:bg-blue-700' 
          : 'border border-blue-600 text-blue-600 hover:bg-blue-50'
      }`}>
        Contratar Plano
      </button>
    </div>
  )
}