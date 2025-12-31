import os
import json
from datetime import date
from intent_engine.core.root_signer import sign_daily_root

PROVIDER = os.getenv("UAAL_ROOT_PUBLISHER", "local")

def publish_daily_root():
    signed = sign_daily_root()
    today = date.today().isoformat()
    payload = json.dumps(signed, indent=2)

    if PROVIDER == "aws":
        import boto3
        s3 = boto3.client("s3")
        s3.put_object(
            Bucket=os.getenv("UAAL_AUDIT_BUCKET"),
            Key=f"merkle-roots/{today}.json",
            Body=payload.encode(),
            ContentType="application/json"
        )

    elif PROVIDER == "azure":
        from azure.storage.blob import BlobServiceClient
        client = BlobServiceClient.from_connection_string(
            os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        )
        blob = client.get_blob_client(
            container=os.getenv("UAAL_AUDIT_CONTAINER"),
            blob=f"merkle-roots/{today}.json"
        )
        blob.upload_blob(payload, overwrite=True)

    else:
        with open(f"merkle-root-{today}.json", "w") as f:
            f.write(payload)

    return signed
