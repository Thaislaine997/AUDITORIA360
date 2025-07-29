import hashlib
from google.cloud import storage


def compute_hash(gcs_uri: str) -> str:
    _, path = gcs_uri.split("gs://")
    bucket_name, blob_name = path.split("/", 1)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    data = blob.download_as_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    return sha256
