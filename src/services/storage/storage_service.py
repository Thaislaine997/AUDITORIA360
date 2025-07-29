"""
Storage service for managing file operations with Cloudflare R2.
"""

import logging
import os
from typing import Optional

import boto3
from dotenv import load_dotenv

from src.core.exceptions import ProcessingError

load_dotenv()
logger = logging.getLogger(__name__)


class StorageService:
    """Service for file storage operations using Cloudflare R2."""
    
    def __init__(self):
        """Initialize storage service with R2 configuration."""
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.access_key_id = os.getenv("R2_ACCESS_KEY_ID")
        self.secret_access_key = os.getenv("R2_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("R2_BUCKET_NAME")
        
        if not all([self.account_id, self.access_key_id, self.secret_access_key, self.bucket_name]):
            logger.error("Missing R2 configuration environment variables")
            raise ProcessingError("Storage service configuration incomplete", "STORAGE_CONFIG")
    
    def get_client(self):
        """Get R2 client instance."""
        try:
            client = boto3.client(
                service_name="s3",
                endpoint_url=f"https://{self.account_id}.r2.cloudflarestorage.com",
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name="auto",
            )
            return client
        except Exception as e:
            logger.error(f"Failed to create R2 client: {e}")
            raise ProcessingError(f"Storage client creation failed: {e}", "STORAGE_CLIENT")
    
    def upload_file(self, file_path: str, object_name: str) -> bool:
        """
        Upload file to R2 bucket.
        
        Args:
            file_path: Local path to the file
            object_name: Name of the object in the bucket
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                raise ProcessingError(f"File not found: {file_path}", "FILE_NOT_FOUND")
            
            client = self.get_client()
            client.upload_file(file_path, self.bucket_name, object_name)
            
            logger.info(f"File '{file_path}' uploaded to '{object_name}' in R2")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {e}")
            raise ProcessingError(f"File upload failed: {e}", "STORAGE_UPLOAD")
    
    def download_file(self, object_name: str, dest_path: str) -> bool:
        """
        Download file from R2 bucket.
        
        Args:
            object_name: Name of the object in the bucket
            dest_path: Local destination path
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            client = self.get_client()
            client.download_file(self.bucket_name, object_name, dest_path)
            
            logger.info(f"File '{object_name}' downloaded to '{dest_path}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download file {object_name}: {e}")
            raise ProcessingError(f"File download failed: {e}", "STORAGE_DOWNLOAD")
    
    def delete_file(self, object_name: str) -> bool:
        """
        Delete file from R2 bucket.
        
        Args:
            object_name: Name of the object to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            client = self.get_client()
            client.delete_object(Bucket=self.bucket_name, Key=object_name)
            
            logger.info(f"File '{object_name}' deleted from R2")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete file {object_name}: {e}")
            raise ProcessingError(f"File deletion failed: {e}", "STORAGE_DELETE")
    
    def list_files(self, prefix: str = "") -> list:
        """
        List files in R2 bucket.
        
        Args:
            prefix: Optional prefix to filter files
            
        Returns:
            List of object names
        """
        try:
            client = self.get_client()
            response = client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            return []
            
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            raise ProcessingError(f"File listing failed: {e}", "STORAGE_LIST")


# Legacy functions for backward compatibility
def get_r2_client():
    """Legacy function for backward compatibility."""
    storage_service = StorageService()
    return storage_service.get_client()


def upload_file_to_r2(file_path: str, object_name: str):
    """Legacy function for backward compatibility."""
    storage_service = StorageService()
    storage_service.upload_file(file_path, object_name)
    print(f"Arquivo '{file_path}' enviado para '{object_name}' no R2.")


def download_file_from_r2(object_name: str, dest_path: str):
    """Legacy function for backward compatibility."""
    storage_service = StorageService()
    storage_service.download_file(object_name, dest_path)
    print(f"Arquivo '{object_name}' baixado do R2 para '{dest_path}'.")


def delete_file_from_r2(object_name: str):
    client = get_r2_client()
    bucket_name = os.getenv("R2_BUCKET_NAME")
    client.delete_object(Bucket=bucket_name, Key=object_name)
    print(f"Arquivo '{object_name}' removido do R2.")
