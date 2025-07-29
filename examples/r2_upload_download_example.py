"""
Exemplo de upload e download de arquivo no Cloudflare R2 usando storage_utils.
Requer: boto3, python-dotenv
"""

import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "services"))
)
from storage_utils import download_file_from_r2, upload_file_to_r2

if __name__ == "__main__":
    # Exemplo de upload
    upload_file_to_r2("README.md", "exemplo_README.md")
    # Exemplo de download
    download_file_from_r2("exemplo_README.md", "README_baixado.md")
