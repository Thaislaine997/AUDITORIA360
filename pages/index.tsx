import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";

const navigation = [
  { name: 'Quem Somos', href: '#quem-somos' },
  { name: 'Serviços', href: '#servicos' },
  { name: 'Planos', href: '#planos' },
  { name: 'FAQ', href: '#faq' },
  { name: 'Contato', href: '#contato' },
];

const scrollToSection = (id: string) => {
  if (typeof window !== 'undefined') {
    const el = document.querySelector(id);
    if (el) {
      const yOffset = -90;
      const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  }
};

const HomePage: NextPage = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      <Head>
        <title>DPEIXER - Auditoria, RH e DP sem complicação</title>
        <meta name="description" content="Especialistas em assessoria, terceirização de DP e RH, consultoria, treinamentos e serviços sob demanda. Portal AUDITORIA360: tecnologia, compliance e excelência para contabilidades e empresas." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      </Head>
      
      <div className="bg-gray-50 font-sans">
        {/* Header */}
        <header className="bg-white shadow-lg fixed w-full top-0 z-50">
          <nav className="container mx-auto px-6 py-4">
            <div className="flex justify-between items-center">
              <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                DPEIXER
              </div>
              <div className="hidden md:flex space-x-8">
                {navigation.map((item) => (
                  <button
                    key={item.name}
                    onClick={() => scrollToSection(item.href)}
                    className="text-gray-700 hover:text-purple-600 transition-colors duration-300 font-medium"
                  >
                    {item.name}
                  </button>
                ))}
              </div>
              <button 
                className="md:hidden"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              </button>
            </div>
          </nav>
        </header>

        {/* Hero Section */}
        <section className="bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-800 text-white pt-24 pb-20 relative overflow-hidden">
          <div className="absolute inset-0 bg-black opacity-10"></div>
          <div className="container mx-auto px-6 relative z-10">
            <div className="flex flex-col lg:flex-row items-center">
              <div className="lg:w-1/2 mb-12 lg:mb-0">
                <motion.div
                  initial={{ opacity: 0, y: 40 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8 }}
                  className="mb-6"
                >
                  <span className="bg-yellow-400 text-gray-900 px-4 py-2 rounded-full text-sm font-bold uppercase tracking-wide">
                    💻 Plataforma AUDITORIA360
                  </span>
                </motion.div>
                <motion.h1 
                  initial={{ opacity: 0, y: 40 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.2 }}
                  className="text-5xl lg:text-7xl font-black mb-6 leading-tight"
                >
                  <span className="text-yellow-300">Auditoria</span>, RH e DP<br/>
                  <span className="text-3xl lg:text-4xl font-semibold text-gray-200">sem complicação</span>
                </motion.h1>
                <motion.p 
                  initial={{ opacity: 0, y: 40 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.4 }}
                  className="text-xl mb-8 text-gray-100 leading-relaxed"
                >
                  Nosso maior diferencial: <strong>tecnologia própria</strong> para gestão e auditoria de RH e DP. 
                  Transforme sua gestão de pessoas com nossa plataforma exclusiva.
                </motion.p>
                <motion.div 
                  initial={{ opacity: 0, y: 40 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.6 }}
                  className="flex flex-col sm:flex-row gap-4"
                >
                  <button className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-xl font-bold hover:bg-yellow-300 transition-all transform hover:scale-105 shadow-lg hover:shadow-yellow-400/25">
                    📞 Entre em Contato
                  </button>
                  <button className="backdrop-blur-md bg-white/10 border border-white/20 text-white px-8 py-4 rounded-xl font-semibold hover:bg-white hover:text-gray-900 transition-all">
                    📞 (47) 93383-5427
                  </button>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, y: 40 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.8 }}
                  className="mt-8 flex items-center space-x-6 text-sm"
                >
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                    </svg>
                    SLA 30 minutos
                  </div>
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                    </svg>
                    LGPD Compliant
                  </div>
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                    </svg>
                    Todo Brasil
                  </div>
                </motion.div>
              </div>
              <div className="lg:w-1/2 flex justify-center">
                <motion.div 
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 1, delay: 0.4 }}
                  className="relative"
                >
                  <div className="w-96 h-96 relative">
                    {/* Dashboard mockup */}
                    <div className="absolute inset-0 bg-white rounded-3xl shadow-2xl p-6 transform rotate-3 hover:rotate-0 transition-transform duration-300">
                      <div className="h-full bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl p-4">
                        <div className="flex items-center justify-between mb-4">
                          <h3 className="text-gray-800 font-bold">AUDITORIA360</h3>
                          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                        </div>
                        <div className="space-y-3">
                          <div className="bg-white rounded-lg p-3 shadow-sm">
                            <div className="flex items-center justify-between">
                              <span className="text-sm text-gray-600">📊 Folha Processada</span>
                              <span className="text-green-600 font-bold">✓</span>
                            </div>
                          </div>
                          <div className="bg-white rounded-lg p-3 shadow-sm">
                            <div className="flex items-center justify-between">
                              <span className="text-sm text-gray-600">⚡ Automação Ativa</span>
                              <span className="text-blue-600 font-bold">90%</span>
                            </div>
                          </div>
                          <div className="bg-white rounded-lg p-3 shadow-sm">
                            <div className="flex items-center justify-between">
                              <span className="text-sm text-gray-600">🔒 Segurança LGPD</span>
                              <span className="text-purple-600 font-bold">100%</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    {/* Floating elements */}
                    <div className="absolute -top-4 -right-4 w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center text-2xl animate-bounce">
                      📈
                    </div>
                    <div className="absolute -bottom-4 -left-4 w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white animate-pulse">
                      ✓
                    </div>
                  </div>
                </motion.div>
              </div>
            </div>
          </div>
        </section>

        {/* AUDITORIA360 Platform */}
        <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
          <div className="container mx-auto px-6">
            <div className="text-center mb-16">
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="inline-flex items-center bg-blue-100 text-blue-800 px-6 py-3 rounded-full font-semibold mb-6"
              >
                💻 Plataforma AUDITORIA360
              </motion.div>
              <motion.h2 
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="text-5xl font-black text-gray-900 mb-6"
              >
                Nosso maior <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">diferencial</span>
              </motion.h2>
              <motion.p 
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="text-xl text-gray-600 max-w-4xl mx-auto"
              >
                Tecnologia própria para gestão e auditoria de RH e DP com impacto comprovado
              </motion.p>
            </div>
            
            {/* Platform Features Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
              {[
                { icon: "📊", title: "Dashboards em Tempo Real", desc: "KPIs de folha, admissões, rescisões e afastamentos", color: "blue" },
                { icon: "✅", title: "Alertas Automáticos", desc: "Prazos, obrigações e riscos trabalhistas", color: "green" },
                { icon: "🔒", title: "Segurança Total", desc: "LGPD com criptografia avançada", color: "purple" },
                { icon: "📂", title: "Histórico Digital", desc: "Armazenamento em nuvem seguro", color: "orange" }
              ].map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className={`bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border-l-4 ${
                    feature.color === 'blue' ? 'border-blue-500' :
                    feature.color === 'green' ? 'border-green-500' :
                    feature.color === 'purple' ? 'border-purple-500' :
                    'border-orange-500'
                  }`}
                >
                  <div className="text-3xl mb-4">{feature.icon}</div>
                  <h3 className="font-bold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-gray-600 text-sm">{feature.desc}</p>
                </motion.div>
              ))}
            </div>

            {/* Additional Features */}
            <div className="grid md:grid-cols-2 gap-8">
              <motion.div
                initial={{ opacity: 0, x: -40 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center mb-6">
                  <span className="text-white text-xl">📥</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Upload Inteligente</h3>
                <p className="text-gray-600">Documentos com versionamento automático e organização inteligente</p>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: 40 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center mb-6">
                  <span className="text-white text-xl">⚡</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Automação Total</h3>
                <p className="text-gray-600">Tarefas repetitivas automatizadas: envio de obrigações, relatórios</p>
              </motion.div>
            </div>
          </div>
        </section>

        {/* About Company */}
        <section id="quem-somos" className="py-20 bg-white">
          <div className="container mx-auto px-6">
            <div className="text-center mb-16">
              <motion.h2
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="text-4xl font-bold text-gray-900 mb-4"
              >
                Quem Somos
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="text-xl text-gray-600 max-w-4xl mx-auto mb-8"
              >
                A DPEIXER Assessoria & Terceirização nasceu para transformar a forma como empresas e escritórios contábeis administram Recursos Humanos (RH), Departamento Pessoal (DP) e Obrigações Trabalhistas.
              </motion.p>
              <motion.p
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="text-lg text-gray-600 max-w-4xl mx-auto"
              >
                Nosso compromisso é ir além do operacional: atuamos como parceiros estratégicos, que unem experiência técnica, tecnologia própria e atendimento humanizado para garantir segurança jurídica, eficiência de processos e redução de custos.
              </motion.p>
            </div>
            <div className="grid md:grid-cols-3 gap-8 mb-20">
              {[
                { title: "Missão", desc: "Simplificar e organizar os processos de gestão de pessoas com tecnologia e excelência.", color: "blue", icon: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" },
                { title: "Valores", desc: "Ética, transparência, inovação, parceria, segurança e foco total no cliente.", color: "green", icon: "M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" },
                { title: "Visão", desc: "Ser a maior referência em terceirização de RH e DP no Brasil com foco em inovação.", color: "purple", icon: "M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" }
              ].map((item, index) => (
                <motion.div
                  key={item.title}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  className={`text-center p-8 rounded-2xl bg-gradient-to-br ${
                    item.color === 'blue' ? 'from-blue-50 to-purple-50' :
                    item.color === 'green' ? 'from-green-50 to-blue-50' :
                    'from-purple-50 to-pink-50'
                  } hover:shadow-xl transition-all duration-300 hover:-translate-y-2`}
                >
                  <div className={`w-16 h-16 ${
                    item.color === 'blue' ? 'bg-blue-500' :
                    item.color === 'green' ? 'bg-green-500' :
                    'bg-purple-500'
                  } rounded-full flex items-center justify-center mx-auto mb-6`}>
                    <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d={item.icon}/>
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">{item.title}</h3>
                  <p className="text-gray-600">{item.desc}</p>
                </motion.div>
              ))}
            </div>
            
            {/* Experience Highlights */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl p-8 text-white"
            >
              <div className="grid md:grid-cols-4 gap-6 text-center">
                <div>
                  <div className="text-3xl font-bold mb-2">8+</div>
                  <p className="text-blue-100">Anos de experiência acumulada em RH e DP</p>
                </div>
                <div>
                  <div className="text-3xl font-bold mb-2">100%</div>
                  <p className="text-blue-100">Processos digitais e adequados à LGPD</p>
                </div>
                <div>
                  <div className="text-3xl font-bold mb-2">30%</div>
                  <p className="text-blue-100">Redução média nos custos de RH</p>
                </div>
                <div>
                  <div className="text-3xl font-bold mb-2">24/7</div>
                  <p className="text-blue-100">Portal do empregado para autoatendimento</p>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Services */}
        <section id="servicos" className="py-20 bg-gray-50">
          <div className="container mx-auto px-6">
            <div className="text-center mb-16">
              <motion.h2
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="text-4xl font-bold text-gray-900 mb-4"
              >
                Nossos Serviços
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="text-xl text-gray-600 max-w-3xl mx-auto"
              >
                Soluções completas em gestão de pessoas, departamento pessoal e consultoria trabalhista 
                com tecnologia proprietária e atendimento especializado.
              </motion.p>
            </div>
            <div className="grid md:grid-cols-2 gap-8">
              {[
                {
                  title: "BPO de Recursos Humanos",
                  desc: "Transformamos o RH em um núcleo estratégico, eliminando tarefas manuais e trazendo inteligência.",
                  gradient: "from-blue-500 to-purple-600",
                  features: [
                    "Admissões e rescisões digitais com assinatura eletrônica",
                    "Gestão completa de ponto eletrônico e escalas",
                    "Administração de benefícios corporativos",
                    "Portal do empregado para autoatendimento 24/7",
                    "Relatórios e indicadores (People Analytics)"
                  ],
                  benefit: "Redução de 30% nos custos de RH",
                  benefitColor: "blue"
                },
                {
                  title: "Departamento Pessoal Terceirizado",
                  desc: "O DP é o coração das obrigações legais da sua empresa. Nós cuidamos de tudo com precisão e conformidade.",
                  gradient: "from-green-500 to-blue-600",
                  features: [
                    "Cálculo e processamento da folha de pagamento",
                    "Emissão de guias e encargos (INSS, FGTS, IRRF)",
                    "Envio e validação no eSocial, DCTFWeb e FGTS Digital",
                    "Auditoria de processos para identificar riscos",
                    "SLA de atendimento: resposta em até 30 minutos"
                  ],
                  benefit: "Redução de passivos trabalhistas",
                  benefitColor: "green"
                }
              ].map((service, index) => (
                <motion.div
                  key={service.title}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
                >
                  <div className={`w-12 h-12 bg-gradient-to-r ${service.gradient} rounded-lg flex items-center justify-center mb-6`}>
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d={index === 0 ? "M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z" : "M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"}/>
                      {index === 1 && <path fillRule="evenodd" d="M4 5a2 2 0 012-2v1a2 2 0 002 2h8a2 2 0 002-2V3a2 2 0 012 2v6h-3a3 3 0 00-3 3v4a1 1 0 01-1 1H6a2 2 0 01-2-2V5zm8 8a3 3 0 013-3h3v4a2 2 0 01-2 2h-4v-3z"/>}
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">{service.title}</h3>
                  <p className="text-gray-600 mb-6">{service.desc}</p>
                  <ul className="space-y-3 text-gray-600 mb-6">
                    {service.features.map((feature, fIndex) => (
                      <li key={fIndex} className="flex items-start">
                        <svg className="w-5 h-5 text-green-500 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                        </svg>
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <div className={`p-4 ${service.benefitColor === 'blue' ? 'bg-blue-50' : 'bg-green-50'} rounded-lg`}>
                    <p className={`text-sm ${service.benefitColor === 'blue' ? 'text-blue-800' : 'text-green-800'} font-semibold`}>
                      Benefícios: {service.benefit}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section id="faq" className="py-20 bg-white">
          <div className="container mx-auto px-6">
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl font-bold text-gray-900 mb-4">Perguntas Frequentes</h2>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-8"
            >
              {[
                {
                  q: "O que está incluso na terceirização da folha?",
                  a: "Processamento completo da folha, encargos, obrigações acessórias, admissão, rescisão, férias, relatórios, atendimento e acesso à plataforma AUDITORIA360."
                },
                {
                  q: "Como é feito o atendimento?",
                  a: "Atendimento consultivo, humanizado e multicanal (telefone, e-mail, portal e WhatsApp), com SLA definido e especialistas dedicados."
                },
                {
                  q: "A DPEIXER atende empresas de qualquer porte?",
                  a: "Sim! Atendemos desde pequenas empresas até grandes grupos, inclusive contabilidades e escritórios de BPO."
                }
              ].map((faq, index) => (
                <div key={index} className="mb-6 last:mb-0">
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{faq.q}</h3>
                  <p className="text-gray-600">{faq.a}</p>
                  {index < 2 && <hr className="my-6 border-gray-200" />}
                </div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* CTA Final */}
        <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20 text-center">
          <div className="container mx-auto px-6">
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-4xl font-bold mb-4">Pronto para transformar o RH da sua empresa?</h2>
              <p className="text-xl mb-8 opacity-90">Entre em contato conosco e descubra como podemos ajudar</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-xl font-bold hover:bg-yellow-300 transition-all transform hover:scale-105">
                  📞 Fale Conosco
                </button>
                <button className="border-2 border-white text-white px-8 py-4 rounded-xl font-bold hover:bg-white hover:text-blue-600 transition-all">
                  📧 Solicitar Proposta
                </button>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Footer */}
        <footer id="contato" className="bg-gray-900 text-white py-16">
          <div className="container mx-auto px-6">
            <div className="grid md:grid-cols-3 gap-8">
              <div>
                <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
                  DPEIXER
                </h3>
                <p className="text-gray-400 mb-4">
                  Transformando a gestão de RH e DP com tecnologia e excelência.
                </p>
                <div className="flex space-x-4">
                  <a href="#" className="bg-blue-600 p-3 rounded-full hover:bg-blue-700 transition-colors">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"/>
                    </svg>
                  </a>
                  <a href="#" className="bg-blue-600 p-3 rounded-full hover:bg-blue-700 transition-colors">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                    </svg>
                  </a>
                </div>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-4">Contato</h4>
                <div className="space-y-2 text-gray-400">
                  <p>📞 (47) 93383-5427</p>
                  <p>📧 contato@dpeixer.com.br</p>
                  <p>📍 Santa Catarina, Brasil</p>
                </div>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-4">Links Rápidos</h4>
                <div className="space-y-2">
                  {navigation.map((item) => (
                    <button
                      key={item.name}
                      onClick={() => scrollToSection(item.href)}
                      className="block text-gray-400 hover:text-white transition-colors"
                    >
                      {item.name}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            <hr className="border-gray-800 my-8" />
            <div className="text-center text-gray-400">
              <p>&copy; 2024 DPEIXER Assessoria & Terceirização. Todos os direitos reservados.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};

export default HomePage;