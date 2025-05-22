# filepath: tests/test_docai_utils.py
import pytest
from unittest.mock import patch, mock_open, MagicMock, call, ANY
import importlib
import os
import json
import logging
import uuid

# Importe as classes reais com aliases para usar no 'spec' dos mocks
from google.oauth2 import service_account
from google.cloud import documentai
from google.cloud.documentai import DocumentProcessorServiceClient as RealDocumentProcessorServiceClient
from google.cloud.storage import Client as RealStorageClient
from google.cloud.storage import Blob as RealStorageBlob

# Módulo a ser testado (será recarregado em cada teste que modifica o ambiente)
import src.docai_utils

# --- Constantes para Configuração Mock ---
JSON_CONFIG_STRING = '{"gcp_project_id": "file_project", "gcp_location": "file_location", "docai_processor_id": "file_processor", "gcs_input_bucket": "file_bucket", "bq_dataset_id": "file_dataset", "bq_table_id": "file_table"}'
JSON_CONFIG_DICT = json.loads(JSON_CONFIG_STRING)

# --- Testes para Carregamento de Configuração ---

@patch('src.docai_utils.logging.getLogger')
@patch('src.docai_utils.json.load') # Mantendo o patch específico para o módulo
@patch.dict(os.environ, {}, clear=True)
@patch('os.path.exists') 
@patch('builtins.open', new_callable=mock_open) 
def test_config_loaded_from_file_when_env_vars_missing(mock_builtin_open, mock_os_path_exists, mock_json_load, mock_get_logger):
    mock_logger_instance = MagicMock()
    mock_get_logger.return_value = mock_logger_instance
    mock_json_load.return_value = JSON_CONFIG_DICT
    
    expected_config_path = os.path.join(os.path.dirname(src.docai_utils.__file__), 'config.json')
    
    def os_path_exists_side_effect(path):
        return path == expected_config_path
    mock_os_path_exists.side_effect = os_path_exists_side_effect

    importlib.reload(src.docai_utils) 
    
    config = src.docai_utils.get_docai_config()
    
    mock_get_logger.assert_called_with("src.docai_utils")
    mock_os_path_exists.assert_any_call(expected_config_path)
    mock_builtin_open.assert_called_once_with(expected_config_path, 'r')
    mock_json_load.assert_called_once_with(mock_builtin_open.return_value)
    
    assert config["gcp_project_id"] == "file_project"
    assert config["gcp_location"] == "file_location"
    assert config["docai_processor_id"] == "file_processor"
    assert config["gcs_input_bucket"] == "file_bucket"
    assert config["bq_dataset_id"] == "file_dataset"
    assert config["bq_table_id"] == "file_table"
    
    mock_logger_instance.warning.assert_not_called()
    mock_logger_instance.info.assert_any_call(f"Configuração carregada de {expected_config_path}")

@patch('src.docai_utils.logging.getLogger')
@patch('os.path.exists', return_value=False) 
@patch.dict(os.environ, {}, clear=True) 
@patch('src.docai_utils.json.load') 
@patch('src.docai_utils.open', new_callable=mock_open)
def test_config_loading_failure_raises_value_error(mock_src_open_not_called, mock_json_load_not_called, mock_os_path_exists_returns_false, mock_get_logger_fail_config):
    mock_logger_instance = MagicMock()
    mock_get_logger_fail_config.return_value = mock_logger_instance
    
    importlib.reload(src.docai_utils)

    with pytest.raises(ValueError) as excinfo:
        src.docai_utils.get_docai_config() 

    assert "Configuração do DocAI incompleta" in str(excinfo.value)
    assert "gcp_project_id" in str(excinfo.value) 
    
    mock_get_logger_fail_config.assert_called_with("src.docai_utils")
    mock_json_load_not_called.assert_not_called()
    mock_src_open_not_called.assert_not_called()
    
    mock_logger_instance.error.assert_called_once()
    error_log_call_args = mock_logger_instance.error.call_args[0][0]
    assert "Configuração do DocAI incompleta" in error_log_call_args
    assert "gcp_project_id" in error_log_call_args

# --- Testes para get_docai_client ---
@patch('logging.getLogger')
@patch('src.docai_utils.documentai.DocumentProcessorServiceClient')
@patch('src.docai_utils.service_account.Credentials.from_service_account_file')
def test_get_docai_client_with_key_path(mock_creds_from_file, mock_docai_constructor, mock_get_logger_client):
    mock_logger_instance = MagicMock()
    mock_get_logger_client.return_value = mock_logger_instance
    mock_credentials_obj = MagicMock(spec=service_account.Credentials)
    mock_creds_from_file.return_value = mock_credentials_obj
    mock_client_instance = MagicMock(spec=RealDocumentProcessorServiceClient)
    mock_docai_constructor.return_value = mock_client_instance
    key_path_test = "/fake/path/to/key.json"
    with patch.dict(os.environ, {"GCP_LOCATION": "test-loc", "GCP_PROJECT_ID": "p", "DOCAI_PROCESSOR_ID": "d", "GCS_INPUT_BUCKET": "b", "BQ_DATASET_ID": "ds", "BQ_TABLE_ID": "t"}):
        importlib.reload(src.docai_utils)
        mock_get_logger_client.return_value = mock_logger_instance
        client = src.docai_utils.get_docai_client(key_path=key_path_test)
    mock_creds_from_file.assert_called_once_with(key_path_test)
    mock_docai_constructor.assert_called_once()
    assert client == mock_client_instance

@patch('logging.getLogger')
@patch('src.docai_utils.documentai.DocumentProcessorServiceClient')
def test_get_docai_client_adc(mock_docai_constructor_adc, mock_get_logger_client_adc):
    mock_logger_instance = MagicMock()
    mock_get_logger_client_adc.return_value = mock_logger_instance
    mock_client_instance = MagicMock(spec=RealDocumentProcessorServiceClient)
    mock_docai_constructor_adc.return_value = mock_client_instance
    with patch.dict(os.environ, {"GCP_LOCATION": "test-loc-adc", "GCP_PROJECT_ID": "p", "DOCAI_PROCESSOR_ID": "d", "GCS_INPUT_BUCKET": "b", "BQ_DATASET_ID": "ds", "BQ_TABLE_ID": "t"}):
        importlib.reload(src.docai_utils)
        mock_get_logger_client_adc.return_value = mock_logger_instance
        client = src.docai_utils.get_docai_client(key_path=None)
    mock_docai_constructor_adc.assert_called_once()
    assert client == mock_client_instance

# --- Testes para process_document_ocr ---
@patch('logging.getLogger')
def test_process_document_ocr_success(mock_get_logger_ocr):
    mock_logger_instance = MagicMock()
    mock_get_logger_ocr.return_value = mock_logger_instance
    mock_docai_client_instance = MagicMock(spec=RealDocumentProcessorServiceClient)
    mock_get_docai_client_function = MagicMock(return_value=mock_docai_client_instance)
    mock_docai_client_instance.processor_path.return_value = "projects/test_project/locations/test_location/processors/test_processor"
    mock_process_result = MagicMock()
    mock_document_payload = MagicMock(spec=documentai.Document)
    mock_document_payload.text = "Conteúdo OCR."
    mock_process_result.document = mock_document_payload
    mock_docai_client_instance.process_document.return_value = mock_process_result
    test_gcs_uri = "gs://bucket/file.pdf"
    env_vars = {"GCP_PROJECT_ID": "test_project", "GCP_LOCATION": "test_location", "DOCAI_PROCESSOR_ID": "test_processor", "GCS_INPUT_BUCKET": "b", "BQ_DATASET_ID": "ds", "BQ_TABLE_ID": "t"}
    with patch.dict(os.environ, env_vars):
        importlib.reload(src.docai_utils)
        mock_get_logger_ocr.return_value = mock_logger_instance
        with patch.object(src.docai_utils, 'get_docai_client', mock_get_docai_client_function) as patched_get_client:
            document = src.docai_utils.process_document_ocr(project_id="test_project", location="test_location", processor_id="test_processor", gcs_uri=test_gcs_uri)
            patched_get_client.assert_called_once_with(None)
    assert document is not None

@patch('logging.getLogger')
def test_process_document_ocr_failure(mock_get_logger_ocr_fail):
    mock_logger_instance = MagicMock()
    mock_get_logger_ocr_fail.return_value = mock_logger_instance
    mock_docai_client_instance = MagicMock(spec=RealDocumentProcessorServiceClient)
    mock_docai_client_instance.processor_path.return_value = "projects/fail_project/locations/fail_location/processors/fail_processor"
    mock_get_docai_client_function = MagicMock(return_value=mock_docai_client_instance)
    mock_docai_client_instance.process_document.side_effect = Exception("DocAI API Error")
    test_gcs_uri = "gs://bucket/fail.pdf"
    env_vars = {"GCP_PROJECT_ID": "fail_project", "GCP_LOCATION": "fail_location", "DOCAI_PROCESSOR_ID": "fail_processor", "GCS_INPUT_BUCKET": "b", "BQ_DATASET_ID": "ds", "BQ_TABLE_ID": "t"}
    with patch.dict(os.environ, env_vars):
        importlib.reload(src.docai_utils)
        mock_get_logger_ocr_fail.return_value = mock_logger_instance
        with patch.object(src.docai_utils, 'get_docai_client', mock_get_docai_client_function) as patched_get_client:
            document = src.docai_utils.process_document_ocr(project_id="fail_project", location="fail_location", processor_id="fail_processor", gcs_uri=test_gcs_uri)
            patched_get_client.assert_called_once_with(None)
    assert document is None

# --- Testes para list_gcs_pdfs ---
@patch('logging.getLogger')
def test_list_gcs_pdfs_success(mock_get_logger_list_gcs):
    print("==> Iniciando test_list_gcs_pdfs_success")
    mock_logger_instance = MagicMock()
    mock_get_logger_list_gcs.return_value = mock_logger_instance
    mock_storage_client_instance = MagicMock(spec=RealStorageClient)
    print("    Mock de RealStorageClient criado")
    mock_gcs_client_constructor_function = MagicMock(return_value=mock_storage_client_instance)
    print("    Mock do construtor do cliente GCS criado")
    blob1_pdf = MagicMock(spec=RealStorageBlob); blob1_pdf.name = "folder/doc1.pdf"; blob1_pdf.content_type = "application/pdf"
    blob2_txt = MagicMock(spec=RealStorageBlob); blob2_txt.name = "folder/doc2.txt"; blob2_txt.content_type = "text/plain"
    mock_storage_client_instance.list_blobs.return_value = [blob1_pdf, blob2_txt]
    bucket_name = "test-bucket"; prefix_folder = "folder/"
    env_vars = {"GCP_PROJECT_ID": "p", "GCP_LOCATION": "l", "DOCAI_PROCESSOR_ID": "d", "GCS_INPUT_BUCKET": bucket_name, "BQ_DATASET_ID": "ds", "BQ_TABLE_ID": "t"}
    with patch.dict(os.environ, env_vars):
        print("    Ambiente mockado, recarregando módulo...")
        importlib.reload(src.docai_utils)
        print("    Módulo recarregado.")
        mock_get_logger_list_gcs.return_value = mock_logger_instance
        with patch.object(src.docai_utils.storage, 'Client', mock_gcs_client_constructor_function) as patched_constructor:
            print("    Patch para storage.Client aplicado. Chamando list_gcs_pdfs...")
            pdf_uris = src.docai_utils.list_gcs_pdfs(bucket_name, prefix_folder)
            print(f"    list_gcs_pdfs retornou: {pdf_uris}")
            patched_constructor.assert_called_once()
            print("    patched_constructor.assert_called_once() passou.")
    mock_storage_client_instance.list_blobs.assert_called_once_with(bucket_name, prefix=prefix_folder)
    assert len(pdf_uris) == 1
    print("==> Finalizando test_list_gcs_pdfs_success")

@patch('logging.getLogger')
def test_list_gcs_pdfs_correct_filtering(mock_get_logger_filter):
    mock_logger_instance = MagicMock()
    mock_get_logger_filter.return_value = mock_logger_instance
    mock_storage_client_instance = MagicMock(spec=RealStorageClient)
    mock_gcs_client_constructor_function = MagicMock(return_value=mock_storage_client_instance)
    blob1 = MagicMock(spec=RealStorageBlob); blob1.name = "folder/doc1.pdf"; blob1.content_type = "application/pdf"
    blob2 = MagicMock(spec=RealStorageBlob); blob2.name = "folder/doc2.txt"; blob2.content_type = "text/plain"
    blob3 = MagicMock(spec=RealStorageBlob); blob3.name = "folder/DOC4.PDF"; blob3.content_type = "application/pdf"
    blob4 = MagicMock(spec=RealStorageBlob); blob4.name = "folder/image.jpg"; blob4.content_type = "image/jpeg"
    mock_storage_client_instance.list_blobs.return_value = [blob1, blob2, blob3, blob4]
    bucket_name = "test-bucket-filter"; prefix_folder = "folder/"
    env_vars = {"GCP_PROJECT_ID": "p", "GCP_LOCATION": "l", "DOCAI_PROCESSOR_ID": "d", "GCS_INPUT_BUCKET": bucket_name, "BQ_DATASET_ID": "ds", "BQ_TABLE_ID": "t"}
    with patch.dict(os.environ, env_vars):
        importlib.reload(src.docai_utils)
        mock_get_logger_filter.return_value = mock_logger_instance
        with patch.object(src.docai_utils.storage, 'Client', mock_gcs_client_constructor_function) as patched_constructor:
            pdf_uris = src.docai_utils.list_gcs_pdfs(bucket_name, prefix_folder)
            patched_constructor.assert_called_once()
    mock_storage_client_instance.list_blobs.assert_called_once_with(bucket_name, prefix=prefix_folder)
    assert len(pdf_uris) == 2

@patch('logging.getLogger')
def test_list_gcs_pdfs_no_pdfs_found(mock_get_logger_no_pdf):
    mock_logger_instance = MagicMock()
    mock_get_logger_no_pdf.return_value = mock_logger_instance
    mock_storage_client_instance = MagicMock(spec=RealStorageClient)
    mock_gcs_client_constructor_function = MagicMock(return_value=mock_storage_client_instance)
    blob_txt = MagicMock(spec=RealStorageBlob); blob_txt.name = "file.txt"; blob_txt.content_type = "text/plain"
    mock_storage_client_instance.list_blobs.return_value = [blob_txt]
    bucket_name = "no-pdf-bucket"
    env_vars = {"GCP_PROJECT_ID": "p", "GCP_LOCATION": "l", "DOCAI_PROCESSOR_ID": "d", "GCS_INPUT_BUCKET": bucket_name, "BQ_DATASET_ID": "ds", "BQ_TABLE_ID": "t"}
    with patch.dict(os.environ, env_vars):
        importlib.reload(src.docai_utils)
        mock_get_logger_no_pdf.return_value = mock_logger_instance
        with patch.object(src.docai_utils.storage, 'Client', mock_gcs_client_constructor_function) as patched_constructor:
            pdf_uris = src.docai_utils.list_gcs_pdfs(bucket_name)
            patched_constructor.assert_called_once()
    mock_storage_client_instance.list_blobs.assert_called_once_with(bucket_name, prefix="")
    assert len(pdf_uris) == 0

@patch('logging.getLogger')
def test_list_gcs_pdfs_client_exception(mock_get_logger_exc):
    mock_logger_instance = MagicMock()
    mock_get_logger_exc.return_value = mock_logger_instance
    mock_gcs_client_constructor_function = MagicMock(side_effect=Exception("Falha ao criar cliente GCS"))
    bucket_name = "exception-bucket"
    env_vars = {"GCP_PROJECT_ID": "p", "GCP_LOCATION": "l", "DOCAI_PROCESSOR_ID": "d", "GCS_INPUT_BUCKET": bucket_name, "BQ_DATASET_ID": "ds", "BQ_TABLE_ID": "t"}
    with patch.dict(os.environ, env_vars):
        importlib.reload(src.docai_utils)
        mock_get_logger_exc.return_value = mock_logger_instance
        with patch.object(src.docai_utils.storage, 'Client', mock_gcs_client_constructor_function) as patched_constructor:
            pdf_uris = src.docai_utils.list_gcs_pdfs(bucket_name)
            patched_constructor.assert_called_once()
    assert len(pdf_uris) == 0
    mock_logger_instance.error.assert_called_once()