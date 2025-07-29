"""
Módulo principal com funções de processamento de documentos e planilhas de controle (Refatorado).
Implementa processamento robusto com tratamento de erros centralizado e documentação abrangente.
"""

import logging
from typing import Optional, Dict, Any
from pathlib import Path
import sys

# Add utils to path for error handling
sys.path.append(str(Path(__file__).parent))

try:
    from utils.error_handling import (
        error_handler, ErrorCategory, ErrorSeverity, 
        handle_exceptions, ValidationError, safe_execute
    )
    ENHANCED_ERROR_HANDLING = True
except ImportError:
    ENHANCED_ERROR_HANDLING = False
    logging.warning("Sistema de tratamento de erros avançado não disponível")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Processador de documentos com OCR e tratamento de erros robusto.
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff']
        logger.info("DocumentProcessor inicializado")
    
    def _validate_inputs(self, file_name: str, bucket_name: str) -> None:
        """
        Valida os parâmetros de entrada.
        
        Args:
            file_name: Nome do arquivo
            bucket_name: Nome do bucket
            
        Raises:
            ValidationError: Se os parâmetros são inválidos
        """
        if not file_name or not isinstance(file_name, str):
            raise ValidationError(
                "Nome do arquivo é obrigatório e deve ser uma string",
                field="file_name",
                validation_code="INVALID_FILENAME"
            )
        
        if not bucket_name or not isinstance(bucket_name, str):
            raise ValidationError(
                "Nome do bucket é obrigatório e deve ser uma string",
                field="bucket_name", 
                validation_code="INVALID_BUCKET"
            )
        
        # Verificar extensão do arquivo
        file_path = Path(file_name)
        if file_path.suffix.lower() not in self.supported_formats:
            raise ValidationError(
                f"Formato de arquivo não suportado: {file_path.suffix}. "
                f"Formatos suportados: {', '.join(self.supported_formats)}",
                field="file_name",
                validation_code="UNSUPPORTED_FORMAT"
            )
    
    @handle_exceptions(ErrorCategory.SYSTEM, ErrorSeverity.MEDIUM)
    def process_document_ocr(self, file_name: str, bucket_name: str) -> Dict[str, Any]:
        """
        Processa um documento PDF usando OCR com tratamento de erros robusto.
        
        Args:
            file_name: Nome do arquivo PDF no bucket
            bucket_name: Nome do bucket GCS
            
        Returns:
            dict: Resultado do processamento com status e dados extraídos
            
        Raises:
            ValidationError: Para erros de validação de entrada
            Exception: Para outros erros de processamento
        """
        try:
            logger.info(f"Iniciando processamento OCR: {file_name} do bucket {bucket_name}")
            
            # Validar entradas
            self._validate_inputs(file_name, bucket_name)
            
            # Simular processamento OCR
            # Em implementação real, aqui seria usado PaddleOCR ou similar
            ocr_result = self._perform_ocr_processing(file_name, bucket_name)
            
            # Validar resultado
            if not ocr_result.get('extracted_text'):
                logger.warning(f"Nenhum texto extraído de {file_name}")
            
            result = {
                "status": "success",
                "file_name": file_name,
                "bucket_name": bucket_name,
                "extracted_text": ocr_result.get('extracted_text', ''),
                "confidence": ocr_result.get('confidence', 0.0),
                "pages_processed": ocr_result.get('pages_processed', 1),
                "processing_time_ms": ocr_result.get('processing_time_ms', 0),
                "metadata": {
                    "processor_version": "1.0.0",
                    "format_detected": Path(file_name).suffix.lower(),
                    "file_size_bytes": ocr_result.get('file_size', 0)
                }
            }
            
            logger.info(f"OCR processado com sucesso: {file_name}")
            return result
            
        except ValidationError as e:
            if ENHANCED_ERROR_HANDLING:
                error = error_handler.create_error(
                    message=f"Erro de validação no processamento OCR: {e.message}",
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.MEDIUM,
                    error_code=e.validation_code,
                    details=f"Campo: {e.field}, Arquivo: {file_name}",
                    original_exception=e
                )
                error_handler.handle_error(error)
            
            return {
                "status": "validation_error",
                "file_name": file_name,
                "bucket_name": bucket_name,
                "error": e.message,
                "error_code": e.validation_code,
                "field": e.field
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento OCR de {file_name}: {str(e)}")
            
            if ENHANCED_ERROR_HANDLING:
                error = error_handler.create_error(
                    message=f"Falha no processamento OCR de {file_name}",
                    category=ErrorCategory.SYSTEM,
                    severity=ErrorSeverity.HIGH,
                    details=f"Bucket: {bucket_name}",
                    original_exception=e
                )
                error_handler.handle_error(error)
            
            return {
                "status": "error",
                "file_name": file_name,
                "bucket_name": bucket_name,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _perform_ocr_processing(self, file_name: str, bucket_name: str) -> Dict[str, Any]:
        """
        Simula o processamento OCR real.
        Em implementação real, integraria com PaddleOCR ou Google Vision API.
        
        Args:
            file_name: Nome do arquivo
            bucket_name: Nome do bucket
            
        Returns:
            dict: Resultado simulado do OCR
        """
        # Simulação do processamento
        import time
        import random
        
        start_time = time.time()
        
        # Simular tempo de processamento baseado no tamanho do arquivo
        file_extension = Path(file_name).suffix.lower()
        base_time = {
            '.pdf': 0.5,
            '.png': 0.2,
            '.jpg': 0.2,
            '.jpeg': 0.2,
            '.tiff': 0.3
        }.get(file_extension, 0.3)
        
        processing_time = base_time + random.uniform(0.1, 0.3)
        time.sleep(processing_time)
        
        # Simular resultado baseado no tipo de arquivo
        extracted_text = f"Texto extraído do documento {file_name} via OCR simulado"
        confidence = random.uniform(0.85, 0.98)
        pages_processed = random.randint(1, 5) if file_extension == '.pdf' else 1
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        return {
            'extracted_text': extracted_text,
            'confidence': confidence,
            'pages_processed': pages_processed,
            'processing_time_ms': processing_time_ms,
            'file_size': random.randint(1024, 1024*1024)  # Simulated file size
        }


class ControlSheetProcessor:
    """
    Processador de planilhas de controle com validação robusta.
    """
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.csv', '.ods']
        self.max_rows = 10000  # Limite para evitar problemas de performance
        logger.info("ControlSheetProcessor inicializado")
    
    def _validate_sheet_inputs(self, file_name: str, bucket_name: str) -> None:
        """
        Valida os parâmetros de entrada para planilhas.
        
        Args:
            file_name: Nome do arquivo
            bucket_name: Nome do bucket
            
        Raises:
            ValidationError: Se os parâmetros são inválidos
        """
        if not file_name or not isinstance(file_name, str):
            raise ValidationError(
                "Nome do arquivo é obrigatório e deve ser uma string",
                field="file_name",
                validation_code="INVALID_FILENAME"
            )
        
        if not bucket_name or not isinstance(bucket_name, str):
            raise ValidationError(
                "Nome do bucket é obrigatório e deve ser uma string",
                field="bucket_name",
                validation_code="INVALID_BUCKET"
            )
        
        # Verificar extensão da planilha
        file_path = Path(file_name)
        if file_path.suffix.lower() not in self.supported_formats:
            raise ValidationError(
                f"Formato de planilha não suportado: {file_path.suffix}. "
                f"Formatos suportados: {', '.join(self.supported_formats)}",
                field="file_name",
                validation_code="UNSUPPORTED_SHEET_FORMAT"
            )
    
    @handle_exceptions(ErrorCategory.BUSINESS_LOGIC, ErrorSeverity.MEDIUM)
    def process_control_sheet(self, file_name: str, bucket_name: str) -> Dict[str, Any]:
        """
        Processa uma planilha de controle com validação robusta.
        
        Args:
            file_name: Nome do arquivo da planilha no bucket
            bucket_name: Nome do bucket GCS
            
        Returns:
            dict: Resultado do processamento com status e dados extraídos
            
        Raises:
            ValidationError: Para erros de validação de entrada
            Exception: Para outros erros de processamento
        """
        try:
            logger.info(f"Iniciando processamento de planilha: {file_name} do bucket {bucket_name}")
            
            # Validar entradas
            self._validate_sheet_inputs(file_name, bucket_name)
            
            # Processar planilha
            processing_result = self._perform_sheet_processing(file_name, bucket_name)
            
            # Validar resultado
            rows_processed = processing_result.get('rows_processed', 0)
            if rows_processed == 0:
                logger.warning(f"Nenhuma linha processada em {file_name}")
            elif rows_processed > self.max_rows:
                logger.warning(f"Planilha muito grande: {rows_processed} linhas (max: {self.max_rows})")
            
            result = {
                "status": "success",
                "file_name": file_name,
                "bucket_name": bucket_name,
                "rows_processed": rows_processed,
                "valid_entries": processing_result.get('valid_entries', 0),
                "invalid_entries": processing_result.get('invalid_entries', 0),
                "errors": processing_result.get('errors', []),
                "warnings": processing_result.get('warnings', []),
                "processing_time_ms": processing_result.get('processing_time_ms', 0),
                "metadata": {
                    "processor_version": "1.0.0",
                    "format_detected": Path(file_name).suffix.lower(),
                    "columns_detected": processing_result.get('columns_detected', 0),
                    "sheets_processed": processing_result.get('sheets_processed', 1)
                }
            }
            
            logger.info(f"Planilha processada com sucesso: {file_name}")
            return result
            
        except ValidationError as e:
            if ENHANCED_ERROR_HANDLING:
                error = error_handler.create_error(
                    message=f"Erro de validação no processamento de planilha: {e.message}",
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.MEDIUM,
                    error_code=e.validation_code,
                    details=f"Campo: {e.field}, Arquivo: {file_name}",
                    original_exception=e
                )
                error_handler.handle_error(error)
            
            return {
                "status": "validation_error",
                "file_name": file_name,
                "bucket_name": bucket_name,
                "error": e.message,
                "error_code": e.validation_code,
                "field": e.field
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento de planilha {file_name}: {str(e)}")
            
            if ENHANCED_ERROR_HANDLING:
                error = error_handler.create_error(
                    message=f"Falha no processamento de planilha {file_name}",
                    category=ErrorCategory.BUSINESS_LOGIC,
                    severity=ErrorSeverity.HIGH,
                    details=f"Bucket: {bucket_name}",
                    original_exception=e
                )
                error_handler.handle_error(error)
            
            return {
                "status": "error",
                "file_name": file_name,
                "bucket_name": bucket_name,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _perform_sheet_processing(self, file_name: str, bucket_name: str) -> Dict[str, Any]:
        """
        Simula o processamento real de planilha.
        Em implementação real, usaria pandas ou openpyxl.
        
        Args:
            file_name: Nome do arquivo
            bucket_name: Nome do bucket
            
        Returns:
            dict: Resultado simulado do processamento
        """
        import time
        import random
        
        start_time = time.time()
        
        # Simular processamento baseado no formato
        file_extension = Path(file_name).suffix.lower()
        
        # Simular número de linhas baseado no formato
        if file_extension == '.csv':
            rows_processed = random.randint(50, 500)
        elif file_extension in ['.xlsx', '.xls']:
            rows_processed = random.randint(100, 1000)
        else:
            rows_processed = random.randint(10, 100)
        
        # Simular validação das entradas
        valid_entries = max(1, int(rows_processed * random.uniform(0.85, 0.98)))
        invalid_entries = rows_processed - valid_entries
        
        # Simular erros encontrados
        errors = []
        warnings = []
        
        if invalid_entries > 0:
            errors.append(f"{invalid_entries} entradas com dados inválidos")
            
        if rows_processed > 500:
            warnings.append("Planilha grande detectada - considere dividir em arquivos menores")
        
        # Simular tempo de processamento
        processing_time = 0.1 + (rows_processed / 1000)
        time.sleep(min(processing_time, 2.0))  # Cap at 2 seconds for demo
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        return {
            'rows_processed': rows_processed,
            'valid_entries': valid_entries,
            'invalid_entries': invalid_entries,
            'errors': errors,
            'warnings': warnings,
            'processing_time_ms': processing_time_ms,
            'columns_detected': random.randint(5, 20),
            'sheets_processed': random.randint(1, 3) if file_extension in ['.xlsx', '.xls'] else 1
        }


# Instâncias globais dos processadores
document_processor = DocumentProcessor()
sheet_processor = ControlSheetProcessor()


def process_document_ocr(file_name: str, bucket_name: str) -> Dict[str, Any]:
    """
    Função de conveniência para processamento OCR (mantém compatibilidade com API existente).
    
    Args:
        file_name: Nome do arquivo PDF no bucket
        bucket_name: Nome do bucket GCS
        
    Returns:
        dict: Resultado do processamento com status e dados extraídos
    """
    return document_processor.process_document_ocr(file_name, bucket_name)


def process_control_sheet(file_name: str, bucket_name: str) -> Dict[str, Any]:
    """
    Função de conveniência para processamento de planilha (mantém compatibilidade com API existente).
    
    Args:
        file_name: Nome do arquivo da planilha no bucket
        bucket_name: Nome do bucket GCS
        
    Returns:
        dict: Resultado do processamento com status e dados extraídos
    """
    return sheet_processor.process_control_sheet(file_name, bucket_name)