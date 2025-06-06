\
import uuid
from datetime import datetime, timezone
import logging
from typing import Dict, Any, List

# Configuração básica do logger (idealmente, isso viria de uma configuração centralizada)
logger = logging.getLogger(__name__)
# Adicionar um handler se não houver um configurado (ex: para testes locais)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class MotorCalculoFolhaService:
    """
    Serviço responsável pelo cálculo da folha de pagamento (INSS, IRRF, FGTS, etc.)
    de acordo com as regras da AUDITORIA360.
    """

    def __init__(self, client_id: str, config_manager: Any = None):
        """
        Inicializa o serviço do motor de cálculo.

        Args:
            client_id (str): Identificador do cliente.
            config_manager (Any, optional): Gerenciador de configurações para buscar
                                             parâmetros específicos do cliente, se necessário.
                                             Pode ser expandido para buscar tabelas legais, etc.
        """
        self.client_id = client_id
        self.config_manager = config_manager
        self.tabelas_legais_cache: Dict[str, Dict[str, Any]] = {} # Adicionado cache
        # O logger pode ser prefixado com client_id se desejado, ou usar o client_id nas mensagens
        self.logger = logging.getLogger(f"{__name__}.{self.client_id}")
        if not self.logger.handlers: # Garante que o logger específico da instância também tenha handlers
            handler = logging.StreamHandler()
            formatter = logging.Formatter(f'%(asctime)s - %(name)s (Client: {self.client_id}) - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _carregar_tabelas_legais(self, competencia_folha: str) -> Dict[str, Any]:
        """
        Carrega as tabelas legais e parâmetros para uma dada competência.
        Atualmente, retorna dados de exemplo. No futuro, buscará do Módulo 1/Configurações (BigQuery/Firestore).

        Args:
            competencia_folha: A competência da folha no formato "YYYY-MM".

        Returns:
            Um dicionário contendo as tabelas legais (INSS, IRRF, Salário Família)
            e outros parâmetros gerais (Salário Mínimo, alíquota FGTS).
        """
        self.logger.info(f"Carregando tabelas legais para competência: {competencia_folha}")

        # --- Dados de Exemplo - Substituir pela lógica de carregamento real ---
        # Estes valores são exemplos e podem não refletir a legislação atual ou todas as complexidades.
        # A estrutura deve ser consistente com o que o método de cálculo espera.

        tabelas = {
            "inss": {
                "teto": 7786.02,  # Exemplo de teto INSS (Maio/2023 em diante)
                "faixas": [
                    {"limite_faixa": 1412.00, "aliquota": 0.075, "parcela_a_deduzir": 0.0},
                    {"limite_faixa": 2666.68, "aliquota": 0.09, "parcela_a_deduzir": 21.18},
                    {"limite_faixa": 4000.03, "aliquota": 0.12, "parcela_a_deduzir": 101.18},
                    {"limite_faixa": 7786.02, "aliquota": 0.14, "parcela_a_deduzir": 181.18}
                    # Para bases acima do teto, a contribuição é sobre o teto.
                    # A lógica de cálculo já trata o teto separadamente para o valor da contribuição,
                    # mas a alíquota efetiva pode ser calculada sobre a base original.
                ]
            },
            "irrf": {
                # Exemplo baseado na tabela de Maio/2023 a Jan/2024
                "deducao_por_dependente": 189.59,
                "limite_desconto_simplificado": 564.80, # 25% de 2.259,20 (limite da 1a faixa de isenção)
                                                       # A partir de Fev/2024, o desconto simplificado é de R$ 528,00 (25% de R$ 2.112,00)
                                                       # E a tabela progressiva também muda.
                                                       # Para Fev/2024 em diante (MP 1.206/2024):
                                                       # Faixa 1: Até 2.259,20 (isenção com novo desconto simplificado de 528)
                                                       # Faixa 1: Até 2.112,00 (Isento)
                                                       # Faixa 2: De 2.112.01 até 2.826,65 (7.5%, dedução 158,40)
                                                       # ... etc.
                                                       # Este exemplo usa uma tabela genérica, precisaria ser atualizada pela competência.
                "faixas": [
                    {"base_calculo_inicial": 0.0, "base_calculo_final": 2259.20, "aliquota": 0.0, "parcela_a_deduzir": 0.0}, # Isento (considerando tabela de Maio/2023)
                    {"base_calculo_inicial": 2259.21, "base_calculo_final": 2826.65, "aliquota": 0.075, "parcela_a_deduzir": 169.44},
                    {"base_calculo_inicial": 2826.66, "base_calculo_final": 3751.05, "aliquota": 0.15, "parcela_a_deduzir": 381.44},
                    {"base_calculo_inicial": 3751.06, "base_calculo_final": 4664.68, "aliquota": 0.225, "parcela_a_deduzir": 662.77},
                    {"base_calculo_inicial": 4664.69, "base_calculo_final": float('inf'), "aliquota": 0.275, "parcela_a_deduzir": 896.00}
                ]
            },
            "salario_familia": {
                # Exemplo para 2024 (Portaria Interministerial MPS/MF Nº 2, de 11/01/2024)
                "limite_renda": 1819.26, # Renda bruta mensal
                "valor_por_dependente": 62.04
            },
            "adicionais": {
                "periculosidade": {
                    "percentual": 0.30 # 30% sobre o salário base (ou conforme CCT)
                },
                "insalubridade": { # Valores e base conforme NR-15 e Portarias. Salário Mínimo como referência comum.
                    "grau_minimo": {"percentual": 0.10, "base_calculo_tipo": "salario_minimo_nacional"}, # 10%
                    "grau_medio": {"percentual": 0.20, "base_calculo_tipo": "salario_minimo_nacional"},  # 20%
                    "grau_maximo": {"percentual": 0.40, "base_calculo_tipo": "salario_minimo_nacional"} # 40%
                },
                "adicional_noturno": {
                    "percentual_urbano": 0.20, # 20% para trabalhadores urbanos
                    "percentual_rural_lavoura": 0.25, # 25% para trabalhadores rurais na lavoura
                    "percentual_rural_pecuaria": 0.25, # 25% para trabalhadores rurais na pecuária (pode variar)
                    "considerar_hora_reduzida_urbano": True, # Hora noturna de 52min30s para urbanos
                    "fator_hora_noturna_reduzida_urbano": 1.14285714 # 60 / 52.5
                }
            },
            "dsr": {
                # Fórmula comum: (Soma das Verbas Variáveis / Dias Úteis no Mês) * (Domingos + Feriados no Mês)
                # Estes dias virão dos parâmetros gerais da folha.
                "calculo_habilitado": True 
            },
            "incidencias_rubricas_motor": {
                # Define as incidências padrão para rubricas calculadas internamente pelo motor.
                # 'dsr_base': True indica que esta rubrica entra na base de cálculo do DSR.
                "MOTOR_PERIC": {"inss": True, "irrf": True, "fgts": True, "dsr_base": False, "nome": "Periculosidade (Calculada)"},
                "MOTOR_INSAL": {"inss": True, "irrf": True, "fgts": True, "dsr_base": False, "nome": "Insalubridade (Calculada)"},
                "MOTOR_ADNOT": {"inss": True, "irrf": True, "fgts": True, "dsr_base": True, "nome": "Adicional Noturno (Calculado)"},
                "MOTOR_DSR": {"inss": True, "irrf": True, "fgts": True, "dsr_base": False, "nome": "DSR (Calculado)"}
            },
            "parametros_gerais": {
                "salario_minimo_nacional": 1412.00, # Exemplo para 2024
                "aliquota_fgts_padrao": 0.08, # 8%
                "aliquota_fgts_aprendiz": 0.02, # 2%
                # Outros parâmetros podem ser adicionados aqui
            }
        }
        
        # Lógica para ajustar tabelas com base na competencia_folha (ex: if competencia_folha >= "2024-02": ...)
        if competencia_folha >= "2024-02":
            self.logger.info(f"Aplicando tabelas IRRF para Fev/2024 em diante para competência {competencia_folha}")
            tabelas["irrf"]["limite_desconto_simplificado"] = 528.00 # Valor do desconto simplificado opcional (MP 1.206/2024)
            tabelas["irrf"]["faixas"] = [
                {"base_calculo_inicial": 0.0, "base_calculo_final": 2112.00, "aliquota": 0.0, "parcela_a_deduzir": 0.0},
                {"base_calculo_inicial": 2112.01, "base_calculo_final": 2826.65, "aliquota": 0.075, "parcela_a_deduzir": 158.40},
                {"base_calculo_inicial": 2826.66, "base_calculo_final": 3751.05, "aliquota": 0.15, "parcela_a_deduzir": 370.40},
                {"base_calculo_inicial": 3751.06, "base_calculo_final": 4664.68, "aliquota": 0.225, "parcela_a_deduzir": 651.73},
                {"base_calculo_inicial": 4664.69, "base_calculo_final": float('inf'), "aliquota": 0.275, "parcela_a_deduzir": 884.96}
            ]
            # O teto do INSS e Salário Família também podem mudar anualmente.
            # Para simplificar, este exemplo não ajusta INSS/SF por competência, mas deveria.
            # Ex: Tabela INSS 2024 (Portaria Interministerial MPS/MF Nº 2/2024)
            # Faixa 1: Até 1.412,00 -> 7,5%
            # Faixa 2: De 1.412,01 até 2.666,68 -> 9%
            # Faixa 3: De 2.666,69 até 4.000,03 -> 12%
            # Faixa 4: De 4.000,04 até 7.786,02 -> 14% (Teto)
            # As parcelas a deduzir também mudam.
            # Este exemplo de INSS já está alinhado com 2024.

        self.logger.debug(f"Tabelas carregadas para {competencia_folha}: {tabelas}")
        self.tabelas_legais_cache[competencia_folha] = tabelas # Armazena no cache
        return tabelas

    def get_tabelas_legais(self, competencia_folha: str) -> Dict[str, Any]:
        """
        Retorna as tabelas legais para a competência especificada,
        utilizando o cache interno ou carregando-as se necessário.
        """
        if competencia_folha in self.tabelas_legais_cache:
            self.logger.info(f"Retornando tabelas legais do cache para competência: {competencia_folha}")
            return self.tabelas_legais_cache[competencia_folha]
        return self._carregar_tabelas_legais(competencia_folha)

    def calcular_folha_funcionario_audit360(
        self,
        id_funcionario: str,
        dados_funcionario_folha: Dict[str, Any], # Dados da folha do funcionário (rubricas, cadastro)
        rubricas_config: Dict[str, Dict[str, Any]], # Configurações de incidência das rubricas do cliente
        tabelas_legais: Dict[str, Any], # Tabelas de INSS, IRRF, Salário Família, etc.
        parametros_gerais: Dict[str, Any] # Parâmetros como dias úteis, feriados, etc.
    ) -> Dict[str, Any]:
        """
        Calcula os encargos da folha (INSS, IRRF, FGTS) e outras verbas dependentes
        para um funcionário específico, com base nos parâmetros do sistema e
        configurações de rubricas.

        A ordem de cálculo foi reestruturada para maior precisão:
        1. Cálculo de Adicionais (Periculosidade, Insalubridade, Ad. Noturno).
        2. Cálculo de DSR.
        3. Consolidação de todas as verbas (originais + calculadas) e formação das bases finais.
        4. Cálculo dos Encargos (INSS, IRRF, FGTS) e Salário Família.
        """
        logger.info(f"[{self.client_id}] Iniciando cálculo da folha para funcionário: {id_funcionario}, Competência: {parametros_gerais.get('competencia_folha')}")
        logger.debug(f"[{self.client_id}] Dados do funcionário: {dados_funcionario_folha}")
        logger.debug(f"[{self.client_id}] Configurações de rubricas: {rubricas_config}")
        logger.debug(f"[{self.client_id}] Tabelas Legais: {tabelas_legais}")
        logger.debug(f"[{self.client_id}] Parâmetros Gerais: {parametros_gerais}")

        resultados = {
            "id_funcionario": id_funcionario,
            "competencia_folha": parametros_gerais.get("competencia_folha"),
            "base_calculo_inss_sistema": 0.0,
            "valor_inss_calculado_sistema": 0.0,
            "aliquota_efetiva_inss_sistema": 0.0,
            "base_calculo_irrf_bruta_sistema": 0.0, # Base antes de deduções legais (INSS, dependentes, etc)
            "base_calculo_irrf_liquida_sistema": 0.0, # Base após deduções legais
            "valor_irrf_calculado_sistema": 0.0,
            "base_calculo_fgts_sistema": 0.0,
            "valor_fgts_calculado_sistema": 0.0,
            "salario_familia_calculado_sistema": 0.0,
            "valor_periculosidade_calculado_sistema": 0.0,
            "valor_insalubridade_calculado_sistema": 0.0,
            "valor_adicional_noturno_calculado_sistema": 0.0,
            "valor_dsr_calculado_sistema": 0.0,
            "outras_verbas_calculadas_motor": {}, # Para armazenar valores de rubricas calculadas pelo motor
            "data_calculo": datetime.now(timezone.utc).isoformat(),
            "logs_calculo": [] # Para registrar etapas importantes ou alertas
        }

        # Estrutura para armazenar todas as verbas (originais da folha + calculadas pelo motor)
        # Cada item será um dict: {"codigo": str, "valor": float, "tipo": "V"|"D", "descricao": str, "origem": "folha"|"motor"}
        verbas_consolidadas_para_bases = []

        # Adiciona rubricas originais da folha do funcionário à lista consolidada
        for rubrica_item in dados_funcionario_folha.get("rubricas_folha", []):
            verbas_consolidadas_para_bases.append({
                "codigo": rubrica_item.get("codigo"),
                "valor": float(rubrica_item.get("valor", 0.0) or 0.0),
                "tipo": rubrica_item.get("tipo", "V").upper() # Vencimento ou Desconto
            })

        # --- PASSO 1: Cálculo de Adicionais (Periculosidade, Insalubridade, Ad. Noturno) ---
        # Estes valores serão adicionados a `verbas_consolidadas_para_bases` se calculados.
        
        # 1.1 Adicional de Periculosidade
        if dados_funcionario_folha.get("recebe_periculosidade", False):
            salario_base_para_periculosidade = 0.0
            codigo_rubrica_salario_base = parametros_gerais.get("codigo_rubrica_salario_base_periculosidade", "SALARIO_BASE") 
            # Tentar encontrar o salário base nas rubricas já existentes
            for rubrica_folha in verbas_consolidadas_para_bases:
                if rubrica_folha["codigo"] == codigo_rubrica_salario_base and rubrica_folha["tipo"] == "V":
                    salario_base_para_periculosidade = rubrica_folha["valor"]
                    break
            # Se não encontrou, e houver um campo específico nos dados do funcionário:
            if salario_base_para_periculosidade == 0.0 and dados_funcionario_folha.get("salario_base_contratual"): 
                salario_base_para_periculosidade = float(dados_funcionario_folha.get("salario_base_contratual", 0.0))

            percentual_periculosidade = tabelas_legais.get("adicionais", {}).get("periculosidade", {}).get("percentual", 0.30)
            if salario_base_para_periculosidade > 0:
                valor_periculosidade = round(salario_base_para_periculosidade * percentual_periculosidade, 2)
                resultados["valor_periculosidade_calculado_sistema"] = valor_periculosidade
                verbas_consolidadas_para_bases.append({
                    "codigo": "MOTOR_PERIC", 
                    "valor": valor_periculosidade, 
                    "tipo": "V", 
                    "descricao": tabelas_legais.get("incidencias_rubricas_motor",{}).get("MOTOR_PERIC",{}).get("nome","Periculosidade (Calculada)"),
                    "origem": "motor"
                })
                logger.info(f"[{self.client_id}] Adicional de Periculosidade calculado: {valor_periculosidade:.2f}")
            else:
                logger.warning(f"[{self.client_id}] Periculosidade não calculada: Salário base para periculosidade não encontrado ou zerado (código esperado: {codigo_rubrica_salario_base}).")
                resultados["logs_calculo"].append(f"ALERTA: Periculosidade não calculada - salário base não encontrado (código: {codigo_rubrica_salario_base})")

        # 1.2 Adicional de Insalubridade
        grau_insalubridade = dados_funcionario_folha.get("grau_insalubridade") # ex: "minimo", "medio", "maximo"
        if grau_insalubridade:
            config_grau_insal = tabelas_legais.get("adicionais", {}).get("insalubridade", {}).get(grau_insalubridade)
            if config_grau_insal:
                percentual_insalubridade = config_grau_insal.get("percentual")
                base_calculo_tipo = config_grau_insal.get("base_calculo_tipo", "salario_minimo_nacional")
                base_valor_insalubridade = 0.0
                if base_calculo_tipo == "salario_minimo_nacional":
                    base_valor_insalubridade = tabelas_legais.get("parametros_gerais", {}).get("salario_minimo_nacional", 0.0)
                elif base_calculo_tipo == "salario_base_funcionario":
                     # Similar à periculosidade, buscar o salário base
                    codigo_rubrica_salario_base_insal = parametros_gerais.get("codigo_rubrica_salario_base_insalubridade", "SALARIO_BASE")
                    for rubrica_folha in verbas_consolidadas_para_bases:
                        if rubrica_folha["codigo"] == codigo_rubrica_salario_base_insal and rubrica_folha["tipo"] == "V":
                            base_valor_insalubridade = rubrica_folha["valor"]
                            break
                    if base_valor_insalubridade == 0.0 and dados_funcionario_folha.get("salario_base_contratual"): 
                        base_valor_insalubridade = float(dados_funcionario_folha.get("salario_base_contratual", 0.0))
                # Adicionar lógica para outras bases (ex: salário normativo da CCT)

                if base_valor_insalubridade > 0 and percentual_insalubridade and percentual_insalubridade > 0:
                    valor_insalubridade = round(base_valor_insalubridade * percentual_insalubridade, 2)
                    resultados["valor_insalubridade_calculado_sistema"] = valor_insalubridade
                    verbas_consolidadas_para_bases.append({
                        "codigo": "MOTOR_INSAL", 
                        "valor": valor_insalubridade, 
                        "tipo": "V", 
                        "descricao": tabelas_legais.get("incidencias_rubricas_motor",{}).get("MOTOR_INSAL",{}).get("nome","Insalubridade (Calculada)"),
                        "origem": "motor"
                    })
                    logger.info(f"[{self.client_id}] Adicional de Insalubridade ({grau_insalubridade}) calculado: {valor_insalubridade:.2f}")
                else:
                    logger.warning(f"[{self.client_id}] Insalubridade ({grau_insalubridade}) não calculada: Base ({base_calculo_tipo} = {base_valor_insalubridade:.2f}) ou percentual ({percentual_insalubridade}) inválidos.")
                    resultados["logs_calculo"].append(f"ALERTA: Insalubridade ({grau_insalubridade}) não calculada - base ou percentual inválido.")
            else:
                logger.warning(f"[{self.client_id}] Configuração para grau de insalubridade '{grau_insalubridade}' não encontrada.")
                resultados["logs_calculo"].append(f"ALERTA: Grau de insalubridade '{grau_insalubridade}' não configurado.")

        # 1.3 Adicional Noturno
        horas_noturnas_trabalhadas = float(dados_funcionario_folha.get("horas_noturnas_trabalhadas", 0.0))
        if horas_noturnas_trabalhadas > 0:
            valor_hora_normal = float(dados_funcionario_folha.get("valor_hora_normal", 0.0))
            if valor_hora_normal == 0.0: # Tenta calcular se não informado
                salario_base_an = 0.0
                horas_contratuais_mes = float(dados_funcionario_folha.get("horas_contratuais_mensais", parametros_gerais.get("horas_contratuais_padrao_mes", 220.0)))
                codigo_rubrica_salario_base_an = parametros_gerais.get("codigo_rubrica_salario_base_ad_noturno", "SALARIO_BASE")
                for rubrica_folha in verbas_consolidadas_para_bases:
                    if rubrica_folha["codigo"] == codigo_rubrica_salario_base_an and rubrica_folha["tipo"] == "V":
                        salario_base_an = rubrica_folha["valor"]
                        break
                if salario_base_an == 0.0 and dados_funcionario_folha.get("salario_base_contratual"): 
                    salario_base_an = float(dados_funcionario_folha.get("salario_base_contratual", 0.0))
                
                if salario_base_an > 0 and horas_contratuais_mes > 0:
                    valor_hora_normal = salario_base_an / horas_contratuais_mes
            
            if valor_hora_normal > 0:
                config_ad_noturno = tabelas_legais.get("adicionais", {}).get("adicional_noturno", {})
                # TODO: Determinar tipo de trabalhador (urbano/rural) para percentual e hora reduzida corretos
                percentual_ad_noturno = config_ad_noturno.get("percentual_urbano", 0.20) 
                fator_reducao_hora_noturna = 1.0
                if config_ad_noturno.get("considerar_hora_reduzida_urbano", False): # Exemplo para urbano
                    fator_reducao_hora_noturna = config_ad_noturno.get("fator_hora_noturna_reduzida_urbano", 1.14285714)
                
                # Adicional por hora = valor_hora_normal * percentual_ad_noturno
                # Valor total = Adicional por hora * horas_noturnas_trabalhadas * fator_reducao_hora_noturna (se hora noturna é paga como mais longa)
                valor_total_ad_noturno = round((valor_hora_normal * percentual_ad_noturno) * horas_noturnas_trabalhadas * fator_reducao_hora_noturna, 2)
                
                resultados["valor_adicional_noturno_calculado_sistema"] = valor_total_ad_noturno
                verbas_consolidadas_para_bases.append({
                    "codigo": "MOTOR_ADNOT", 
                    "valor": valor_total_ad_noturno, 
                    "tipo": "V", 
                    "descricao": tabelas_legais.get("incidencias_rubricas_motor",{}).get("MOTOR_ADNOT",{}).get("nome","Adicional Noturno (Calculado)"),
                    "origem": "motor"
                })
                logger.info(f"[{self.client_id}] Adicional Noturno calculado: {valor_total_ad_noturno:.2f} (Valor Hora: {valor_hora_normal:.2f}, Horas Noturnas: {horas_noturnas_trabalhadas}, Fator Red.: {fator_reducao_hora_noturna})")
            else:
                logger.warning(f"[{self.client_id}] Adicional Noturno não calculado: Valor da hora normal zerado ou não pôde ser determinado.")
                resultados["logs_calculo"].append("ALERTA: Adicional Noturno não calculado - valor hora normal zerado.")

        # --- PASSO 2: Calcular DSR (Descanso Semanal Remunerado) ---
        if tabelas_legais.get("dsr", {}).get("calculo_habilitado", False):
            soma_verbas_base_dsr = 0.0
            # Itera sobre as verbas consolidadas (originais + adicionais já calculados pelo motor)
            for verba in verbas_consolidadas_para_bases:
                config_incidencia_verba = None
                if verba["origem"] == "folha":
                    config_incidencia_verba = rubricas_config.get(verba["codigo"])
                elif verba["origem"] == "motor":
                    config_incidencia_verba = tabelas_legais.get("incidencias_rubricas_motor", {}).get(verba["codigo"])
                
                if config_incidencia_verba and config_incidencia_verba.get("dsr_base", False) and verba["tipo"] == "V":
                    soma_verbas_base_dsr += verba["valor"]
            
            dias_uteis = parametros_gerais.get("dias_uteis_mes")
            domingos_feriados = parametros_gerais.get("domingos_feriados_mes")

            if soma_verbas_base_dsr > 0 and dias_uteis and domingos_feriados and dias_uteis > 0:
                valor_dsr = round((soma_verbas_base_dsr / dias_uteis) * domingos_feriados, 2)
                resultados["valor_dsr_calculado_sistema"] = valor_dsr
                verbas_consolidadas_para_bases.append({
                    "codigo": "MOTOR_DSR", 
                    "valor": valor_dsr, 
                    "tipo": "V", 
                    "descricao": tabelas_legais.get("incidencias_rubricas_motor",{}).get("MOTOR_DSR",{}).get("nome","DSR (Calculado)"),
                    "origem": "motor"
                })
                logger.info(f"[{self.client_id}] DSR calculado: {valor_dsr:.2f} (Base DSR: {soma_verbas_base_dsr:.2f}, Dias Úteis: {dias_uteis}, Domingos/Feriados: {domingos_feriados})")
            elif soma_verbas_base_dsr > 0:
                logger.warning(f"[{self.client_id}] DSR não calculado: Dias úteis ({dias_uteis}) ou domingos/feriados ({domingos_feriados}) inválidos, mas base DSR era {soma_verbas_base_dsr:.2f}.")
                resultados["logs_calculo"].append(f"ALERTA: DSR não calculado - dias úteis/feriados inválidos (Base DSR: {soma_verbas_base_dsr:.2f})")
        
        # --- PASSO 3: Consolidação de Todas as Verbas e Formação das Bases de Cálculo Finais ---
        base_inss_temp = 0.0
        base_fgts_temp = 0.0
        base_irrf_bruta_temp = 0.0

        logger.debug(f"[{self.client_id}] Verbas consolidadas para cálculo das bases: {verbas_consolidadas_para_bases}")

        for verba in verbas_consolidadas_para_bases:
            codigo_verba = verba["codigo"]
            valor_verba = verba["valor"]
            tipo_verba = verba["tipo"]
            origem_verba = verba["origem"]

            config_incidencia = None
            if origem_verba == "folha":
                config_incidencia = rubricas_config.get(codigo_verba)
            elif origem_verba == "motor": # Rubricas calculadas pelo motor (PERIC, INSAL, ADNOT, DSR)
                config_incidencia = tabelas_legais.get("incidencias_rubricas_motor", {}).get(codigo_verba)

            if not config_incidencia:
                logger.warning(f"[{self.client_id}] Configuração de incidência não encontrada para rubrica '{codigo_verba}' (origem: {origem_verba}). Esta rubrica não será considerada nas bases.")
                resultados["logs_calculo"].append(f"ALERTA: Incidência não encontrada para rubrica '{codigo_verba}'. Não compôs bases.")
                continue

            # Considerar apenas VENCIMENTOS para somar nas bases, DESCONTOS não entram como base positiva.
            # Descontos podem ser relevantes para o líquido, mas não para base de INSS/IRRF/FGTS.
            if tipo_verba == "V":
                if config_incidencia.get("inss", False) or config_incidencia.get("incide_inss_empregado", False): # Compatibilidade com schema antigo
                    base_inss_temp += valor_verba
                if config_incidencia.get("irrf", False) or config_incidencia.get("incide_irrf", False):
                    base_irrf_bruta_temp += valor_verba
                if config_incidencia.get("fgts", False) or config_incidencia.get("incide_fgts_mensal", False):
                    base_fgts_temp += valor_verba
        
        resultados["base_calculo_inss_sistema"] = round(base_inss_temp, 2)
        resultados["base_calculo_irrf_bruta_sistema"] = round(base_irrf_bruta_temp, 2)
        resultados["base_calculo_fgts_sistema"] = round(base_fgts_temp, 2)

        logger.info(f"[{self.client_id}] Bases de cálculo finais - INSS: {resultados['base_calculo_inss_sistema']:.2f}, IRRF Bruta: {resultados['base_calculo_irrf_bruta_sistema']:.2f}, FGTS: {resultados['base_calculo_fgts_sistema']:.2f}")

        # --- PASSO 4: Cálculo dos Encargos (INSS, IRRF, FGTS) e Salário Família ---

        # 4.1 Cálculo do INSS
        valor_inss_calculado = 0.0
        aliquota_efetiva_inss = 0.0
        base_calculo_inss_para_calculo = resultados["base_calculo_inss_sistema"]
        
        tabela_inss = tabelas_legais.get("inss", {})
        teto_inss = tabela_inss.get("teto", float('inf'))
        base_inss_considerada_para_calculo_faixas = min(base_calculo_inss_para_calculo, teto_inss)

        if base_calculo_inss_para_calculo > 0:
            for faixa in tabela_inss.get("faixas", []):
                limite_faixa = faixa["limite_faixa"]
                aliquota = faixa["aliquota"]
                parcela_a_deduzir = faixa.get("parcela_a_deduzir", 0.0) # Parcela a deduzir para cálculo progressivo direto

                # Lógica para tabela progressiva com parcela a deduzir (mais comum e simples de implementar)
                if base_inss_considerada_para_calculo_faixas <= limite_faixa:
                    valor_inss_calculado = (base_inss_considerada_para_calculo_faixas * aliquota) - parcela_a_deduzir
                    break # Encontrou a faixa correta
            else: # Caso a base seja maior que o limite da última faixa (que deveria ser o teto)
                # Se chegou aqui, significa que a base_inss_considerada_para_calculo_faixas é maior que todos os limites
                # Isso pode acontecer se a última faixa não tiver limite_faixa = teto ou float('inf')
                # Neste caso, aplicar a alíquota da última faixa sobre a base (limitada ao teto)
                if tabela_inss.get("faixas"): 
                    ultima_faixa = tabela_inss["faixas"][-1]
                    valor_inss_calculado = (base_inss_considerada_para_calculo_faixas * ultima_faixa["aliquota"]) - ultima_faixa.get("parcela_a_deduzir", 0.0)
            
            # Garante que o INSS não seja negativo e arredonda
            valor_inss_calculado = round(max(0, valor_inss_calculado), 2)

            if base_calculo_inss_para_calculo > 0:
                aliquota_efetiva_inss = round((valor_inss_calculado / base_calculo_inss_para_calculo) * 100, 4) if valor_inss_calculado > 0 else 0.0
        
        resultados["valor_inss_calculado_sistema"] = valor_inss_calculado
        resultados["aliquota_efetiva_inss_sistema"] = aliquota_efetiva_inss
        logger.info(f"[{self.client_id}] INSS calculado: {valor_inss_calculado:.2f} (Alíquota Efetiva: {aliquota_efetiva_inss}%)")

        # 4.2 Cálculo do Salário Família
        valor_salario_familia = 0.0
        num_dependentes_sf = dados_funcionario_folha.get("dependentes_salario_familia", 0)
        if num_dependentes_sf > 0:
            config_sf = tabelas_legais.get("salario_familia", {})
            # A base para o Salário Família é a remuneração total do empregado no mês.
            # Usaremos a base de INSS como proxy, pois geralmente reflete a remuneração tributável para esse fim.
            remuneracao_para_sf = resultados["base_calculo_inss_sistema"]
            if remuneracao_para_sf <= config_sf.get("limite_renda", 0.0):
                valor_cota_sf = config_sf.get("valor_por_dependente", 0.0)
                valor_salario_familia = round(num_dependentes_sf * valor_cota_sf, 2)
        
        resultados["salario_familia_calculado_sistema"] = valor_salario_familia
        if valor_salario_familia > 0:
            logger.info(f"[{self.client_id}] Salário Família calculado: {valor_salario_familia:.2f} ({num_dependentes_sf} dependentes)")
            # Adicionar o Salário Família às verbas consolidadas se necessário para outros fins (ex: líquido)
            # Não é base para INSS/IRRF/FGTS.
            verbas_consolidadas_para_bases.append({
                "codigo": "MOTOR_SALFAM", 
                "valor": valor_salario_familia, 
                "tipo": "V", 
                "descricao": "Salário Família (Calculado)",
                "origem": "motor"
            })

        # 4.3 Cálculo do IRRF
        valor_irrf_calculado = 0.0
        base_calculo_irrf_liquida = 0.0
        base_irrf_bruta_para_deducoes = resultados["base_calculo_irrf_bruta_sistema"]

        if base_irrf_bruta_para_deducoes > 0:
            deducoes_irrf_total = 0.0
            # Dedução do INSS calculado
            deducoes_irrf_total += resultados["valor_inss_calculado_sistema"]
            
            # Dedução por dependentes de IRRF
            num_dependentes_irrf = dados_funcionario_folha.get("dependentes_irrf", 0)
            valor_deducao_por_dependente_irrf = float(tabelas_legais.get("irrf", {}).get("deducao_por_dependente", 0.0))
            if num_dependentes_irrf > 0 and valor_deducao_por_dependente_irrf > 0:
                deducoes_irrf_total += (num_dependentes_irrf * valor_deducao_por_dependente_irrf)

            # Dedução de Pensão Alimentícia Judicial
            valor_pensao_dedutivel = float(dados_funcionario_folha.get("pensao_alimenticia_valor_dedutivel_irrf", 0.0))
            if valor_pensao_dedutivel > 0:
                deducoes_irrf_total += valor_pensao_dedutivel
            
            # Dedução de Previdência Privada
            valor_previdencia_privada_contribuicao = float(dados_funcionario_folha.get("previdencia_privada_contribuicao_dedutivel_irrf", 0.0))
            if valor_previdencia_privada_contribuicao > 0:
                # Limite de 12% sobre os rendimentos tributáveis (base bruta do IRRF)
                limite_deducao_prev_privada = resultados["base_calculo_irrf_bruta_sistema"] * 0.12
                valor_dedutivel_prev_privada = min(valor_previdencia_privada_contribuicao, limite_deducao_prev_privada)
                deducoes_irrf_total += valor_dedutivel_prev_privada

            base_irrf_apos_deducoes_legais = base_irrf_bruta_para_deducoes - deducoes_irrf_total

            # Opção pelo Desconto Simplificado Mensal (se configurado e mais vantajoso)
            desconto_simplificado_valor = 0.0
            limite_desconto_simplificado_tabela = tabelas_legais.get("irrf", {}).get("limite_desconto_simplificado")
            
            if limite_desconto_simplificado_tabela is not None and limite_desconto_simplificado_tabela > 0:
                # O desconto simplificado é de 25% da faixa de isenção da tabela progressiva mensal.
                # Ou um valor fixo, dependendo da legislação (ex: R$ 528,00 para Fev/2024 em diante)
                # A `limite_desconto_simplificado` na tabela já deve ser esse valor (ex: 528.00 ou 564.80)
                desconto_simplificado_aplicavel = float(limite_desconto_simplificado_tabela)
                
                # Base para IRRF com desconto simplificado
                base_irrf_com_desconto_simplificado = base_irrf_bruta_para_deducoes - desconto_simplificado_aplicavel
                
                # Calcular IRRF com deduções legais
                irrf_com_deducoes_legais = 0.0
                if base_irrf_apos_deducoes_legais > 0:
                    for faixa_irrf in tabelas_legais.get("irrf", {}).get("faixas", []):
                        if base_irrf_apos_deducoes_legais >= faixa_irrf["base_calculo_inicial"] and base_irrf_apos_deducoes_legais <= faixa_irrf["base_calculo_final"]:
                            irrf_com_deducoes_legais = (base_irrf_apos_deducoes_legais * faixa_irrf["aliquota"]) - faixa_irrf["parcela_a_deduzir"]
                            break
                    else: # Base maior que a última faixa
                        if tabelas_legais.get("irrf", {}).get("faixas"): 
                            ultima_faixa_irrf = tabelas_legais["irrf"]["faixas"][-1]
                            irrf_com_deducoes_legais = (base_irrf_apos_deducoes_legais * ultima_faixa_irrf["aliquota"]) - ultima_faixa_irrf["parcela_a_deduzir"]
                irrf_com_deducoes_legais = max(0, irrf_com_deducoes_legais)

                # Calcular IRRF com desconto simplificado
                irrf_com_desconto_simplificado_calc = 0.0
                if base_irrf_com_desconto_simplificado > 0:
                    for faixa_irrf in tabelas_legais.get("irrf", {}).get("faixas", []):
                        if base_irrf_com_desconto_simplificado >= faixa_irrf["base_calculo_inicial"] and base_irrf_com_desconto_simplificado <= faixa_irrf["base_calculo_final"]:
                            irrf_com_desconto_simplificado_calc = (base_irrf_com_desconto_simplificado * faixa_irrf["aliquota"]) - faixa_irrf["parcela_a_deduzir"]
                            break
                    else: # Base maior que a última faixa
                        if tabelas_legais.get("irrf", {}).get("faixas"): 
                            ultima_faixa_irrf = tabelas_legais["irrf"]["faixas"][-1]
                            irrf_com_desconto_simplificado_calc = (base_irrf_com_desconto_simplificado * ultima_faixa_irrf["aliquota"]) - ultima_faixa_irrf["parcela_a_deduzir"]
                irrf_com_desconto_simplificado_calc = max(0, irrf_com_desconto_simplificado_calc)
                
                # Escolher o menor IRRF (mais vantajoso para o empregado)
                if irrf_com_desconto_simplificado_calc < irrf_com_deducoes_legais:
                    valor_irrf_calculado = irrf_com_desconto_simplificado_calc
                    base_calculo_irrf_liquida = base_irrf_com_desconto_simplificado
                    logger.info(f"[{self.client_id}] IRRF: Optou-se pelo desconto simplificado. IRRF: {valor_irrf_calculado:.2f}, Base Líquida: {base_calculo_irrf_liquida:.2f}")
                else:
                    valor_irrf_calculado = irrf_com_deducoes_legais
                    base_calculo_irrf_liquida = base_irrf_apos_deducoes_legais
                    logger.info(f"[{self.client_id}] IRRF: Optou-se pelas deduções legais. IRRF: {valor_irrf_calculado:.2f}, Base Líquida: {base_calculo_irrf_liquida:.2f}")
            else: # Sem opção de desconto simplificado ou não configurado
                base_calculo_irrf_liquida = base_irrf_apos_deducoes_legais
                if base_calculo_irrf_liquida > 0:
                    for faixa_irrf in tabelas_legais.get("irrf", {}).get("faixas", []):
                        # A base de cálculo para IRRF é progressiva por faixas.
                        # A lógica aqui deve encontrar a faixa correta e aplicar alíquota e parcela a deduzir.
                        if base_calculo_irrf_liquida >= faixa_irrf["base_calculo_inicial"] and base_calculo_irrf_liquida <= faixa_irrf["base_calculo_final"]:
                            valor_irrf_calculado = (base_calculo_irrf_liquida * faixa_irrf["aliquota"]) - faixa_irrf["parcela_a_deduzir"]
                            break
                    else: # Base maior que a última faixa
                         if tabelas_legais.get("irrf", {}).get("faixas"): 
                            ultima_faixa_irrf = tabelas_legais["irrf"]["faixas"][-1]
                            valor_irrf_calculado = (base_calculo_irrf_liquida * ultima_faixa_irrf["aliquota"]) - ultima_faixa_irrf["parcela_a_deduzir"]
                logger.info(f"[{self.client_id}] IRRF: Calculado com deduções legais (sem opção de simplificado). IRRF: {valor_irrf_calculado:.2f}, Base Líquida: {base_calculo_irrf_liquida:.2f}")

        resultados["valor_irrf_calculado_sistema"] = round(max(0, valor_irrf_calculado), 2)
        resultados["base_calculo_irrf_liquida_sistema"] = round(max(0, base_calculo_irrf_liquida), 2)
        if resultados["valor_irrf_calculado_sistema"] > 0:
             logger.info(f"[{self.client_id}] IRRF calculado final: {resultados['valor_irrf_calculado_sistema']:.2f}")

        # 4.4 Cálculo do FGTS
        valor_fgts_calculado = 0.0
        base_calculo_fgts = resultados["base_calculo_fgts_sistema"]
        if base_calculo_fgts > 0:
            # TODO: Considerar tipo de contrato para alíquota (ex: aprendiz 2%)
            aliquota_fgts = tabelas_legais.get("parametros_gerais", {}).get("aliquota_fgts_padrao", 0.08)
            tipo_contrato_funcionario = dados_funcionario_folha.get("tipo_contrato", "normal") # ex: "aprendiz"
            if tipo_contrato_funcionario == "aprendiz":
                aliquota_fgts = tabelas_legais.get("parametros_gerais", {}).get("aliquota_fgts_aprendiz", 0.02)
            
            valor_fgts_calculado = round(base_calculo_fgts * aliquota_fgts, 2)
        
        resultados["valor_fgts_calculado_sistema"] = valor_fgts_calculado
        if valor_fgts_calculado > 0:
            logger.info(f"[{self.client_id}] FGTS calculado: {valor_fgts_calculado:.2f}")

        # Armazenar as verbas calculadas pelo motor no campo 'outras_verbas_calculadas_motor' para referência
        for verba in verbas_consolidadas_para_bases:
            if verba["origem"] == "motor":
                resultados["outras_verbas_calculadas_motor"][verba["codigo"]] = {
                    "valor": verba["valor"],
                    "descricao": verba["descricao"]
                }

        # Calcular totais
        # Soma todos os vencimentos da lista de verbas consolidadas
        total_vencimentos_calculado_sistema = sum(
            verba['valor'] for verba in verbas_consolidadas_para_bases if verba['tipo'] == 'V'
        )

        # Descontos incluem INSS e IRRF calculados pelo motor, mais outros descontos da folha original
        total_descontos_calculado_sistema = resultados['valor_inss_calculado_sistema'] + resultados['valor_irrf_calculado_sistema']
        for verba in verbas_consolidadas_para_bases:
            if verba['tipo'] == 'D':
                # Adiciona apenas descontos que são originários da folha
                if verba.get('origem') == 'folha': 
                    total_descontos_calculado_sistema += verba['valor']
        
        total_liquido_calculado_sistema = round(total_vencimentos_calculado_sistema - total_descontos_calculado_sistema, 2)

        resultados['total_vencimentos_calculado_sistema'] = round(total_vencimentos_calculado_sistema, 2)
        resultados['total_descontos_calculado_sistema'] = round(total_descontos_calculado_sistema, 2)
        resultados['total_liquido_calculado_sistema'] = total_liquido_calculado_sistema

        logs_calculo = resultados.get('logs_calculo', [])
        # Atualiza o log com as bases corretas que já foram calculadas e armazenadas
        logs_calculo.append(f"Bases de cálculo utilizadas: INSS={resultados['base_calculo_inss_sistema']:.2f}, IRRF Bruta={resultados['base_calculo_irrf_bruta_sistema']:.2f}, FGTS={resultados['base_calculo_fgts_sistema']:.2f}")
        logs_calculo.append(f"Totais Calculados: Vencimentos={resultados['total_vencimentos_calculado_sistema']:.2f}, Descontos={resultados['total_descontos_calculado_sistema']:.2f}, Líquido={resultados['total_liquido_calculado_sistema']:.2f}")
        resultados['logs_calculo'] = logs_calculo

        logger.info(f"[{self.client_id}] Cálculo finalizado para funcionário {id_funcionario}. Resultado: {resultados}")
        return resultados

# Exemplo de uso (para desenvolvimento/teste local):
if __name__ == '__main__':
    logger.info("Executando exemplo do MotorCalculoFolhaService...")
    
    # Mock de dados para teste
    mock_client_id = "cliente_teste_001"
    mock_service = MotorCalculoFolhaService(client_id=mock_client_id)

    mock_competencia = "2024-12"
    mock_tabelas = mock_service._carregar_tabelas_legais(mock_competencia) # Carrega tabelas de exemplo

    mock_dados_func = {
        "id_folha": "folha_dez_2024_001",
        "id_funcionario": "func_123",
        "competencia": mock_competencia,
        "rubricas_folha": [
            {"codigo": "R001", "descricao": "Salário Base", "valor": 3000.00, "tipo": "V"},
            {"codigo": "R010", "descricao": "Horas Extras 50%", "valor": 500.00, "tipo": "V"},
            {"codigo": "R015", "descricao": "Comissões", "valor": 200.00, "tipo": "V"},
            {"codigo": "D001", "descricao": "Faltas", "valor": 100.00, "tipo": "D"}, # Exemplo de desconto
        ],
        "dependentes_sf": 1,
        "dependentes_irrf": 2
    }

    mock_rubricas_config = {
        "R001": {"inss": True, "irrf": True, "fgts": True, "dsr_base": False},
        "R010": {"inss": True, "irrf": True, "fgts": True, "dsr_base": True}, # HE incide para DSR
        "R015": {"inss": True, "irrf": True, "fgts": True, "dsr_base": True}, # Comissão incide para DSR
        "D001": {"inss": True, "irrf": True, "fgts": False}, # Faltas podem reduzir base de INSS/IRRF
    }
    
    mock_params_gerais = {
        "competencia_folha": mock_competencia,
        "aliquota_fgts_padrao": 0.08,
        "dias_uteis_mes": 22, # Exemplo para DSR
        "domingos_feriados_mes": 8 # Exemplo para DSR
    }

    # Chamada da função principal de cálculo
    # Nota: A lógica de cálculo dentro da função ainda é um placeholder.
    # resultado_calculo = mock_service.calcular_folha_funcionario_audit360(
    #     dados_funcionario_folha=mock_dados_func,
    #     rubricas_config=mock_rubricas_config,
    #     tabelas_legais=mock_tabelas,
    #     parametros_gerais=mock_params_gerais
    # )

    # print("\\n--- Resultado do Cálculo (Exemplo) ---")
    # import json
    # print(json.dumps(resultado_calculo, indent=4, ensure_ascii=False))

    logger.warning("A lógica de cálculo detalhada (INSS, IRRF, FGTS, DSR, etc.) precisa ser implementada.")
    logger.info("O exemplo acima mostra a estrutura e os dados de entrada/saída esperados.")
    logger.info("Descomente a chamada a 'calcular_folha_funcionario_audit360' e implemente as seções TODO.")

