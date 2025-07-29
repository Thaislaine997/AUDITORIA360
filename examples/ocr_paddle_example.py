"""
Exemplo abrangente de uso do PaddleOCR para processamento de documentos.

Este exemplo demonstra:
- OCR básico em imagens
- Processamento de PDFs
- Extração de dados estruturados
- Validação de documentos
- Performance e otimização

Requer: paddleocr, paddlepaddle, pdf2image, opencv-python
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import time

try:
    from paddleocr import PaddleOCR
    import cv2
    import numpy as np
    from pdf2image import convert_from_path
    
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Dependências não instaladas: {e}")
    print("Execute: pip install paddleocr pdf2image opencv-python")
    DEPENDENCIES_AVAILABLE = False


class DocumentOCR:
    """Classe para processamento OCR de documentos."""
    
    def __init__(self, lang: str = "pt", use_gpu: bool = False):
        """
        Inicializa o OCR.
        
        Args:
            lang: Idioma do OCR (pt, en, etc.)
            use_gpu: Usar GPU se disponível
        """
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Dependências necessárias não estão instaladas")
        
        self.ocr = PaddleOCR(
            use_angle_cls=True, 
            lang=lang, 
            use_gpu=use_gpu,
            show_log=False
        )
        print(f"✅ OCR inicializado (idioma: {lang}, GPU: {use_gpu})")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Pré-processa imagem para melhor OCR.
        
        Args:
            image_path: Caminho da imagem
            
        Returns:
            numpy.ndarray: Imagem processada
        """
        # Carregar imagem
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Aplicar denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Aplicar threshold para binarização
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def extract_text_from_image(self, image_path: str, preprocess: bool = True) -> Dict:
        """
        Extrai texto de uma imagem.
        
        Args:
            image_path: Caminho da imagem
            preprocess: Se deve pré-processar a imagem
            
        Returns:
            dict: Resultado da extração
        """
        start_time = time.time()
        
        try:
            # Pré-processar se solicitado
            if preprocess:
                processed_img = self.preprocess_image(image_path)
                # Salvar imagem processada temporariamente
                temp_path = "/tmp/processed_image.png"
                cv2.imwrite(temp_path, processed_img)
                image_to_process = temp_path
            else:
                image_to_process = image_path
            
            # Executar OCR
            result = self.ocr.ocr(image_to_process, cls=True)
            
            # Processar resultado
            extracted_data = self._process_ocr_result(result)
            
            processing_time = time.time() - start_time
            
            return {
                "success": True,
                "text": extracted_data["full_text"],
                "lines": extracted_data["lines"],
                "confidence": extracted_data["avg_confidence"],
                "processing_time": processing_time,
                "image_path": image_path,
                "preprocessed": preprocess
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "image_path": image_path,
                "processing_time": time.time() - start_time
            }
    
    def extract_text_from_pdf(self, pdf_path: str, dpi: int = 300) -> Dict:
        """
        Extrai texto de um PDF convertendo para imagens.
        
        Args:
            pdf_path: Caminho do PDF
            dpi: Resolução para conversão
            
        Returns:
            dict: Resultado da extração
        """
        start_time = time.time()
        
        try:
            # Converter PDF para imagens
            print(f"📄 Convertendo PDF: {pdf_path}")
            pages = convert_from_path(pdf_path, dpi=dpi)
            
            all_text = []
            all_lines = []
            confidence_scores = []
            
            for i, page in enumerate(pages):
                print(f"🔍 Processando página {i+1}/{len(pages)}")
                
                # Salvar página como imagem temporária
                temp_image_path = f"/tmp/pdf_page_{i+1}.png"
                page.save(temp_image_path, "PNG")
                
                # Processar página
                page_result = self.extract_text_from_image(temp_image_path)
                
                if page_result["success"]:
                    all_text.append(f"=== PÁGINA {i+1} ===\n{page_result['text']}")
                    all_lines.extend([
                        {"page": i+1, "line": j+1, "text": line["text"], "confidence": line["confidence"]}
                        for j, line in enumerate(page_result["lines"])
                    ])
                    confidence_scores.append(page_result["confidence"])
                
                # Limpar arquivo temporário
                os.remove(temp_image_path)
            
            processing_time = time.time() - start_time
            
            return {
                "success": True,
                "text": "\n\n".join(all_text),
                "lines": all_lines,
                "pages_processed": len(pages),
                "confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
                "processing_time": processing_time,
                "pdf_path": pdf_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "pdf_path": pdf_path,
                "processing_time": time.time() - start_time
            }
    
    def extract_structured_data(self, text: str, document_type: str = "payroll") -> Dict:
        """
        Extrai dados estruturados do texto OCR.
        
        Args:
            text: Texto extraído
            document_type: Tipo do documento (payroll, contract, cct)
            
        Returns:
            dict: Dados estruturados extraídos
        """
        if document_type == "payroll":
            return self._extract_payroll_data(text)
        elif document_type == "contract":
            return self._extract_contract_data(text)
        elif document_type == "cct":
            return self._extract_cct_data(text)
        else:
            return {"raw_text": text}
    
    def _process_ocr_result(self, result: List) -> Dict:
        """Processa resultado bruto do OCR."""
        full_text = []
        lines = []
        confidence_scores = []
        
        for line in result:
            for box, (text, conf) in line:
                full_text.append(text)
                lines.append({
                    "text": text,
                    "confidence": conf,
                    "box": box
                })
                confidence_scores.append(conf)
        
        return {
            "full_text": " ".join(full_text),
            "lines": lines,
            "avg_confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        }
    
    def _extract_payroll_data(self, text: str) -> Dict:
        """Extrai dados específicos de demonstrativo de pagamento."""
        data = {}
        
        # Padrões regex para dados comuns
        patterns = {
            "nome": r"(?:Nome|Funcionário|Employee):\s*([A-Za-zÀ-ÿ\s]+)",
            "cpf": r"CPF:\s*(\d{3}\.?\d{3}\.?\d{3}-?\d{2})",
            "matricula": r"(?:Matrícula|Registro):\s*(\d+)",
            "salario_base": r"(?:Salário Base|Salário):\s*R?\$?\s*([\d.,]+)",
            "inss": r"INSS:\s*R?\$?\s*([\d.,]+)",
            "irrf": r"IRRF:\s*R?\$?\s*([\d.,]+)",
            "liquido": r"(?:Líquido|Valor Líquido):\s*R?\$?\s*([\d.,]+)"
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data[field] = match.group(1).strip()
        
        return data
    
    def _extract_contract_data(self, text: str) -> Dict:
        """Extrai dados específicos de contrato de trabalho."""
        data = {}
        
        patterns = {
            "nome": r"(?:Nome|Contratado):\s*([A-Za-zÀ-ÿ\s]+)",
            "cargo": r"(?:Cargo|Função):\s*([A-Za-zÀ-ÿ\s]+)",
            "salario": r"(?:Salário|Remuneração):\s*R?\$?\s*([\d.,]+)",
            "data_admissao": r"(?:Admissão|Data de Admissão):\s*(\d{1,2}\/\d{1,2}\/\d{4})",
            "jornada": r"(?:Jornada|Carga Horária):\s*(\d+)\s*horas"
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data[field] = match.group(1).strip()
        
        return data
    
    def _extract_cct_data(self, text: str) -> Dict:
        """Extrai dados específicos de CCT."""
        data = {}
        
        patterns = {
            "sindicato": r"(?:Sindicato|Entidade):\s*([A-Za-zÀ-ÿ\s]+)",
            "vigencia": r"(?:Vigência|Período):\s*(\d{4}-?\d{4})",
            "reajuste": r"(?:Reajuste|Aumento):\s*([\d,]+)%",
            "vale_alimentacao": r"(?:Vale Alimentação|Alimentação):\s*R?\$?\s*([\d.,]+)"
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data[field] = match.group(1).strip()
        
        return data


def create_sample_documents():
    """Cria documentos de exemplo para teste."""
    print("\n📄 Criando documentos de exemplo...")
    
    # Criar imagem de texto simulada (usando OpenCV)
    if DEPENDENCIES_AVAILABLE:
        # Criar imagem com texto
        img = np.ones((600, 800, 3), dtype=np.uint8) * 255
        
        # Adicionar texto
        font = cv2.FONT_HERSHEY_SIMPLEX
        texts = [
            "DEMONSTRATIVO DE PAGAMENTO",
            "Nome: Maria Silva Santos",
            "CPF: 123.456.789-00",
            "Matrícula: 001234",
            "",
            "PROVENTOS:",
            "Salário Base: R$ 4.500,00",
            "Horas Extras: R$ 300,00",
            "",
            "DESCONTOS:",
            "INSS: R$ 495,00",
            "IRRF: R$ 112,50",
            "",
            "LÍQUIDO: R$ 4.192,50"
        ]
        
        y_start = 50
        for i, text in enumerate(texts):
            y = y_start + (i * 35)
            cv2.putText(img, text, (50, y), font, 0.7, (0, 0, 0), 2)
        
        # Salvar imagem
        sample_image = "/tmp/demonstrativo_exemplo.png"
        cv2.imwrite(sample_image, img)
        print(f"✅ Imagem criada: {sample_image}")
        
        return [sample_image]
    
    return []


def example_basic_ocr():
    """Exemplo básico de OCR."""
    print("\n🔍 === EXEMPLO DE OCR BÁSICO ===")
    
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Dependências não disponíveis")
        return
    
    # Criar documentos de exemplo
    sample_files = create_sample_documents()
    
    if not sample_files:
        print("❌ Nenhum arquivo de exemplo foi criado")
        return
    
    # Inicializar OCR
    ocr_processor = DocumentOCR(lang="pt")
    
    for file_path in sample_files:
        print(f"\n📄 Processando: {file_path}")
        
        # Processar com e sem pré-processamento
        for preprocess in [False, True]:
            print(f"\n{'Com' if preprocess else 'Sem'} pré-processamento:")
            
            result = ocr_processor.extract_text_from_image(file_path, preprocess=preprocess)
            
            if result["success"]:
                print(f"✅ Sucesso em {result['processing_time']:.2f}s")
                print(f"📊 Confiança média: {result['confidence']:.2f}")
                print(f"📝 Linhas extraídas: {len(result['lines'])}")
                
                # Mostrar texto extraído
                text = result['text']
                if len(text) > 200:
                    text = text[:200] + "..."
                print(f"📄 Texto: {text}")
                
            else:
                print(f"❌ Erro: {result['error']}")


def example_structured_extraction():
    """Exemplo de extração estruturada."""
    print("\n📋 === EXEMPLO DE EXTRAÇÃO ESTRUTURADA ===")
    
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Dependências não disponíveis")
        return
    
    # Criar documentos de exemplo
    sample_files = create_sample_documents()
    
    if not sample_files:
        print("❌ Nenhum arquivo de exemplo foi criado")
        return
    
    ocr_processor = DocumentOCR(lang="pt")
    
    for file_path in sample_files:
        print(f"\n📄 Processando: {Path(file_path).name}")
        
        # Extrair texto
        result = ocr_processor.extract_text_from_image(file_path)
        
        if result["success"]:
            # Extrair dados estruturados
            structured_data = ocr_processor.extract_structured_data(
                result["text"], 
                document_type="payroll"
            )
            
            print(f"📊 Dados estruturados extraídos:")
            for field, value in structured_data.items():
                print(f"- {field}: {value}")


def example_performance_comparison():
    """Exemplo de comparação de performance."""
    print("\n⚡ === TESTE DE PERFORMANCE ===")
    
    if not DEPENDENCIES_AVAILABLE:
        print("❌ Dependências não disponíveis")
        return
    
    sample_files = create_sample_documents()
    
    if not sample_files:
        print("❌ Nenhum arquivo de exemplo foi criado")
        return
    
    # Testar diferentes configurações
    configs = [
        {"lang": "pt", "use_gpu": False, "name": "CPU - Português"},
        {"lang": "en", "use_gpu": False, "name": "CPU - Inglês"}
    ]
    
    results = []
    
    for config in configs:
        print(f"\n🔧 Testando: {config['name']}")
        
        try:
            ocr_processor = DocumentOCR(
                lang=config["lang"], 
                use_gpu=config["use_gpu"]
            )
            
            for file_path in sample_files:
                result = ocr_processor.extract_text_from_image(file_path)
                
                if result["success"]:
                    results.append({
                        "config": config["name"],
                        "file": Path(file_path).name,
                        "time": result["processing_time"],
                        "confidence": result["confidence"],
                        "lines": len(result["lines"])
                    })
                    
                    print(f"⏱️ Tempo: {result['processing_time']:.2f}s")
                    print(f"📊 Confiança: {result['confidence']:.2f}")
                    
        except Exception as e:
            print(f"❌ Erro na configuração {config['name']}: {e}")
    
    # Resumo dos resultados
    if results:
        print(f"\n📈 RESUMO DE PERFORMANCE:")
        for result in results:
            print(f"- {result['config']}: {result['time']:.2f}s (conf: {result['confidence']:.2f})")


def main():
    """Função principal com todos os exemplos."""
    print("🔍 EXEMPLOS AVANÇADOS - OCR PADDLEOCR AUDITORIA360")
    print("=" * 55)
    
    if len(sys.argv) >= 2:
        # Modo compatibilidade - processar arquivo específico
        img_path = sys.argv[1]
        
        if not DEPENDENCIES_AVAILABLE:
            print("❌ Dependências não disponíveis")
            return
        
        if not os.path.exists(img_path):
            print(f"❌ Arquivo não encontrado: {img_path}")
            return
        
        print(f"🔍 Processando arquivo: {img_path}")
        
        ocr_processor = DocumentOCR(lang="pt")
        result = ocr_processor.extract_text_from_image(img_path)
        
        if result["success"]:
            print(f"\n📄 Texto extraído:")
            for line in result["lines"]:
                print(f"Texto: {line['text']} (confiança: {line['confidence']:.2f})")
        else:
            print(f"❌ Erro: {result['error']}")
    
    else:
        # Executar todos os exemplos
        try:
            example_basic_ocr()
            example_structured_extraction()
            example_performance_comparison()
            
            print("\n✅ Todos os exemplos executados com sucesso!")
            print("\n📚 Para mais informações, consulte:")
            print("- Documentação OCR: docs/tecnico/ocr-guide.md")
            print("- Uso: python ocr_paddle_example.py caminho/para/imagem.png")
            
        except Exception as e:
            print(f"\n❌ Erro durante execução: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
