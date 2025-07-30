"""
OCR service using PaddleOCR for text extraction.
"""

import logging
from typing import Dict

from paddleocr import PaddleOCR

from src.core.exceptions import ProcessingError

logger = logging.getLogger(__name__)


class OCRService:
    """Service for OCR text extraction using PaddleOCR."""

    def __init__(self, use_angle_cls: bool = True, lang: str = "pt"):
        """Initialize OCR service with configuration."""
        try:
            self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
        except Exception as e:
            logger.error(f"Failed to initialize OCR: {e}")
            raise ProcessingError(f"OCR initialization failed: {e}", "OCR_INIT")

    def extract_text(self, file_path: str) -> Dict[str, any]:
        """
        Extract text from image or PDF file.

        Args:
            file_path: Path to the file to process

        Returns:
            Dict with extracted text and confidence information
        """
        try:
            logger.info(f"Processing OCR for file: {file_path}")

            result = self.ocr.ocr(file_path, cls=True)

            if not result or not result[0]:
                return {
                    "status": "success",
                    "extracted_text": "",
                    "confidence": 0.0,
                    "lines": [],
                }

            texts = []
            lines_info = []
            total_confidence = 0.0
            valid_lines = 0

            for line in result:
                for detection in line:
                    if len(detection) >= 2:
                        text = detection[1][0]
                        confidence = detection[1][1]

                        texts.append(text)
                        lines_info.append(
                            {
                                "text": text,
                                "confidence": confidence,
                                "bbox": detection[0] if len(detection) > 0 else None,
                            }
                        )

                        total_confidence += confidence
                        valid_lines += 1

            avg_confidence = total_confidence / valid_lines if valid_lines > 0 else 0.0

            return {
                "status": "success",
                "extracted_text": "\n".join(texts),
                "confidence": avg_confidence,
                "lines": lines_info,
                "total_lines": valid_lines,
            }

        except Exception as e:
            logger.error(f"OCR processing failed for {file_path}: {e}")
            raise ProcessingError(f"OCR processing failed: {e}", "OCR_PROCESSING")


# Legacy function for backward compatibility
def extrair_texto_ocr(caminho_arquivo: str) -> str:
    """Legacy function for backward compatibility."""
    ocr_service = OCRService()
    result = ocr_service.extract_text(caminho_arquivo)
    return result["extracted_text"]
