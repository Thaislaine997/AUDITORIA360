import { NextPage } from 'next'
import Head from 'next/head'
import Link from 'next/link'
import Layout from '../components/layout/Layout'

const HomePage: NextPage = () => {
  return (
    <>
      <Head>
        <title>AUDITORIA360 - Plataforma Moderna de Terceirização de Departamento Pessoal</title>
        <meta name="description" content="AUDITORIA360 - Soluções modernas em Departamento Pessoal e Recursos Humanos" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Layout>
        <div className="relative">
          {/* Hero Section */}
          <section className="bg-gradient-to-br from-blue-600 to-blue-800 text-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
              <div className="text-center">
                <h1 className="text-4xl md:text-6xl font-bold mb-6">
                  AUDITORIA360
                </h1>
                <p className="text-xl md:text-2xl mb-8 text-blue-100">
                  Plataforma Moderna de Terceirização de Departamento Pessoal
                </p>
                <p className="text-lg mb-10 max-w-3xl mx-auto text-blue-50">
                  Soluções completas em Departamento Pessoal e Recursos Humanos para contabilidades e empresas
                  que buscam precisão, eficiência e compliance trabalhista.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link 
                    href="/login" 
                    className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                  >
                    Acessar Portal
                  </Link>
                  <a 
                    href="#funcionalidades" 
                    className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
                  >
                    Conhecer Soluções
                  </a>
                </div>
              </div>
            </div>
          </section>

          {/* Features Section */}
          <section id="funcionalidades" className="py-20 bg-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center mb-16">
                <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                  Soluções Modernas
                </h2>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                  Tecnologia de ponta para processos 100% digitais e compliance garantido
                </p>
              </div>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div className="text-center p-6">
                  <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-blue-600 text-2xl">✓</span>
                  </div>
                  <h3 className="text-xl font-semibold mb-3">Precisão</h3>
                  <p className="text-gray-600">Segurança jurídica em todos os processos</p>
                </div>
                
                <div className="text-center p-6">
                  <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-green-600 text-2xl">⚡</span>
                  </div>
                  <h3 className="text-xl font-semibold mb-3">Eficiência</h3>
                  <p className="text-gray-600">Operacional e automatizada</p>
                </div>
                
                <div className="text-center p-6">
                  <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-purple-600 text-2xl">🛡️</span>
                  </div>
                  <h3 className="text-xl font-semibold mb-3">Compliance</h3>
                  <p className="text-gray-600">Trabalhista garantido</p>
                </div>
                
                <div className="text-center p-6">
                  <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-orange-600 text-2xl">💻</span>
                  </div>
                  <h3 className="text-xl font-semibold mb-3">Digital</h3>
                  <p className="text-gray-600">Processos 100% digitais</p>
                </div>
              </div>
            </div>
          </section>

          {/* CTA Section */}
          <section className="bg-gray-50 py-20">
            <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Pronto para modernizar seu Departamento Pessoal?
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Acesse nossa plataforma e descubra como podemos transformar seus processos
              </p>
              <Link 
                href="/login" 
                className="bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-lg"
              >
                Começar Agora
              </Link>
            </div>
          </section>
        </div>
      </Layout>
    </>
  )
}

export default HomePage