"""
Exemplo prático de uso da API de Documentos do AUDITORIA360.

Este exemplo demonstra:
- Upload de documentos para R2
- Listagem e busca de documentos
- Download de documentos
- Processamento OCR
- Gestão de versões

Requer: requests, python-dotenv, pathlib
"""

import os
import requests
from pathlib import Path
from typing import Dict, List, Optional


class DocumentsAPI:
    """Cliente para interagir com a API de Documentos."""
    
    def __init__(self, base_url: str = "http://localhost:8000", token: str = None):
        self.base_url = base_url
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}" if token else ""
        }
    
    def upload_document(
        self, 
        file_path: str, 
        category: str = "other",
        title: Optional[str] = None,
        description: Optional[str] = None,
        process_ocr: bool = True
    ) -> Dict:
        """
        Faz upload de um documento.
        
        Args:
            file_path: Caminho do arquivo
            category: Categoria do documento
            title: Título personalizado
            description: Descrição do documento
            process_ocr: Se deve processar OCR automaticamente
            
        Returns:
            dict: Dados do documento criado
        """
        url = f"{self.base_url}/api/v1/documents/upload"
        
        try:
            file_name = Path(file_path).name
            
            with open(file_path, 'rb') as file:
                files = {"file": (file_name, file)}
                data = {
                    "category": category,
                    "title": title or file_name,
                    "description": description or f"Documento {file_name}",
                    "process_ocr": process_ocr
                }
                
                response = requests.post(url, files=files, data=data, headers=self.headers)
                response.raise_for_status()
                
                result = response.json()
                print(f"✅ Documento uploaded: {file_name}")
                return result
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro no upload: {e}")
            return {"error": str(e)}
        except FileNotFoundError:
            error_msg = f"Arquivo não encontrado: {file_path}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def list_documents(
        self, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict]:
        """
        Lista documentos com filtros.
        
        Args:
            skip: Número de registros para pular
            limit: Limite de registros
            category: Filtrar por categoria
            search: Termo de busca
            
        Returns:
            list: Lista de documentos
        """
        url = f"{self.base_url}/api/v1/documents/"
        params = {"skip": skip, "limit": limit}
        
        if category:
            params["category"] = category
        if search:
            params["search"] = search
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            documents = response.json()
            print(f"✅ Documentos obtidos: {len(documents)} encontrados")
            return documents
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao listar documentos: {e}")
            return []
    
    def get_document(self, document_id: int) -> Dict:
        """
        Obtém detalhes de um documento específico.
        
        Args:
            document_id: ID do documento
            
        Returns:
            dict: Dados do documento
        """
        url = f"{self.base_url}/api/v1/documents/{document_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            document = response.json()
            print(f"✅ Documento obtido: {document.get('title', 'N/A')}")
            return document
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao obter documento: {e}")
            return {"error": str(e)}
    
    def download_document(self, document_id: int, download_path: str) -> bool:
        """
        Baixa um documento.
        
        Args:
            document_id: ID do documento
            download_path: Caminho para salvar o arquivo
            
        Returns:
            bool: True se download foi bem-sucedido
        """
        url = f"{self.base_url}/api/v1/documents/{document_id}/download"
        
        try:
            response = requests.get(url, headers=self.headers, stream=True)
            response.raise_for_status()
            
            with open(download_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            print(f"✅ Documento baixado: {download_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro no download: {e}")
            return False
    
    def process_ocr(self, document_id: int) -> Dict:
        """
        Processa OCR em um documento.
        
        Args:
            document_id: ID do documento
            
        Returns:
            dict: Resultado do processamento OCR
        """
        url = f"{self.base_url}/api/v1/documents/{document_id}/ocr"
        
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ OCR processado para documento {document_id}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro no processamento OCR: {e}")
            return {"error": str(e)}
    
    def search_documents(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Busca documentos por conteúdo.
        
        Args:
            query: Termo de busca
            filters: Filtros adicionais
            
        Returns:
            list: Documentos encontrados
        """
        url = f"{self.base_url}/api/v1/documents/search"
        params = {"q": query}
        
        if filters:
            params.update(filters)
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            results = response.json()
            print(f"✅ Busca realizada: {len(results)} documentos encontrados")
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na busca: {e}")
            return []


def create_sample_documents():
    """Cria documentos de exemplo para teste."""
    print("\n📄 === CRIANDO DOCUMENTOS DE EXEMPLO ===")
    
    # Criar alguns arquivos de exemplo
    sample_files = {
        "/tmp/contrato_trabalho.txt": """
        CONTRATO DE TRABALHO
        
        Nome: João Silva Santos
        CPF: 123.456.789-00
        Cargo: Analista de Sistemas
        Salário: R$ 5.000,00
        Data de Admissão: 15/01/2024
        
        Cláusulas do contrato:
        1. Jornada de trabalho: 40 horas semanais
        2. Vale transporte: R$ 200,00
        3. Vale refeição: R$ 350,00
        """,
        "/tmp/demonstrativo_pagamento.txt": """
        DEMONSTRATIVO DE PAGAMENTO
        Janeiro/2024
        
        Funcionário: Maria Costa
        Matrícula: 001234
        
        PROVENTOS:
        Salário Base: R$ 4.500,00
        Horas Extras: R$ 300,00
        Vale Refeição: R$ 350,00
        
        DESCONTOS:
        INSS: R$ 495,00
        IRRF: R$ 112,50
        Plano de Saúde: R$ 150,00
        
        LÍQUIDO: R$ 4.392,50
        """,
        "/tmp/cct_sindicato.txt": """
        CONVENÇÃO COLETIVA DE TRABALHO
        
        Sindicato dos Trabalhadores em Tecnologia
        Vigência: 2024-2025
        
        Cláusula 15 - Reajuste Salarial
        Os salários serão reajustados em 5% ao ano.
        
        Cláusula 22 - Vale Alimentação
        Valor mínimo: R$ 350,00 por mês.
        
        Cláusula 31 - Plano de Saúde
        Empresa contribui com 80% do valor.
        """
    }
    
    for file_path, content in sample_files.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Arquivo criado: {file_path}")
    
    return list(sample_files.keys())


def example_document_upload():
    """Exemplo de upload de documentos."""
    print("\n📤 === EXEMPLO DE UPLOAD DE DOCUMENTOS ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = DocumentsAPI(token=token)
    
    # Criar arquivos de exemplo
    sample_files = create_sample_documents()
    
    uploaded_docs = []
    
    for file_path in sample_files:
        file_name = Path(file_path).name
        
        # Determinar categoria baseada no nome do arquivo
        if "contrato" in file_name:
            category = "contracts"
        elif "demonstrativo" in file_name:
            category = "payroll"
        elif "cct" in file_name:
            category = "cct"
        else:
            category = "other"
        
        result = api.upload_document(
            file_path=file_path,
            category=category,
            title=f"Documento - {file_name}",
            description=f"Documento de exemplo da categoria {category}",
            process_ocr=True
        )
        
        if "id" in result:
            uploaded_docs.append(result)
            print(f"- ID: {result['id']}")
            print(f"- URL: {result.get('file_url', 'N/A')}")
            print(f"- Tamanho: {result.get('file_size', 0)} bytes")
    
    return uploaded_docs


def example_document_listing():
    """Exemplo de listagem e busca de documentos."""
    print("\n📋 === EXEMPLO DE LISTAGEM DE DOCUMENTOS ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = DocumentsAPI(token=token)
    
    # Listar todos os documentos
    all_docs = api.list_documents(limit=10)
    
    if all_docs:
        print(f"Documentos cadastrados:")
        for doc in all_docs:
            print(f"- {doc.get('title', 'N/A')} ({doc.get('category', 'N/A')})")
    
    # Filtrar por categoria
    payroll_docs = api.list_documents(category="payroll")
    print(f"\nDocumentos de folha de pagamento: {len(payroll_docs)}")
    
    # Buscar documentos
    search_results = api.search_documents(
        query="salário",
        filters={"category": "payroll", "date_from": "2024-01-01"}
    )
    print(f"Documentos com 'salário': {len(search_results)}")
    
    for result in search_results:
        relevance = result.get('relevance_score', 0)
        print(f"- {result.get('title', 'N/A')} (relevância: {relevance:.2f})")


def example_document_processing():
    """Exemplo de processamento de documentos."""
    print("\n🔍 === EXEMPLO DE PROCESSAMENTO OCR ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = DocumentsAPI(token=token)
    
    # Simular um documento já enviado
    document_id = 1
    
    # Obter detalhes do documento
    doc_details = api.get_document(document_id)
    
    if "id" in doc_details:
        print(f"Processando documento: {doc_details.get('title', 'N/A')}")
        print(f"Categoria: {doc_details.get('category', 'N/A')}")
        print(f"Tamanho: {doc_details.get('file_size', 0)} bytes")
        
        # Processar OCR se ainda não foi processado
        if not doc_details.get('ocr_processed', False):
            ocr_result = api.process_ocr(document_id)
            
            if "extracted_text" in ocr_result:
                print(f"\n📝 Texto extraído via OCR:")
                print(f"Confiança: {ocr_result.get('confidence', 0):.2f}")
                print(f"Páginas processadas: {ocr_result.get('pages_processed', 0)}")
                print(f"Idioma detectado: {ocr_result.get('detected_language', 'N/A')}")
                
                # Mostrar amostra do texto
                text = ocr_result['extracted_text']
                if len(text) > 200:
                    text = text[:200] + "..."
                print(f"Amostra do texto: {text}")
        else:
            print("OCR já foi processado para este documento")


def example_document_download():
    """Exemplo de download de documentos."""
    print("\n💾 === EXEMPLO DE DOWNLOAD DE DOCUMENTOS ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = DocumentsAPI(token=token)
    
    # Baixar documento específico
    document_id = 1
    download_path = "/tmp/documento_baixado.pdf"
    
    success = api.download_document(document_id, download_path)
    
    if success:
        file_size = os.path.getsize(download_path)
        print(f"Arquivo baixado com sucesso:")
        print(f"- Caminho: {download_path}")
        print(f"- Tamanho: {file_size} bytes")
        
        # Verificar se arquivo existe
        if os.path.exists(download_path):
            print(f"✅ Arquivo confirmado no sistema de arquivos")
        else:
            print(f"❌ Arquivo não encontrado após download")


def example_document_versioning():
    """Exemplo de versionamento de documentos."""
    print("\n📊 === EXEMPLO DE VERSIONAMENTO ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = DocumentsAPI(token=token)
    
    # Criar nova versão de um documento existente
    document_id = 1
    new_version_file = "/tmp/contrato_trabalho_v2.txt"
    
    # Criar versão atualizada
    updated_content = """
    CONTRATO DE TRABALHO - VERSÃO 2.0
    
    Nome: João Silva Santos
    CPF: 123.456.789-00
    Cargo: Analista de Sistemas Sênior  # PROMOÇÃO
    Salário: R$ 6.000,00  # AUMENTO
    Data de Admissão: 15/01/2024
    Data de Promoção: 01/03/2024
    
    Novas cláusulas:
    4. Bônus por performance: até 20%
    5. Home office: 2 dias por semana
    """
    
    with open(new_version_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    # Upload nova versão
    url = f"{api.base_url}/api/v1/documents/{document_id}/versions"
    
    try:
        with open(new_version_file, 'rb') as file:
            files = {"file": file}
            data = {
                "version_notes": "Promoção e aumento salarial",
                "major_version": True
            }
            
            response = requests.post(url, files=files, data=data, headers=api.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Nova versão criada:")
            print(f"- Versão: {result.get('version', 'N/A')}")
            print(f"- Notas: {result.get('version_notes', 'N/A')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao criar versão: {e}")
    
    # Listar versões do documento
    versions_url = f"{api.base_url}/api/v1/documents/{document_id}/versions"
    
    try:
        response = requests.get(versions_url, headers=api.headers)
        response.raise_for_status()
        
        versions = response.json()
        print(f"\nHistórico de versões:")
        for version in versions:
            print(f"- v{version.get('version', 'N/A')}: {version.get('created_at', 'N/A')}")
            if version.get('version_notes'):
                print(f"  Notas: {version['version_notes']}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao listar versões: {e}")


def main():
    """Função principal com todos os exemplos."""
    print("📁 EXEMPLOS DE USO - API DE DOCUMENTOS AUDITORIA360")
    print("=" * 60)
    
    try:
        example_document_upload()
        example_document_listing()
        example_document_processing()
        example_document_download()
        example_document_versioning()
        
        print("\n✅ Todos os exemplos executados com sucesso!")
        print("\n📚 Para mais informações, consulte:")
        print("- Documentação da API: http://localhost:8000/docs")
        print("- Manual de documentos: docs/usuario/manual-documentos.md")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        print("Verifique se a API está rodando e o token é válido")


if __name__ == "__main__":
    main()