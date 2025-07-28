"""
Tests for main API module functions and OCR processing
"""
import pytest
from unittest.mock import Mock, patch
from src.main import process_document_ocr, process_control_sheet

def test_process_document_ocr_success():
    """Test successful OCR document processing"""
    result = process_document_ocr("test.pdf", "test-bucket")
    
    assert result["status"] == "success"
    assert result["file_name"] == "test.pdf"
    assert result["bucket_name"] == "test-bucket"
    assert "extracted_text" in result
    assert "confidence" in result
    assert "pages_processed" in result

def test_process_document_ocr_different_files():
    """Test OCR processing with different file types"""
    # Test PDF
    result_pdf = process_document_ocr("document.pdf", "bucket1")
    assert result_pdf["status"] == "success"
    assert result_pdf["file_name"] == "document.pdf"
    
    # Test image
    result_img = process_document_ocr("image.jpg", "bucket2")
    assert result_img["status"] == "success"
    assert result_img["file_name"] == "image.jpg"

def test_process_control_sheet_success():
    """Test successful control sheet processing"""
    result = process_control_sheet("sheet.xlsx", "test-bucket")
    
    assert result["status"] == "success"
    assert result["file_name"] == "sheet.xlsx"
    assert result["bucket_name"] == "test-bucket"
    assert "rows_processed" in result
    assert "valid_entries" in result
    assert "errors" in result

def test_process_control_sheet_different_formats():
    """Test control sheet processing with different formats"""
    # Test Excel
    result_xlsx = process_control_sheet("data.xlsx", "bucket1")
    assert result_xlsx["status"] == "success"
    assert result_xlsx["rows_processed"] == 100
    
    # Test CSV
    result_csv = process_control_sheet("data.csv", "bucket2")
    assert result_csv["status"] == "success"

@patch('src.main.logger')
def test_process_document_ocr_with_logging(mock_logger):
    """Test OCR processing with logging verification"""
    result = process_document_ocr("test.pdf", "test-bucket")
    
    # Verify logging was called
    mock_logger.info.assert_called()
    assert result["status"] == "success"

@patch('src.main.logger')
def test_process_control_sheet_with_logging(mock_logger):
    """Test control sheet processing with logging verification"""
    result = process_control_sheet("test.xlsx", "test-bucket")
    
    # Verify logging was called
    mock_logger.info.assert_called()
    assert result["status"] == "success"

def test_process_document_ocr_edge_cases():
    """Test OCR processing edge cases"""
    # Empty file name
    result = process_document_ocr("", "bucket")
    assert result["status"] == "success"
    assert result["file_name"] == ""
    
    # Special characters in name
    result = process_control_sheet("file with spaces & symbols.pdf", "bucket")
    assert result["status"] == "success"

def test_return_data_structure():
    """Test that return data structures are consistent"""
    ocr_result = process_document_ocr("test.pdf", "bucket")
    sheet_result = process_control_sheet("test.xlsx", "bucket")
    
    # Both should have status
    assert "status" in ocr_result
    assert "status" in sheet_result
    
    # Both should have file_name and bucket_name
    assert "file_name" in ocr_result
    assert "file_name" in sheet_result
    assert "bucket_name" in ocr_result
    assert "bucket_name" in sheet_result

def test_mock_ocr_confidence_values():
    """Test OCR confidence values are realistic"""
    result = process_document_ocr("test.pdf", "bucket")
    
    confidence = result.get("confidence", 0)
    assert 0 <= confidence <= 1.0
    assert isinstance(confidence, (int, float))

def test_mock_sheet_processing_values():
    """Test sheet processing values are realistic"""
    result = process_control_sheet("test.xlsx", "bucket")
    
    rows_processed = result.get("rows_processed", 0)
    valid_entries = result.get("valid_entries", 0)
    
    assert rows_processed >= 0
    assert valid_entries >= 0
    assert valid_entries <= rows_processed