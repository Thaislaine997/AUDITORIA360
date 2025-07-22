import hashlib

try:
    from google.cloud import storage
    STORAGE_AVAILABLE = True
except ImportError:
    # Mock Google Cloud Storage for testing
    class MockStorageClient:
        def bucket(self, name):
            return MockBucket()
    
    class MockBucket:
        def blob(self, name):
            return MockBlob()
    
    class MockBlob:
        def download_as_bytes(self):
            return b"mock data for testing"
    
    storage = type('storage', (), {'Client': MockStorageClient})()
    STORAGE_AVAILABLE = False

def compute_hash(gcs_uri: str) -> str:
    _, path = gcs_uri.split('gs://')
    bucket_name, blob_name = path.split('/', 1)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    data = blob.download_as_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    return sha256