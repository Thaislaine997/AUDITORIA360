"""
Comprehensive OCR Integration Tests
Day 4: Create OCR integration tests for the OCR pipeline
"""

import os
import sys
import tempfile
from unittest.mock import MagicMock, mock_open, patch

import numpy as np
import pytest
from PIL import Image

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Mock PaddleOCR if not available
try:
    from paddleocr import PaddleOCR
except ImportError:
    sys.modules["paddleocr"] = MagicMock()
    from paddleocr import PaddleOCR

from services.ocr_utils import extrair_texto_ocr


class TestOCRIntegration:
    """Comprehensive test suite for OCR integration"""

    @pytest.fixture
    def sample_image_path(self):
        """Create a temporary sample image file"""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            # Create a simple test image
            img = Image.new("RGB", (100, 50), color="white")
            img.save(tmp_file.name, "PNG")
            yield tmp_file.name

        # Cleanup
        if os.path.exists(tmp_file.name):
            os.unlink(tmp_file.name)

    @pytest.fixture
    def mock_ocr_result(self):
        """Mock OCR result structure"""
        return [
            [
                ([[1, 2], [3, 4], [5, 6], [7, 8]], ("Texto linha 1", 0.95)),
                ([[10, 12], [13, 14], [15, 16], [17, 18]], ("Texto linha 2", 0.88)),
            ]
        ]

    @pytest.fixture
    def mock_empty_ocr_result(self):
        """Mock empty OCR result"""
        return [[]]

    @pytest.fixture
    def mock_complex_ocr_result(self):
        """Mock complex OCR result with multiple lines and varying confidence"""
        return [
            [
                ([[1, 2], [3, 4], [5, 6], [7, 8]], ("AUDITORIA360", 0.99)),
                (
                    [[10, 12], [13, 14], [15, 16], [17, 18]],
                    ("Relatório de Folha", 0.92),
                ),
                ([[20, 22], [23, 24], [25, 26], [27, 28]], ("Janeiro 2025", 0.85)),
                (
                    [[30, 32], [33, 34], [35, 36], [37, 38]],
                    ("Total: R$ 150.000,00", 0.96),
                ),
            ]
        ]

    # Test basic OCR functionality
    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_success(
        self, mock_paddleocr_class, sample_image_path, mock_ocr_result
    ):
        """Test successful text extraction from image"""
        # Setup mock
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = mock_ocr_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        # Test
        result = extrair_texto_ocr(sample_image_path)

        # Assertions
        assert result == "Texto linha 1\nTexto linha 2"
        mock_paddleocr_class.assert_called_once_with(use_angle_cls=True, lang="pt")
        mock_ocr_instance.ocr.assert_called_once_with(sample_image_path, cls=True)

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_empty_result(
        self, mock_paddleocr_class, sample_image_path, mock_empty_ocr_result
    ):
        """Test OCR with empty result"""
        # Setup mock
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = mock_empty_ocr_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        # Test
        result = extrair_texto_ocr(sample_image_path)

        # Assertions
        assert result == ""
        mock_paddleocr_class.assert_called_once_with(use_angle_cls=True, lang="pt")
        mock_ocr_instance.ocr.assert_called_once_with(sample_image_path, cls=True)

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_complex_result(
        self, mock_paddleocr_class, sample_image_path, mock_complex_ocr_result
    ):
        """Test OCR with complex result"""
        # Setup mock
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = mock_complex_ocr_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        # Test
        result = extrair_texto_ocr(sample_image_path)

        # Assertions
        expected_text = (
            "AUDITORIA360\nRelatório de Folha\nJaneiro 2025\nTotal: R$ 150.000,00"
        )
        assert result == expected_text

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_single_line(
        self, mock_paddleocr_class, sample_image_path
    ):
        """Test OCR with single line result"""
        single_line_result = [
            [([[1, 2], [3, 4], [5, 6], [7, 8]], ("Documento único", 0.95))]
        ]

        # Setup mock
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = single_line_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        # Test
        result = extrair_texto_ocr(sample_image_path)

        # Assertions
        assert result == "Documento único"

    # Test error handling
    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_file_not_found(self, mock_paddleocr_class):
        """Test OCR with non-existent file"""
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.side_effect = FileNotFoundError("Arquivo não encontrado")
        mock_paddleocr_class.return_value = mock_ocr_instance

        with pytest.raises(FileNotFoundError):
            extrair_texto_ocr("/path/to/nonexistent/file.png")

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_invalid_image(
        self, mock_paddleocr_class, sample_image_path
    ):
        """Test OCR with invalid image format"""
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.side_effect = Exception("Formato de imagem inválido")
        mock_paddleocr_class.return_value = mock_ocr_instance

        with pytest.raises(Exception):
            extrair_texto_ocr(sample_image_path)

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_paddleocr_initialization_error(
        self, mock_paddleocr_class, sample_image_path
    ):
        """Test OCR when PaddleOCR initialization fails"""
        mock_paddleocr_class.side_effect = Exception(
            "Erro na inicialização do PaddleOCR"
        )

        with pytest.raises(Exception):
            extrair_texto_ocr(sample_image_path)

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_malformed_result(
        self, mock_paddleocr_class, sample_image_path
    ):
        """Test OCR with malformed result structure"""
        malformed_result = [
            [
                ([[1, 2], [3, 4]], ("Texto incompleto",)),  # Missing confidence
                ([[5, 6]], ("Outro texto", 0.8)),  # Incomplete box coordinates
            ]
        ]

        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = malformed_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        # The current implementation is robust and handles malformed results gracefully
        # It extracts text from valid entries and ignores malformed ones
        result = extrair_texto_ocr(sample_image_path)

        # Should extract text from valid entries
        expected_text = "Texto incompleto\nOutro texto"
        assert result == expected_text

    # Test different file formats
    @pytest.mark.parametrize(
        "file_extension", [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
    )
    def test_extrair_texto_ocr_different_formats(self, file_extension, mock_ocr_result):
        """Test OCR with different image formats"""
        with tempfile.NamedTemporaryFile(
            suffix=file_extension, delete=False
        ) as tmp_file:
            # Create test image for each format
            img = Image.new("RGB", (100, 50), color="white")

            # Convert extension to PIL format
            format_map = {
                ".png": "PNG",
                ".jpg": "JPEG",
                ".jpeg": "JPEG",
                ".tiff": "TIFF",
                ".bmp": "BMP",
            }
            img_format = format_map.get(file_extension, "PNG")
            img.save(tmp_file.name, img_format)

            with patch("services.ocr_utils.PaddleOCR") as mock_paddleocr_class:
                mock_ocr_instance = MagicMock()
                mock_ocr_instance.ocr.return_value = mock_ocr_result
                mock_paddleocr_class.return_value = mock_ocr_instance

                result = extrair_texto_ocr(tmp_file.name)
                assert result == "Texto linha 1\nTexto linha 2"

            # Cleanup
            if os.path.exists(tmp_file.name):
                os.unlink(tmp_file.name)

    # Test OCR configuration parameters
    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_configuration(
        self, mock_paddleocr_class, sample_image_path, mock_ocr_result
    ):
        """Test that OCR is configured correctly"""
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = mock_ocr_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        extrair_texto_ocr(sample_image_path)

        # Verify OCR initialization parameters
        mock_paddleocr_class.assert_called_once_with(use_angle_cls=True, lang="pt")

        # Verify OCR method parameters
        mock_ocr_instance.ocr.assert_called_once_with(sample_image_path, cls=True)

    # Test special characters and encoding
    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_special_characters(
        self, mock_paddleocr_class, sample_image_path
    ):
        """Test OCR with special characters and accents"""
        special_chars_result = [
            [
                ([[1, 2], [3, 4], [5, 6], [7, 8]], ("João José da Silva", 0.95)),
                (
                    [[10, 12], [13, 14], [15, 16], [17, 18]],
                    ("Salário: R$ 3.500,50", 0.92),
                ),
                (
                    [[20, 22], [23, 24], [25, 26], [27, 28]],
                    ("Função: Técnico em Informática", 0.88),
                ),
                (
                    [[30, 32], [33, 34], [35, 36], [37, 38]],
                    ("E-mail: joao@empresa.com.br", 0.93),
                ),
            ]
        ]

        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = special_chars_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        result = extrair_texto_ocr(sample_image_path)

        expected_text = (
            "João José da Silva\n"
            "Salário: R$ 3.500,50\n"
            "Função: Técnico em Informática\n"
            "E-mail: joao@empresa.com.br"
        )
        assert result == expected_text

    # Test performance and resource management
    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_memory_efficiency(
        self, mock_paddleocr_class, sample_image_path
    ):
        """Test that OCR doesn't create multiple instances unnecessarily"""
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = [[]]
        mock_paddleocr_class.return_value = mock_ocr_instance

        # Call multiple times
        for _ in range(3):
            extrair_texto_ocr(sample_image_path)

        # Should create new instance each time (current implementation)
        assert mock_paddleocr_class.call_count == 3

    # Test integration with file paths
    def test_extrair_texto_ocr_with_relative_path(self, mock_ocr_result):
        """Test OCR with relative file path"""
        with patch("services.ocr_utils.PaddleOCR") as mock_paddleocr_class:
            mock_ocr_instance = MagicMock()
            mock_ocr_instance.ocr.return_value = mock_ocr_result
            mock_paddleocr_class.return_value = mock_ocr_instance

            # Test with relative path
            relative_path = "./test_image.png"
            result = extrair_texto_ocr(relative_path)

            assert result == "Texto linha 1\nTexto linha 2"
            mock_ocr_instance.ocr.assert_called_once_with(relative_path, cls=True)

    def test_extrair_texto_ocr_with_absolute_path(self, mock_ocr_result):
        """Test OCR with absolute file path"""
        with patch("services.ocr_utils.PaddleOCR") as mock_paddleocr_class:
            mock_ocr_instance = MagicMock()
            mock_ocr_instance.ocr.return_value = mock_ocr_result
            mock_paddleocr_class.return_value = mock_ocr_instance

            # Test with absolute path
            absolute_path = "/home/user/documents/test_image.png"
            result = extrair_texto_ocr(absolute_path)

            assert result == "Texto linha 1\nTexto linha 2"
            mock_ocr_instance.ocr.assert_called_once_with(absolute_path, cls=True)

    # Test edge cases
    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_empty_string_path(self, mock_paddleocr_class):
        """Test OCR with empty string path"""
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.side_effect = Exception("Caminho inválido")
        mock_paddleocr_class.return_value = mock_ocr_instance

        with pytest.raises(Exception):
            extrair_texto_ocr("")

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_none_path(self, mock_paddleocr_class):
        """Test OCR with None path"""
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.side_effect = TypeError("Tipo inválido")
        mock_paddleocr_class.return_value = mock_ocr_instance

        with pytest.raises(TypeError):
            extrair_texto_ocr(None)

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_very_long_path(
        self, mock_paddleocr_class, mock_ocr_result
    ):
        """Test OCR with very long file path"""
        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = mock_ocr_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        # Create a very long path
        long_path = "/".join(["very_long_directory_name"] * 20) + "/test_image.png"

        result = extrair_texto_ocr(long_path)
        assert result == "Texto linha 1\nTexto linha 2"

    # Test text processing edge cases
    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_whitespace_handling(
        self, mock_paddleocr_class, sample_image_path
    ):
        """Test OCR text with leading/trailing whitespace"""
        whitespace_result = [
            [
                ([[1, 2], [3, 4], [5, 6], [7, 8]], ("  Texto com espaços  ", 0.95)),
                ([[10, 12], [13, 14], [15, 16], [17, 18]], ("\tTexto com tab\t", 0.92)),
                (
                    [[20, 22], [23, 24], [25, 26], [27, 28]],
                    ("\nTexto com quebra\n", 0.88),
                ),
            ]
        ]

        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = whitespace_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        result = extrair_texto_ocr(sample_image_path)

        expected_text = "  Texto com espaços  \n\tTexto com tab\t\n\nTexto com quebra\n"
        assert result == expected_text

    @patch("services.ocr_utils.PaddleOCR")
    def test_extrair_texto_ocr_empty_text_lines(
        self, mock_paddleocr_class, sample_image_path
    ):
        """Test OCR with empty text lines"""
        empty_lines_result = [
            [
                ([[1, 2], [3, 4], [5, 6], [7, 8]], ("Linha 1", 0.95)),
                ([[10, 12], [13, 14], [15, 16], [17, 18]], ("", 0.50)),  # Empty text
                ([[20, 22], [23, 24], [25, 26], [27, 28]], ("Linha 3", 0.88)),
            ]
        ]

        mock_ocr_instance = MagicMock()
        mock_ocr_instance.ocr.return_value = empty_lines_result
        mock_paddleocr_class.return_value = mock_ocr_instance

        result = extrair_texto_ocr(sample_image_path)

        expected_text = "Linha 1\n\nLinha 3"  # Empty line preserved
        assert result == expected_text


class TestOCRPipelineIntegration:
    """Test OCR pipeline integration scenarios"""

    def test_ocr_pipeline_document_processing(self):
        """Test complete document processing pipeline"""
        with patch("services.ocr_utils.PaddleOCR") as mock_paddleocr_class:
            # Mock a complete payroll document
            payroll_result = [
                [
                    (
                        [[0, 0], [100, 0], [100, 20], [0, 20]],
                        ("FOLHA DE PAGAMENTO", 0.98),
                    ),
                    ([[0, 25], [80, 25], [80, 40], [0, 40]], ("Janeiro/2025", 0.95)),
                    (
                        [[0, 50], [60, 50], [60, 65], [0, 65]],
                        ("Nome: João Silva", 0.93),
                    ),
                    ([[0, 70], [70, 70], [70, 85], [0, 85]], ("Cargo: Analista", 0.91)),
                    (
                        [[0, 90], [90, 90], [90, 105], [0, 105]],
                        ("Salário: R$ 5.000,00", 0.96),
                    ),
                    (
                        [[0, 110], [85, 110], [85, 125], [0, 125]],
                        ("INSS: R$ 550,00", 0.94),
                    ),
                    (
                        [[0, 130], [80, 130], [80, 145], [0, 145]],
                        ("IRRF: R$ 427,63", 0.92),
                    ),
                ]
            ]

            mock_ocr_instance = MagicMock()
            mock_ocr_instance.ocr.return_value = payroll_result
            mock_paddleocr_class.return_value = mock_ocr_instance

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                # Create dummy image
                img = Image.new("RGB", (200, 150), color="white")
                img.save(tmp_file.name, "PNG")

                result = extrair_texto_ocr(tmp_file.name)

                expected_lines = [
                    "FOLHA DE PAGAMENTO",
                    "Janeiro/2025",
                    "Nome: João Silva",
                    "Cargo: Analista",
                    "Salário: R$ 5.000,00",
                    "INSS: R$ 550,00",
                    "IRRF: R$ 427,63",
                ]

                assert result == "\n".join(expected_lines)

                # Cleanup
                os.unlink(tmp_file.name)

    def test_ocr_batch_processing_simulation(self):
        """Test batch processing of multiple documents"""
        documents = ["doc1.png", "doc2.jpg", "doc3.pdf"]

        with patch("services.ocr_utils.PaddleOCR") as mock_paddleocr_class:
            mock_ocr_instance = MagicMock()

            # Different results for each document
            results = [
                [[([[0, 0], [50, 0], [50, 15], [0, 15]], ("Documento 1", 0.95))]],
                [[([[0, 0], [50, 0], [50, 15], [0, 15]], ("Documento 2", 0.97))]],
                [[([[0, 0], [50, 0], [50, 15], [0, 15]], ("Documento 3", 0.93))]],
            ]

            mock_ocr_instance.ocr.side_effect = results
            mock_paddleocr_class.return_value = mock_ocr_instance

            extracted_texts = []
            for doc in documents:
                text = extrair_texto_ocr(doc)
                extracted_texts.append(text)

            assert extracted_texts == ["Documento 1", "Documento 2", "Documento 3"]
            assert mock_ocr_instance.ocr.call_count == 3


if __name__ == "__main__":
    pytest.main([__file__])
